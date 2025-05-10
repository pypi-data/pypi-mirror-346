"""Client for interacting with the Delos API."""

import json
import warnings
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import IO, Annotated, Any, Callable, Literal, cast

import aiohttp
import requests
from pydantic import BaseModel, PrivateAttr

from .endpoints import Endpoints, RequestMethod
from .exceptions import APIKeyMissingError
from .models import ResponseFormat
from .releases import AllReleases
from .settings import VerboseLevel, delos_logger
from .utils import load_file, load_files

DELOS_PLATFORM_BACKEND_URL = "https://api.delos.so"


class APIClient(BaseModel):
    """Base class for API clients."""

    api_key: str
    _server_url: str = PrivateAttr()
    _verbose: VerboseLevel = PrivateAttr()
    _session: requests.Session = PrivateAttr()
    _client_version: Any = PrivateAttr()

    class Config:
        """Configuration for the API Clients."""

        arbitrary_types_allowed = True

    def __init__(
        self: "APIClient",
        api_key: str,
        server_url: str = DELOS_PLATFORM_BACKEND_URL,
        verbose: int | VerboseLevel = VerboseLevel.INFO,
    ) -> None:
        """Initialize the client with the server URL and API key.

        Args:
            api_key: The API key to be used for requests.
            server_url: The URL of the server.
            verbose: The verbosity level of the client.
                0 - No logging
                1 - Only print the requests (default)
                2 - Print the requests and the response

        """
        super().__init__(api_key=api_key)
        if not api_key:
            raise APIKeyMissingError

        self._server_url = server_url
        self._verbose = VerboseLevel(verbose) if isinstance(verbose, int) else verbose
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        self._client_version = AllReleases[0]

        # Inner client logger
        self._logger_id = f"{__name__}.{id(self)}"
        self._logger = delos_logger.bind(client_id=self._logger_id)

        # Disable logger if verbose is NONE
        if self._verbose == VerboseLevel.NONE:
            delos_logger.disable(self._logger_id)

    @property
    def server_url(self) -> str:
        """Get the server URL."""
        return self._server_url

    @property
    def verbose(self) -> VerboseLevel:
        """Get the verbosity level."""
        return self._verbose

    def _log(self, message: str, level: int = VerboseLevel.INFO) -> None:
        """Log internal client messages based on verbosity setting.

        Args:
            message: The message to log.
            level: The verbosity level of the message.

        """
        if self._verbose >= level:
            if level == VerboseLevel.DEBUG:
                self._logger.debug(message)
            elif level == VerboseLevel.INFO:
                self._logger.info(message)

    def _build_request(
        self: "APIClient",
        endpoint: tuple[str, RequestMethod],
        data: dict[str, Any] | None = None,
        files: Any = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, Callable[..., requests.Response], dict[str, Any]]:
        """Prepare the request by setting up the URL, request function, and request arguments.

        Args:
            endpoint: A tuple containing the endpoint URL and the request type.
            data: The data to be sent in the request body (default is None).
            files: The files to be sent in the request (default is None).
            params: The query parameters to be sent in the request (default is None).
            kwargs: Specific keyword arguments to be passed to the request function.

        Returns:
            A tuple containing the URL, request function, and prepared request arguments.

        """
        url = f"{self.server_url}{self._client_version.suffix}{endpoint[0]}"
        request_method = endpoint[1]

        request_func = cast(
            "Callable[..., requests.Response] | None",
            {
                RequestMethod.GET: self._session.get,
                RequestMethod.POST: self._session.post,
                RequestMethod.PUT: self._session.put,
                RequestMethod.DELETE: self._session.delete,
            }.get(request_method),
        )

        if not request_func:
            unsupported_method_error = f"Unsupported HTTP method: {request_method}"
            self._log(unsupported_method_error, level=VerboseLevel.DEBUG)
            raise ValueError(unsupported_method_error)

        files_details = [name for (param, (name, content)) in files] if files else ""
        files_message = f"{len(files)} Files: {files_details}" if files else "No files"

        self._log(f"Request URL: {url}", VerboseLevel.DEBUG)
        self._log(f"Request Method: {request_method}", VerboseLevel.DEBUG)
        self._log(f"Request Data: {data}", VerboseLevel.DEBUG)
        self._log(f"Request Files: {files_message}", VerboseLevel.DEBUG)
        self._log(f"Request Params: {params}", VerboseLevel.DEBUG)

        form_data = {}
        if data:
            form_data.update({k: str(v) if v is not None else "" for k, v in data.items()})

        request_args = {
            "data": form_data,
            "files": files,
            "params": params,
            **kwargs,
        }

        return url, request_func, request_args

    def _build_async_request(
        self: "APIClient",
        endpoint: tuple[str, RequestMethod],
        data: dict[str, Any] | None = None,
        files: Any = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, Callable[..., Any], dict[str, Any]]:
        """Prepare the request by setting up the URL, request function, and request arguments.

        Args:
            endpoint: A tuple containing the endpoint URL and the request type.
            data: The data to be sent in the request body (default is None).
            files: The files to be sent in the request (default is None).
            params: The query parameters to be sent in the request (default is None).
            kwargs: Specific keyword arguments to be passed to the request function.

        Returns:
            A tuple containing the URL, request function, and prepared request arguments.

        """
        url = f"{self.server_url}{self._client_version.suffix}{endpoint[0]}"
        request_method = endpoint[1]

        request_func = getattr(aiohttp.ClientSession(), request_method.lower(), None)

        if not request_func:
            unsupported_method_error = f"Unsupported HTTP method: {request_method}"
            self._log(unsupported_method_error, level=VerboseLevel.DEBUG)
            raise ValueError(unsupported_method_error)

        files_details = [name for (param, (name, content)) in files] if files else ""
        files_message = f"{len(files_details)} Files: {files_details}" if files else "No files"

        self._log(f"Request URL: {url}", VerboseLevel.DEBUG)
        self._log(f"Request Method: {request_method}", VerboseLevel.DEBUG)
        self._log(f"Request Data: {data}", VerboseLevel.DEBUG)
        self._log(f"Request Files: {files_message}", VerboseLevel.DEBUG)
        self._log(f"Request Params: {params}", VerboseLevel.DEBUG)

        headers = {"Authorization": f"Bearer {self.api_key}"}

        request_args = {
            "headers": headers,
            "data": data,
            "params": params,
            **kwargs,
        }

        if files:
            form_data = aiohttp.FormData()
            for param, (name, content) in files:
                form_data.add_field(param, content, filename=name)
            request_args["data"] = form_data

        return url, request_func, request_args

    def _make_request(
        self: "APIClient",
        endpoint: tuple[str, RequestMethod],
        data: dict[str, Any] | None = None,
        files: Any = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        """Make a request to the specified endpoint with the given data and files.

        Args:
            api_key: The Delos key to be used for the request.
            endpoint: A tuple containing the endpoint URL and the request type.
            data: The data to be sent in the request body (default is None).
            files: The files to be sent in the request (default is None).
            params: The query parameters to be sent in the request (default is None).
            kwargs: Specific keyword arguments to be passed to the request function.

        Returns:
            The response from the request as a dictionary, or None if an error occurred.

        """
        url, request_func, request_args = self._build_request(endpoint, data, files, params, **kwargs)

        try:
            response = request_func(url, **request_args)
            response.raise_for_status()

            if self.verbose >= VerboseLevel.INFO:
                self._log(f"Response: {response.json()}", VerboseLevel.INFO)
            return response.json()

        except requests.exceptions.RequestException:
            error_message = f"Request to {url} failed"
            self._logger.exception(error_message)
            raise

    async def _make_streaming_request(
        self: "APIClient",
        endpoint: tuple[str, RequestMethod],
        data: dict[str, Any] | None = None,
        files: Any = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[str | dict[str, Any], None]:
        """Make a request to the specified streaming endpoint with the given data and files.

        Args:
            api_key: The Delos key linked to this client.
            endpoint: A tuple containing the endpoint URL and the request type.
            data: The data to be sent in the request body (default is None).
            files: The files to be sent in the request (default is None).
            params: The query parameters to be sent in the request (default is None).
            kwargs: Specific keyword arguments to be passed to the request function.

        Returns:
            The streaming response from the request.

        """
        if endpoint[1] != RequestMethod.POST:
            streaming_error_message = "Streaming is only supported for POST requests."
            self._logger.warning(streaming_error_message)
            raise ValueError(streaming_error_message)

        url, _request_func, request_args = self._build_async_request(endpoint, data, files, params, **kwargs)

        session = aiohttp.ClientSession()
        try:
            # Create the session separately so we can ensure it's closed
            async with session.post(url, **request_args) as response:
                response.raise_for_status()
                async for line in response.content.iter_any():
                    decoded_line = line.decode("utf-8").strip()
                    if decoded_line:
                        yield decoded_line

            if self._verbose >= VerboseLevel.INFO:
                self._log("Streaming completed", VerboseLevel.INFO)

        except aiohttp.ClientError:
            error_message = f"Request to {url} (streaming) failed"
            self._logger.exception(error_message)
            raise

        finally:
            await session.close()
            if self._verbose >= VerboseLevel.INFO:
                self._log("Session closed", VerboseLevel.INFO)


class IndexClient(APIClient):
    """Client for interacting with the Delos Index API.

    Attributes:
        server_url: The URL of the server.
        api_key: The API key to be used for requests.

    """

    def __init__(
        self,
        api_key: str,
        server_url: str = DELOS_PLATFORM_BACKEND_URL,
        verbose: VerboseLevel = VerboseLevel.INFO,
    ) -> None:
        """Initialize the DelosClient.

        Args:
            api_key: The Delos key linked to this client.
            server_url: The URL of the server.
            verbose: The verbosity level of the client.

        """
        super().__init__(api_key=api_key, server_url=server_url, verbose=verbose)

    def files_index_create(
        self: "IndexClient",
        name: str,
        read_images: bool = False,
        filepaths: list[Path] | list[str] | None = None,
        fileobjects: list[tuple[str, IO[bytes]]] | None = None,
        filesobjects: Annotated[
            list[tuple[str, IO[bytes]]] | None,
            "Deprecated: Use `fileobjects` (without intermediate S) instead",
        ] = None,
        tags_index: list[str] | None = None,
        tags_files: list[str] | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to create an index.

        Args:
            name: The name of the index.
            read_images: Whether to read images from the files (Optional). Default is False.

            filepaths: A list of file paths to be indexed. Provide either `filepaths` or `fileobjects`, not both.
            fileobjects: A list of file objects to be indexed.
            filesobjects: Old name ("fileSobjects", new is "fileobjects") - SOON TO BE DEPRECATED.
            tags_index: A list of tags to be enabled for the index. Used for automatic files tagging.
            tags_files: A list of tags to be assigned to the files uploaded in this request.
                Used as filters when querying `.files_index_ask`.

        Returns:
            The server response.

        """
        if filesobjects:
            deprecation_warning = (
                "The parameter `filesobjects` has been renamed. Old parameter name soon will be deprecated. "
                "Use parameter `fileobjects` (instead of `fileSobjects`)'"
            )
            self._logger.warning(deprecation_warning)
            warnings.warn(
                deprecation_warning,
                DeprecationWarning,
                stacklevel=2,
            )
            fileobjects = filesobjects

        if (filepaths is None and fileobjects is None) or (filepaths is not None and fileobjects is not None):
            warning_message = "Provide only `filepaths` or `fileobjects`, not both or neither."
            raise ValueError(warning_message)

        return self._make_request(
            Endpoints.FILES.INDEX_CREATE.value,
            data={"name": name, "read_images": read_images, "tags_index": tags_index, "tags_files": tags_files},
            files=load_files(filepaths, fileobjects),
        )

    def files_index_files_add(
        self: "IndexClient",
        index_uuid: str,
        read_images: bool = False,
        filepaths: list[Path] | list[str] | None = None,
        fileobjects: list[tuple[str, IO[bytes]]] | None = None,
        filesobjects: Annotated[
            list[tuple[str, IO[bytes]]] | None,
            "Deprecated: Use `fileobjects` (without intermediate S) instead",
        ] = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to add files to an index.

        Args:
            index_uuid: The index UUID.
            read_images: Whether to read images from the files (Optional). Default is False.

            filepaths: A list of file paths to be added to the index.
            fileobjects: A list of file objects to be indexed. Provide either `filepaths` or `fileobjects`, not both.
            filesobjects: Old name ("fileSobjects", new is "fileobjects") - SOON TO BE DEPRECATED.
            tags: A list of tags to be applied to ALL FILES in this operation.

        Returns:
            The server response.

        """
        if filesobjects:
            deprecation_warning = (
                "The parameter `filesobjects` has been renamed. Old parameter name soon will be deprecated. "
                "Use parameter `fileobjects` (instead of `fileSobjects`)'"
            )
            self._logger.warning(deprecation_warning)
            warnings.warn(
                deprecation_warning,
                DeprecationWarning,
                stacklevel=2,
            )
            fileobjects = filesobjects

        if (filepaths is None and fileobjects is None) or (filepaths is not None and fileobjects is not None):
            warning_message = "Provide only `filepaths` or `fileobjects`, not both or neither."
            raise ValueError(warning_message)

        return self._make_request(
            Endpoints.FILES.INDEX_ADD_FILES.value,
            data={"index_uuid": index_uuid, "read_images": read_images, "tags": tags},
            files=load_files(filepaths, fileobjects),
        )

    def files_index_retry(
        self,
        index_uuid: str,
        read_images: bool = False,
        tags: list[str] | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to retry files from an index.

        Args:
            index_uuid: The index UUID.
            read_images: Whether to read images from the files (Optional). Default is False.
            tags: A list of tags to be applied to ALL FILES in this operation.

        Returns:
            The server response.

        """
        if tags is None:
            tags = []

        return self._make_request(
            Endpoints.FILES.INDEX_RETRY_FILES.value,
            data={"index_uuid": index_uuid, "read_images": read_images, "tags": tags},
        )

    def files_index_files_delete(
        self: "IndexClient",
        index_uuid: str,
        files_hashes: list[str],
    ) -> dict[str, Any] | None:
        """Make a request to delete files from an index.

        Args:
            index_uuid: The index UUID.
            files_hashes: A list of file hashes to be deleted from the index.

        Returns:
            The server response.

        """
        debug_message = (
            f"{len(files_hashes)} Files to be deleted: {files_hashes} (type {type(files_hashes)} "
            f"- first item:{files_hashes[0]} ({type(files_hashes[0])}))"
        )
        self._logger.warning(debug_message)
        files_hashes_str = [str(file_hash) for file_hash in files_hashes]
        data = {"index_uuid": index_uuid, "files_hashes": files_hashes_str}
        return self._make_request(Endpoints.FILES.INDEX_DELETE_FILES.value, data=data)

    def files_index_delete(self: "IndexClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to delete an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_DELETE.value, data=data)

    def files_index_restore(self: "IndexClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to restore an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_RESTORE.value, data=data)

    def files_index_rename(
        self: "IndexClient",
        index_uuid: str,
        name: str,
    ) -> dict[str, Any] | None:
        """Make a request to rename an index.

        Args:
            index_uuid: The index UUID.
            name: The new name for the index.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid, "name": name}
        return self._make_request(Endpoints.FILES.INDEX_RENAME.value, data=data)

    def files_index_ask(
        self: "IndexClient",
        index_uuid: str,
        question: str,
        output_language: str | None = None,
        active_files: list[str] | str | None = None,
        tags: list[str] | None = None,
        instructions: str | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to ask a question about the index contents.

        Args:
            index_uuid: The index UUID.
            question: The question to be asked.
            output_language: The output language for the question.
            active_files: The file_id of the files to be used for the question.
            tags: Subset of files to be used in this research (when not provided, all tags are enabled).
            instructions: Instructions for the LLM formatting and answer.

        Returns:
            The server response.

        """
        data = {
            "index_uuid": str(index_uuid),
            "question": question,
            "active_files": json.dumps(active_files) if isinstance(active_files, list) else active_files,
        }
        if output_language:
            data["output_language"] = output_language
        if tags:
            data["tags"] = json.dumps(tags) if isinstance(tags, list) else tags
        if instructions:
            data["instructions"] = instructions

        return self._make_request(Endpoints.FILES.INDEX_ASK.value, data=data)

    def files_index_embed(self: "IndexClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to embed an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        data = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_EMBED.value, data=data)

    def files_index_details(self: "IndexClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to get details of an index.

        Args:
            index_uuid: The index UUID.

        Returns:
            The server response.

        """
        params = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES.INDEX_DETAILS.value, params=params)

    def files_index_list(self: "IndexClient") -> dict[str, Any] | None:
        """Make a request to list all indexes."""
        return self._make_request(Endpoints.FILES.INDEX_LIST.value)

    def files_index_tags_get(self: "IndexClient", index_uuid: str) -> dict[str, Any] | None:
        """Make a request to get the tags of a given index."""
        params = {"index_uuid": index_uuid}
        return self._make_request(Endpoints.FILES_TAGS.INDEX_GET_TAGS.value, params=params)

    def files_index_tags_update(
        self: "IndexClient",
        index_uuid: str,
        tags: list[str],
    ) -> dict[str, Any] | None:
        """Make a request to update the tags of a given index."""
        data = {"index_uuid": index_uuid, "tags": tags}
        return self._make_request(Endpoints.FILES_TAGS.INDEX_UPDATE_TAGS.value, data=data)

    def files_index_files_tags_update(
        self: "IndexClient",
        index_uuid: str,
        files_uuids: str | list[str],
        tags: list[str],
    ) -> dict[str, Any] | None:
        """Make a request to update the tags of a given file."""
        data = {"index_uuid": index_uuid, "files_ids": files_uuids, "tags": tags}
        return self._make_request(Endpoints.FILES_TAGS.INDEX_UPDATE_FILE_TAGS.value, data=data)


class DelosClient(IndexClient):
    """Client for interacting with the Delos API.

    Attributes:
        server_url: The URL of the server.
        api_key: The API key to be used for requests.

    """

    def __init__(
        self,
        api_key: str,
        server_url: str = DELOS_PLATFORM_BACKEND_URL,
        verbose: VerboseLevel = VerboseLevel.INFO,
    ) -> None:
        """Initialize the DelosClient.

        Args:
            api_key: The Delos key linked to this client.
            server_url: The URL of the server.
            verbose: The verbosity level of the client.

        """
        super().__init__(api_key=api_key, server_url=server_url, verbose=verbose)

    def status_health(
        self: "DelosClient",
    ) -> dict[str, Any] | None:
        """Make a request to check the health of the server."""
        return self._make_request(Endpoints.STATUS.HEALTH.value)

    def translate_text(
        self: "DelosClient",
        text: str,
        output_language: str,
        input_language: str | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to translate text.

        Args:
            text: The text to be translated.
            output_language: The output language for the translation.
            input_language: The input language for the translation (Optional).

        Returns:
            The server response.

        """
        data = {
            "text": text,
            "output_language": output_language,
        }
        if input_language:
            data["input_language"] = input_language
        return self._make_request(endpoint=Endpoints.TRANSLATE.TRANSLATE_TEXT.value, data=data)

    def translate_file(
        self: "DelosClient",
        output_language: str,
        input_language: str | None = None,
        return_type: Literal["raw_text", "url", "file"] = "raw_text",
        filepath: Path | str | None = None,
        fileobject: tuple[str, IO[bytes]] | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to translate a file.

        Args:
            output_language: The output language for the translation.
            input_language: The input language for the translation (Optional).
            return_type: The type of return for the translation (Optional). Default is "raw_text".

            filepath: The file path to be translated.
            fileobject: The file object to be translated. Provide either filepath or fileobject, not both.

        Returns:
            The server response.

        """
        files = load_file(filepath, fileobject)
        data = {
            "output_language": output_language,
            "return_type": return_type,
        }
        if input_language:
            data["input_language"] = input_language

        return self._make_request(Endpoints.TRANSLATE.TRANSLATE_FILE.value, data=data, files=files)

    def web_search(
        self: "DelosClient",
        text: str,
        output_language: str | None = None,
        desired_urls: list[str] | str | None = None,
    ) -> dict[str, Any] | None:
        """Make a request to perform a search.

        Args:
            text: The text to be searched.
            output_language: The output language for the search (Optional).
            desired_urls: The desired URLs to be priviledged in the search (Optional).

        Returns:
            The server response.

        """
        data = {"text": text}
        if output_language:
            data["output_language"] = output_language
        if desired_urls:
            data["desired_urls"] = str(desired_urls)

        return self._make_request(Endpoints.WEB.SEARCH.value, data)

    async def llm_chat_beta(
        self: "DelosClient",
        model: str,
        messages: list[dict[str, str]] | None = None,
        temperature: float | None = None,
        response_format: ResponseFormat | str | None = None,
        stream: bool = False,
        request_usage: bool = False,
        text: str | None = None,  # deprecated
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncGenerator[str | dict[str, Any], None] | None:
        """Make a request to chat with the LLM.

        Args:
            text: The text to be chatted.
            messages: The history of the conversation (Optional. Default is None).
            model: The model to be used for chatting.
            temperature: The temperature for the chat (Optional. Default is 0.7).
            response_format: The response format for the chat (Optional).
                For example: `response_format = {"type":"json_object"}`
            stream: Whether to stream the response or not.
            request_usage: Whether to request usage for the request or not.
            kwargs: Other specific keyword arguments to be passed to the request function.

        Returns:
            The server response.

        """
        if messages is None and text is None:
            missing_message = "Either `messages` or `text` must be provided. Note that `text` will be deprecated soon."
            raise ValueError(missing_message)

        messages_list = messages or []
        deprecated_text_message = (
            "The parameter `text:str`, soon will be deprecated. "
            "Send your message in the list of `messages:list[dict[str,str]]`, following the message format:"
            "`message: dict[str,str] = {'role':'user', 'content':text_content}`."
        )

        if not messages:
            self._logger.warning("List of `messages` will soon be required (`text` parameter deprecated).")

        if text or not messages:
            self._logger.warning(deprecated_text_message)
            warnings.warn(
                deprecated_text_message,
                DeprecationWarning,
                stacklevel=2,
            )
            if text is not None:
                messages_list.append({"role": "user", "content": text})

        data = {"model": model, "stream": stream, "request_usage": request_usage}
        data["messages"] = str(messages_list)

        if response_format is not None:
            if isinstance(response_format, str):
                warning_message = (
                    "The parameter `response_format:str`, soon will be deprecated. "
                    "Use instead `response_format:dict[str, Any]` which must contain a `type` key. For example: "
                    '`response_format={"type":"json_object"}` or `response_format={"type":"text"}`.'
                )
                self._logger.warning(warning_message)
                warnings.warn(
                    warning_message,
                    DeprecationWarning,
                    stacklevel=2,
                )
                data["response_format"] = response_format

            else:
                parsed_format = json.dumps(response_format)
                data["response_format"] = parsed_format

        if temperature is not None:
            data["temperature"] = str(temperature)

        data.update(kwargs)

        if stream:
            return self._make_streaming_request(endpoint=Endpoints.LLM.CHAT_BETA.value, data=data)
        return self._make_request(endpoint=Endpoints.LLM.CHAT_BETA.value, data=data)

    def llm_chat(
        self: "DelosClient",
        text: str,
        model: str,
        messages: list[dict[str, str]] | None = None,
        temperature: float | None = None,
        response_format: ResponseFormat | str | None = None,  # str: deprecated
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        """Make a request to chat with the LLM.

        Args:
            text: The text to be chatted.
            messages: The history of the conversation (Optional. Default is None).
            model: The model to be used for chatting.
            temperature: The temperature for the chat (Optional. Default is 0.7).
            response_format: The response format for the chat (Optional).
                For example: `response_format = {"type":"json_object"}`
            kwargs: Other specific keyword arguments to be passed to the request function.

        Returns:
            The server response.

        """
        data = {"text": text, "model": model}
        if messages is not None:
            data["messages"] = str(messages)
        if response_format is not None:
            if isinstance(response_format, str):
                warning_message = (
                    "The parameter `response_format:str`, soon will be deprecated. "
                    "Use instead `response_format:dict[str, Any]` which must contain a `type` key. For example: "
                    '`response_format={"type":"json_object"}` or `response_format={"type":"text"}`.'
                )
                self._logger.warning(warning_message)
                warnings.warn(
                    warning_message,
                    DeprecationWarning,
                    stacklevel=2,
                )
                data["response_format"] = response_format

            else:
                parsed_format = json.dumps(response_format)
                data["response_format"] = parsed_format

        if temperature is not None:
            data["temperature"] = str(temperature)

        data.update(kwargs)
        return self._make_request(endpoint=Endpoints.LLM.CHAT.value, data=data)

    async def llm_chat_stream(
        self: "DelosClient",
        text: str,
        model: str,
        messages: list[dict[str, str]] | None = None,
        temperature: float | None = None,
        request_usage: bool = False,
        response_format: ResponseFormat | str | None = None,  # str: deprecated
        **kwargs: Any,
    ) -> AsyncGenerator[str | dict[str, Any], None]:
        """Make a streaming request to chat with the LLM.

        Args:
            text: The text to be chatted.
            model: The model to be used for chatting.
            messages: The history of the conversation (Optional. Default is None).
            temperature: The temperature for the chat (Optional. Default is 0.7).
            response_format: The response format for the chat (Optional).
                For example: `response_format = {"type":"json_object"}`
            request_usage: Whether to request usage for the request or not.
            kwargs: Other specific keyword arguments to be passed to the request function.

        Returns:
            The server response.

        """
        data = {"text": text, "model": model, "request_usage": request_usage}
        if messages is not None:
            data["messages"] = str(messages)

        if response_format is not None:
            if isinstance(response_format, str):
                self._logger.warning(
                    "The parameter `response_format:str`, soon will be deprecated. "
                    "Use instead `response_format:dict[str, Any]` which must contain a `type` key. For example: "
                    '`response_format={"type":"json_object"}` or `response_format={"type":"text"}`.',
                )
                data["response_format"] = response_format
            else:
                data["response_format"] = str(response_format)

        if temperature is not None:
            data["temperature"] = str(temperature)

        data.update(kwargs)

        stream = self._make_streaming_request(endpoint=Endpoints.LLM.CHAT_STREAM.value, data=data)
        async for chunk in stream:
            yield chunk

    def llm_embed(
        self: "DelosClient",
        text: str,
        model: str,
    ) -> dict[str, Any] | None:
        """Make a request to embed data using the LLM.

        Args:
            text: The text to be embedded.
            model: The model to use for embedding.

        Returns:
            The server response.

        """
        return self._make_request(Endpoints.LLM.EMBED.value, data={"text": text, "model": model})
