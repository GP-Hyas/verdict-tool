import os
import httpx
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Any, Dict

load_dotenv()


@dataclass
class Endpoints:
    base_url: str

    @property
    def verdict(self) -> str:
        return f"{self.base_url}/decision/verdict"


class APIClient:
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url
        self.key = os.getenv("APIKEY")
        self.clientid = os.getenv("CLIENTID")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-API-Key": self.key,
        }
        self.endpoints = Endpoints(base_url=self.base_url)
        self.timeout = timeout

    async def __aenter__(self):
        self.client = httpx.AsyncClient(headers=self.headers, timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"Exception occurred: {exc_type} - {exc_value}")
        await self.client.aclose()

    async def _make_request(
        self, method: str, url: str, payload: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        try:
            response = await self.client.request(method, url, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            print(f"Request error: {exc}")
            return {"error": str(exc)}
        except httpx.HTTPStatusError as exc:
            print(f"HTTP error: {exc.response.status_code}: {exc.response.text}")
            return {"error": exc.response.text}

    async def verdict(self, domain: str) -> Dict[str, Any]:
        payload = {"clientId": self.clientid, "domain": domain}
        return await self._make_request("POST", self.endpoints.verdict, payload=payload)
