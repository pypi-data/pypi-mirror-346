from collections.abc import AsyncGenerator
from pathlib import Path
from typing import IO, Any, Literal

import requests
from _typeshed import Incomplete
from pydantic import BaseModel

from .endpoints import Endpoints as Endpoints
from .endpoints import RequestMethod as RequestMethod
from .exceptions import APIKeyMissingError as APIKeyMissingError
from .models import ResponseFormat
from .releases import AllReleases as AllReleases
from .settings import VerboseLevel as VerboseLevel
from .settings import delos_logger as delos_logger

DELOS_PLATFORM_BACKEND_URL: str

class APIClient(BaseModel):
    api_key: str
    _server_url: str
    _verbose: VerboseLevel
    _session: requests.Session
    _client_version: Any

    class Config:
        arbitrary_types_allowed: bool

    def __init__(
        self,
        api_key: str,
        server_url: str = ...,
        verbose: VerboseLevel = ...,
    ) -> None: ...
    @property
    def server_url(self) -> str: ...
    @property
    def verbose(self) -> VerboseLevel: ...

class IndexClient(APIClient):
    api_key: Incomplete
    server_url: Incomplete
    verbose: Incomplete
    session: Incomplete

    def __init__(
        self,
        api_key: str,
        server_url: str | None = ...,
        verbose: VerboseLevel = ...,
    ) -> None: ...
    def files_index_create(
        self,
        name: str,
        read_images: bool = False,
        filepaths: list[Path] | list[str] | None = None,
        filesobjects: list[tuple[str, IO[bytes]]] | None = None,
        tags_index: list[str] | None = None,
        tags_files: list[str] | None = None,
    ) -> dict[str, Any] | None: ...
    def files_index_files_add(
        self,
        index_uuid: str,
        read_images: bool = False,
        filepaths: list[Path] | list[str] | None = None,
        filesobjects: list[tuple[str, IO[bytes]]] | None = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any] | None: ...
    def files_index_retry(
        self,
        index_uuid: str,
        read_images: bool = False,
        tags: list[str] | None = None,
    ) -> dict[str, Any] | None: ...
    def files_index_files_delete(self, index_uuid: str, files_ids: list[str]) -> dict[str, Any] | None: ...
    def files_index_delete(self, index_uuid: str) -> dict[str, Any] | None: ...
    def files_index_restore(self, index_uuid: str) -> dict[str, Any] | None: ...
    def files_index_rename(self, index_uuid: str, name: str) -> dict[str, Any] | None: ...
    def files_index_ask(
        self,
        index_uuid: str,
        question: str,
        output_language: str | None = None,
        active_files: list[str] | str | None = None,
        tags: list[str] | None = None,
        instructions: str | None = None,
    ) -> dict[str, Any] | None: ...
    def files_index_embed(self, index_uuid: str) -> dict[str, Any] | None: ...
    def files_index_details(self, index_uuid: str) -> dict[str, Any] | None: ...
    def files_index_list(self) -> dict[str, Any] | None: ...
    def files_index_tags_get(self: IndexClient, index_uuid: str) -> dict[str, Any] | None: ...
    def files_index_tags_update(self: IndexClient, index_uuid: str, tags: list[str]) -> dict[str, Any] | None: ...
    def files_index_files_tags_update(
        self: IndexClient,
        index_uuid: str,
        file_uuids: str | list[str],
        tags: list[str],
    ) -> dict[str, Any] | None: ...

class DelosClient(IndexClient):
    api_key: Incomplete
    server_url: Incomplete
    verbose: Incomplete
    session: Incomplete

    def __init__(
        self,
        api_key: str,
        server_url: str | None = ...,
        verbose: VerboseLevel = ...,
    ) -> None: ...
    def status_health(self) -> dict[str, Any] | None: ...
    def translate_text(
        self,
        text: str,
        output_language: str,
        input_language: str | None = None,
    ) -> dict[str, Any] | None: ...
    def translate_file(
        self,
        output_language: str,
        input_language: str | None = None,
        return_type: Literal["raw_text", "url", "file"] = "raw_text",
        filepath: Path | str | None = None,
        fileobject: tuple[str, IO[bytes]] | None = None,
    ) -> dict[str, Any] | None: ...
    def web_search(
        self,
        text: str,
        output_language: str | None = None,
        desired_urls: list[str] | str | None = None,
    ) -> dict[str, Any] | None: ...
    def llm_chat(
        self: DelosClient,
        text: str,
        model: str,
        messages: list[dict[str, str]] | None = None,
        temperature: float | None = None,
        response_format: ResponseFormat | str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None: ...
    async def llm_chat_stream(
        self: DelosClient,
        text: str,
        model: str,
        messages: list[dict[str, str]] | None = None,
        temperature: float | None = None,
        response_format: ResponseFormat | str | None = None,
        request_usage: bool = False,
        **kwargs: Any,
    ) -> AsyncGenerator[str | dict[str, Any], None]: ...
    async def llm_chat_beta(
        self: DelosClient,
        model: str,
        messages: list[dict[str, str]] | None = None,
        temperature: float | None = None,
        response_format: ResponseFormat | str | None = None,
        stream: bool = False,
        request_usage: bool = False,
        text: str | None = None,  # deprecated
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncGenerator[str | dict[str, Any], None]: ...
    def llm_embed(self, text: str, model: str) -> dict[str, Any] | None: ...
