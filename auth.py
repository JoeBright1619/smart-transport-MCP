import os

import httpx
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "http://localhost:8000/api/v1"
AUTH_BASE_URL = "http://localhost:8000"


class AuthManager:
    def __init__(self):
        self.client: httpx.AsyncClient | None = None
        self.access_token: str | None = None

    async def start(self) -> None:
        self.client = httpx.AsyncClient()

        await self.login_from_environment()

    async def login(self, email: str, password: str) -> None:
        if self.client is None:
            raise RuntimeError("AuthManager has not been started")

        response = await self.client.post(
            f"{AUTH_BASE_URL}/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        response.raise_for_status()

        data = response.json()

        self.access_token = data["data"]["accessToken"]

    async def refresh(self) -> None:
        if self.client is None:
            raise RuntimeError("AuthManager has not been started")

        response = await self.client.post(
            f"{AUTH_BASE_URL}/auth/refresh"
        )

        response.raise_for_status()

        data = response.json()

        self.access_token = data["data"]["accessToken"]

    async def request(
        self,
        method: str,
        url: str,
        *,
        base_url: str = API_BASE_URL,
        **kwargs,
    ) -> httpx.Response:

        if self.client is None:
            raise RuntimeError("AuthManager has not been started")

        if self.access_token is None:
            raise RuntimeError("Not authenticated")

        headers = dict(kwargs.pop("headers", {}))

        headers["Authorization"] = (
            f"Bearer {self.access_token}"
        )

        response = await self.client.request(
            method,
            f"{base_url}{url}",
            headers=headers,
            **kwargs,
        )

        if response.status_code != 401:
            return response

        await self.refresh()

        headers["Authorization"] = (
            f"Bearer {self.access_token}"
        )

        return await self.client.request(
            method,
            f"{base_url}{url}",
            headers=headers,
            **kwargs,
        )
    async def login_from_environment(self) -> None:
        email = os.getenv("SMART_TRANSPORT_EMAIL")
        password = os.getenv("SMART_TRANSPORT_PASSWORD")

        if not email or not password:
            raise RuntimeError(
                "SMART_TRANSPORT_EMAIL and "
                "SMART_TRANSPORT_PASSWORD must be set"
            )

        await self.login(email, password)

    async def close(self) -> None:
        if self.client is not None:
            await self.client.aclose()
            self.client = None