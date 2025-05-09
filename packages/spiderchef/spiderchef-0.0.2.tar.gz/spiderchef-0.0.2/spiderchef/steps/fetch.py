import urllib
from typing import TYPE_CHECKING, Any, Literal

import orjson
from aiohttp import ClientResponse
from curl_cffi import Response
from pydantic import Field
from structlog import get_logger

from spiderchef.exceptions import ResponseIsNotOkError
from spiderchef.steps.base import AsyncStep

if TYPE_CHECKING:
    from spiderchef.recipe import Recipe

log = get_logger()


class FetchStep(AsyncStep):
    """Step to fetch data from an API."""

    return_type: Literal["text", "json", "response"] = "text"
    method: Literal["GET", "POST"] = "GET"
    path: str = ""
    params: dict[str, Any] = Field(default_factory=dict)
    json_data: dict[str, Any] = Field(default_factory=dict)
    data: dict[str, Any] | str = Field(default_factory=dict)
    headers: dict[str, Any] = Field(default_factory=dict)
    ok_status_codes: list[int] = Field(default_factory=list)
    timeout: int = 5

    def validate_response(self, response: ClientResponse | Response):
        if isinstance(response, ClientResponse):
            status = response.status
        else:
            status = response.status_code
        if not self.ok_status_codes:
            self.ok_status_codes = [200]
        if status not in self.ok_status_codes:
            raise ResponseIsNotOkError(status)

    async def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        session = await recipe.session
        encoded_params = (
            urllib.parse.urlencode(self.params, doseq=True)
            if recipe.session_type == "aiohttp"
            else self.params
        )
        match self.method:
            case "GET":
                recipe._response = await session.get(
                    url=self.path,
                    params=encoded_params,
                    timeout=self.timeout,
                    headers=self.headers,
                )
            case "POST":
                if self.data:
                    recipe._response = await session.post(
                        url=self.path,
                        params=encoded_params,
                        data=self.data,
                        timeout=self.timeout,
                        headers=self.headers,
                    )
                else:
                    recipe._response = await session.post(
                        url=self.path,
                        params=encoded_params,
                        json=self.json_data,
                        timeout=self.timeout,
                        headers=self.headers,
                    )
        self.validate_response(recipe._response)
        if recipe.session_type == "aiohttp":
            recipe.text_response = await recipe._response.text()
            if self.return_type == "json":
                recipe.json_response = await recipe._response.json(loads=orjson.loads)
        else:
            recipe.text_response = recipe._response.text
            if self.return_type == "json":
                recipe.json_response = recipe._response.json()
        match self.return_type:
            case "json":
                return recipe.json_response
            case "text":
                return recipe.text_response
            case "response":
                return recipe._response
