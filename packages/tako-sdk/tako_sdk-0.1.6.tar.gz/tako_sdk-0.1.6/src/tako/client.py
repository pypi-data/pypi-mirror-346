from typing import List, Optional
import requests
import httpx

from tako.types.common.exceptions import raise_exception_from_response
from tako.types.knowledge_search.types import (
    KnowledgeSearchResults,
    KnowledgeSearchSourceIndex,
)

DEFAULT_SERVER_URL = "https://trytako.com/"
DEFAULT_API_VERSION = "v1"


class TakoClient:
    def __init__(
        self,
        api_key: str,
        server_url: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        assert api_key is not None, "API key is required"
        self.api_key = api_key
        self.server_url = server_url or DEFAULT_SERVER_URL
        self.api_version = api_version or DEFAULT_API_VERSION

    def knowledge_search(
        self,
        text: str,
        source_indexes: Optional[List[KnowledgeSearchSourceIndex]] = None,
    ) -> KnowledgeSearchResults:
        """
        Search for knowledge cards based on a text query.

        Args:
            text: The text to search for.
            source_indexes: The source indexes to search for.

        Returns:
            A list of knowledge search results.

        Raises:
            APIException: If the API returns an error.
        """
        url = f"{self.server_url}/api/{self.api_version}/knowledge_search"
        payload = {
            "inputs": {
                "text": text,
            },
        }
        if source_indexes:
            payload["source_indexes"] = source_indexes

        response = requests.post(
            url, json=payload, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        raise_exception_from_response(response)

        return KnowledgeSearchResults.model_validate(response.json())

    def get_image(self, card_id: str) -> bytes:
        """
        Get an image for a knowledge card.

        Args:
            card_id: The ID of the knowledge card.

        Returns:
            The image as bytes.
        """
        url = f"{self.server_url}/api/{self.api_version}/image/{card_id}/"
        response = requests.get(
            url,
            headers={
                "Accept": "image/*",
            },
        )
        return response.content


class AsyncTakoClient:
    def __init__(
        self,
        api_key: str,
        server_url: Optional[str] = None,
        api_version: Optional[str] = None,
        default_timeout_seconds: Optional[float] = 30.0,
    ):
        assert api_key is not None, "API key is required"
        self.api_key = api_key
        self.server_url = (server_url or DEFAULT_SERVER_URL).strip("/")
        self.api_version = api_version or DEFAULT_API_VERSION
        self.default_timeout_seconds = default_timeout_seconds

    async def knowledge_search(
        self,
        text: str,
        source_indexes: Optional[List[KnowledgeSearchSourceIndex]] = None,
        timeout_seconds: Optional[float] = None,
    ) -> KnowledgeSearchResults:
        """
        Async search for knowledge cards based on a text query.

        Args:
            text: The text to search for.
            source_indexes: The source indexes to search for.

        Returns:
            A list of knowledge search results.

        Raises:
            APIException: If the API returns an error.
        """
        # Trailing slash is required for httpx
        url = f"{self.server_url}/api/{self.api_version}/knowledge_search/"
        payload = {
            "inputs": {
                "text": text,
            },
        }
        if source_indexes:
            payload["source_indexes"] = source_indexes

        async with httpx.AsyncClient(
            timeout=timeout_seconds or self.default_timeout_seconds
        ) as client:
            response = await client.post(
                url, json=payload, headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return KnowledgeSearchResults.model_validate(response.json())

    async def get_image(
        self, card_id: str, timeout_seconds: Optional[float] = None
    ) -> bytes:
        """
        Async get an image for a knowledge card.

        Args:
            card_id: The ID of the knowledge card.

        Returns:
            The image as bytes.
        """
        # Trailing slash is required for httpx
        url = f"{self.server_url}/api/{self.api_version}/image/{card_id}/"
        async with httpx.AsyncClient(
            timeout=timeout_seconds or self.default_timeout_seconds
        ) as client:
            response = await client.get(
                url,
                headers={
                    "Accept": "image/*",
                },
            )
            return response.content
