from spiderchef.steps.base import AsyncStep, BaseStep, SyncStep
from spiderchef.steps.conditional import CompareStep
from spiderchef.steps.extract import (
    ExtractItemsStep,
    GetValueStep,
    RegexFirstStep,
    RegexValueStep,
    XpathFirstStep,
    XpathValueStep,
)
from spiderchef.steps.fetch import FetchStep
from spiderchef.steps.format import (
    JoinBaseUrl,
    RemoveExtraWhitespace,
    RemoveHTMLTags,
    ToFloat,
    ToInt,
    ToMoneyStep,
    ToStr,
)

# Registry of available steps
STEP_REGISTRY: dict[str, type[BaseStep]] = {
    "get": GetValueStep,
    "compare": CompareStep,
    "fetch": FetchStep,
    "regex": RegexValueStep,
    "regex_first": RegexFirstStep,
    "xpath_first": XpathFirstStep,
    "xpath": XpathValueStep,
    "join_base_url": JoinBaseUrl,
    "extract_items": ExtractItemsStep,
    "to_money": ToMoneyStep,
    "to_int": ToInt,
    "to_str": ToStr,
    "to_float": ToFloat,
    "remove_extra_whitespace": RemoveExtraWhitespace,
    "remove_html_tags": RemoveHTMLTags,
}

__all__ = ["STEP_REGISTRY", "AsyncStep", "BaseStep", "SyncStep"]
