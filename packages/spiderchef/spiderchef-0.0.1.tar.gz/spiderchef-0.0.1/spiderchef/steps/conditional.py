from typing import TYPE_CHECKING, Any, Literal

from pydash import get

from spiderchef.steps.base import SyncStep

if TYPE_CHECKING:
    from spiderchef.recipe import Recipe


class CompareStep(SyncStep):
    """Step to compare two values from the recipe's JSON data."""

    left_key: str
    right_key: str
    condition: Literal[
        "greater_than",
        "less_than",
        "equal",
        "greater_than_or_equal",
        "less_than_or_equal",
    ]

    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> bool:
        def get_value(json_response: dict[str, Any], key: str) -> int:
            if value := get(json_response, key):
                return value if isinstance(value, float | int) else len(value)
            raise ValueError(f"Could not get value for key: {key}")

        left_value = get_value(recipe.json_response, self.left_key)
        right_value = get_value(recipe.json_response, self.right_key)

        match self.condition:
            case "greater_than":
                return left_value > right_value
            case "equal":
                return left_value == right_value
            case "less_than":
                return left_value < right_value
            case "greater_than_or_equal":
                return left_value >= right_value
            case "less_than_or_equal":
                return left_value <= right_value
