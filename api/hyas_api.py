import os
import httpx
import asyncio
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Any, Dict, Optional
from utils.logger_config import logger

# Load environment variables
load_dotenv()


# Custom exception for API errors
class APIERROR(Exception):
    """Custom exception for API-related errors."""

    pass


@dataclass(frozen=True)
class Endpoints:
    """Dataclass to manage API endpoints."""

    base_url: str

    @property
    def verdict(self) -> str:
        """Return the URL for the verdict endpoint."""
        return f"{self.base_url}/decision/verdict"


class APIClient:
    """HTTP client to interact with the Verdict API."""

    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url
        self.key = self._get_env_var("APIKEY")
        self.clientid = self._get_env_var("CLIENTID")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-API-Key": self.key,
        }
        self.endpoints = Endpoints(base_url=self.base_url)
        self.timeout = timeout

    @staticmethod
    def _get_env_var(var_name: str) -> str:
        """Retrieve environment variable and validate its presence"""
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"Environment variable '{var_name}' is not set.")
        return value

    async def __aenter__(self) -> "APIClient":
        """Async context manager entry: initialize the HTTPX client"""
        self.client = httpx.AsyncClient(headers=self.headers, timeout=self.timeout)
        logger.info("Initialized API client.")
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        """Async context manager exit: close the HTTPX client."""
        if exc_type:
            logger.error(f"Exception occurred: {exc_type} - {exc_value}")
        await self.client.aclose()
        logger.info("Closed API client.")

    async def _make_request(
        self,
        method: str,
        url: str,
        payload: Optional[Dict[str, Any]] = None,
        retries: int = 3,
    ) -> Dict[str, Any]:
        """Helper method to make an HTTP request."""
        for attempt in range(1, retries + 1):
            try:
                if attempt > 1:
                    logger.debug(
                        f"Retrying... Attempt {attempt}/{retries} for {payload['domain']}"
                    )
                response = await self.client.request(method, url, json=payload)
                response.raise_for_status()
                return response.json()

            except httpx.RequestError as exc:
                if attempt == retries:
                    logger.error(
                        f"Failed to process {payload.get('domain', 'N/A')} "
                        f"after {retries} attempts. Error: {exc}"
                    )
                else:
                    logger.debug(f"Network error: {exc} (Retrying...)")
                await asyncio.sleep(2)  # Wait before retry

            except Exception as exc:
                logger.error(
                    f"Unexpected error for {payload.get('domain', 'N/A')}: {exc}"
                )
                break

        return {
            "error": "Request Failed",
            "message": f"Max retries ({retries}) reached",
            "url": url,
            "domain": payload.get("domain") if payload else "N/A",
        }

    async def verdict(self, domain: str) -> Dict[str, Any]:
        """
        Fetch the verdict for a given domain.

        Args:
            domain (str): The domain to query.

        Returns:
            Dict[str, Any]: The API response.
        """
        payload = {"clientId": self.clientid, "domain": domain}
        logger.info(f"Fetching verdict for domain: {domain}")
        return await self._make_request("POST", self.endpoints.verdict, payload=payload)
