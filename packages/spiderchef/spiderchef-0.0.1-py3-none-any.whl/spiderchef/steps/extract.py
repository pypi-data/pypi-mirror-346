import string
from re import findall
from typing import TYPE_CHECKING, Any, Literal

from lxml.html import fromstring, tostring
from pydantic import field_validator
from pydash import get
from structlog import get_logger

from spiderchef.steps.base import AsyncStep, BaseStep, SyncStep

if TYPE_CHECKING:
    from spiderchef.recipe import Recipe

log = get_logger()


class GetValueStep(SyncStep):
    """Step to get a value from the recipe's JSON data."""

    expression: str

    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        if "[]" in self.expression:
            expr = self.expression.replace("[]", "")
            json_value = (
                previous_output if self.use_previous_output else recipe.json_response
            )
            for i in expr.split("."):
                if isinstance(json_value, dict):
                    json_value = get(json_value, i)
                elif isinstance(json_value, list):
                    json_value = [get(val, i) for val in json_value]
            return json_value
        return get(
            previous_output if self.use_previous_output else recipe.json_response,
            self.expression,
        )


class XpathValueStep(SyncStep):
    """Step to xpath a value from the recipe's text data."""

    expression: str
    return_type: Literal["text", "element", "html"] = "html"
    rebuild_tree: bool = False

    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        output = []
        if not recipe._tree or self.rebuild_tree:
            recipe._tree = fromstring(recipe.text_response)
        if recipe._tree is not None:
            for i in recipe._tree.xpath(self.expression):
                if self.return_type == "text":
                    output.append(i.text)
                elif self.return_type == "element":
                    output.append(i)
                else:
                    output.append(tostring(i, encoding="utf-8").decode())
        return output


class RegexValueStep(SyncStep):
    """Step to regex a value from the recipe's text data."""

    index: int | None = None
    expression: str

    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        items = []
        if not self.use_previous_output and recipe.text_response:
            items = findall(self.expression, recipe.text_response)
        else:
            items = findall(self.expression, previous_output)
        if isinstance(self.index, int):
            return items[self.index]
        return items


class RegexFirstStep(RegexValueStep):
    index: int = 0


class ExtractItemsStep(AsyncStep):
    """Step to regex a value from the recipe's text data."""

    expression: str
    expression_type: Literal["json", "xpath", "regex"] = "regex"
    items: dict[str, list[BaseStep]]

    @field_validator("items", mode="before")
    def convert_step_dicts(
        cls, value: dict[str, list[dict]]
    ) -> dict[str, list[BaseStep]]:
        """Convert step dictionaries to Step instances before model creation."""
        converted_steps = {}
        for item, steps in value.items():
            converted_steps[item] = []
            for step in steps:
                if isinstance(step, dict) and "type" in step:
                    step_class = cls.step_registry.get(step["type"])
                    if not step_class:
                        raise ValueError(f"Unknown step type: {step['type']}")

                    # Create the step instance
                    converted_steps[item].append(step_class(**step))
                else:
                    # If it's already a Step instance or something else, keep it as is
                    converted_steps[item].append(step)

        return converted_steps

    async def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        outputs = []
        match self.expression_type:
            case "json":
                extraction_cls = GetValueStep
            case "xpath":
                extraction_cls = XpathValueStep
            case "regex":
                extraction_cls = RegexValueStep

        data_items = extraction_cls(
            expression=self.expression,
            use_previous_output=self.use_previous_output,
        ).execute(recipe, previous_output)

        for data_number, data in enumerate(data_items, start=1):
            output = {}
            log.info(f"  ➡️  {data_number}.  Extracting item ")
            for item_number, item in zip(string.ascii_lowercase, self.items.items()):
                item, steps = item
                item_output = data
                log.info(f"    ➡️  {item_number}.  Extracting {item}...")
                for step in steps:
                    if issubclass(type(step), AsyncStep):
                        item_output = await step.execute(recipe, item_output)
                    else:
                        item_output = step.execute(recipe, item_output)
                output[item] = item_output
            outputs.append(output)
        return outputs
