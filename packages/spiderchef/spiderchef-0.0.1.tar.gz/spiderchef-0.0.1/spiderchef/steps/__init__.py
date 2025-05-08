from spiderchef.steps.base import AsyncStep, BaseStep, SyncStep
from spiderchef.steps.conditional import CompareStep
from spiderchef.steps.extract import (
    ExtractItemsStep,
    GetValueStep,
    RegexFirstStep,
    RegexValueStep,
    XpathValueStep,
)
from spiderchef.steps.fetch import FetchStep
from spiderchef.steps.format import JoinBaseUrl, ToInt, ToMoneyStep

# Registry of available steps
STEP_REGISTRY: dict[str, type[BaseStep]] = {
    "get": GetValueStep,
    "compare": CompareStep,
    "fetch": FetchStep,
    "regex": RegexValueStep,
    "regex_first": RegexFirstStep,
    "xpath": XpathValueStep,
    "join_base_url": JoinBaseUrl,
    "extract_items": ExtractItemsStep,
    "to_money": ToMoneyStep,
    "to_int": ToInt,
}

__all__ = ["STEP_REGISTRY", "AsyncStep", "BaseStep", "SyncStep"]
