from typing import Any, ClassVar, Literal

import yaml
from aiohttp import ClientResponse, ClientSession
from curl_cffi import CurlHttpVersion
from curl_cffi.requests import AsyncSession, Response
from lxml.etree import _ElementTree
from pydantic import BaseModel, Field, HttpUrl, field_validator
from structlog import get_logger

from spiderchef.steps import STEP_REGISTRY, AsyncStep, BaseStep

log = get_logger()


# TBD: Proxies still need to be fully integrated
class Proxy(BaseModel):
    proxy_url: HttpUrl | None = None
    username: str | None = None
    password: str | None = None


class Recipe(BaseModel):
    step_registry: ClassVar[dict[str, BaseStep]] = STEP_REGISTRY
    name: str = "test_recipe"
    base_url: str
    session_type: Literal["aiohttp", "curl-cffi"] = "curl-cffi"
    http_version: Literal["1", "1.1", "2", "3"] = "2"
    impersonate: str = "firefox133"
    default_encoding: str = "utf-8"
    _session: ClientSession | AsyncSession | None = None
    _response: ClientResponse | Response | None = None
    _tree: _ElementTree | None = None
    json_response: Any = None
    text_response: str | None = None
    headers: dict = Field(default_factory=dict)
    proxies: list[Proxy] = Field(default_factory=list)
    steps: list[BaseStep]

    @classmethod
    def from_yaml(cls, file_path: str):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return cls(**data)

    @field_validator("steps", mode="before")
    def convert_step_dicts(cls, value: list[dict]) -> dict:
        """Convert step dictionaries to Step instances before model creation."""
        converted_steps = []
        for step in value:
            if isinstance(step, dict) and "type" in step:
                step_class = cls.step_registry.get(step["type"])
                if not step_class:
                    raise ValueError(f"Unknown step type: {step['type']}")

                step_class.step_registry = cls.step_registry
                # Create the step instance
                step_instance = step_class(**step)

                converted_steps.append(step_instance)
            else:
                # If it's already a Step instance or something else, keep it as is
                converted_steps.append(step)

        return converted_steps

    @property
    async def session(self) -> ClientSession | AsyncSession:
        if not self._session:
            if self.session_type == "aiohttp":
                self._session = ClientSession(base_url=self.base_url)
            else:
                match self.http_version:
                    case "2":
                        http_version = CurlHttpVersion.V2TLS
                    case "1.1":
                        http_version = CurlHttpVersion.V1_1
                    case "1":
                        http_version = CurlHttpVersion.V1_0
                    case "3":
                        http_version = CurlHttpVersion.V3
                self._session = AsyncSession(
                    base_url=self.base_url,
                    http_version=http_version,
                    impersonate=self.impersonate,
                    default_encoding=self.default_encoding,
                )
            await self._session.__aenter__()
        return self._session

    async def close(self) -> None:
        if self._session:
            await self._session.__aexit__(None, None, None)

    async def cook(self) -> Any:
        output = None
        log.info(f"🥣🥄🔥 Cooking '{self.name}' recipe!")
        for step_number, step in enumerate(self.steps, start=1):
            log.info(
                f"➡️  {step_number}. {step.name}...", step_class=step.__class__.__name__
            )
            if issubclass(type(step), AsyncStep):
                output = await step.execute(self, output)
            else:
                output = step.execute(self, output)
        await self.close()
        log.info(f"🍞 '{self.name}' recipe finished", output=output)
        return output
