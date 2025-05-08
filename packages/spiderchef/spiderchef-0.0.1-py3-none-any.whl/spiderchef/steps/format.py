from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin

from structlog import get_logger

from spiderchef.steps.base import SyncStep

if TYPE_CHECKING:
    from spiderchef.recipe import Recipe

log = get_logger()


class ToInt(SyncStep):
    """Convert to integer."""

    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        return int(previous_output)


class JoinBaseUrl(SyncStep):
    """Joins a string (+optional path) with base_url"""

    path: str = ""

    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        if isinstance(previous_output, list):
            previous_output = [
                urljoin(recipe.base_url, self.path + str(i)) for i in previous_output
            ]
        else:
            previous_output = urljoin(recipe.base_url, self.path + str(previous_output))
        return previous_output


class ToMoneyStep(SyncStep):
    """Converts string to money format.

    Handles different currency formats, decimal separators, and thousands separators.
    Examples:
    - '1.407' → 1407 (if period is thousands separator)
    - '1,407.99' → 1407.99 (US format)
    - '1.407,99' → 1407.99 (EU format)
    """

    decimal_separator: str = ","
    thousands_separator: str = "."

    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> float:
        if previous_output is None:
            return 0.0

        value = str(previous_output).strip()

        # Handle different formats
        if self.decimal_separator == "." and self.thousands_separator == ",":
            # US format: 1,234.56
            value = value.replace(self.thousands_separator, "")
        elif self.decimal_separator == "," and self.thousands_separator == ".":
            # EU format: 1.234,56
            value = value.replace(self.thousands_separator, "")
            value = value.replace(self.decimal_separator, ".")
        elif self.decimal_separator == "." and "," not in value:
            # Format like '1.407' without any decimal part
            # Count dots to determine if it's a thousands separator or decimal
            if value.count(".") == 1 and len(value.split(".")[-1]) <= 2:
                # Likely a decimal separator: 1.40
                pass
            else:
                # Likely a thousands separator: 1.407 → 1407
                value = value.replace(".", "")

        try:
            return float(value)
        except ValueError:
            log.warning(f"Could not convert '{previous_output}' to money value")
            return 0.0
