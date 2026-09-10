import httpx


BACKEND_URL = "http://localhost:8000/api/v1"


class AuthManager:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=BACKEND_URL
        )

        self.access_token: str | None = None

    async def login(self, email: str, password: str) -> None:
        response = await self.client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        response.raise_for_status()

        data = response.json()

        self.access_token = data["data"]["access_token"]

    async def refresh(self) -> None:
        response = await self.client.post(
            "/auth/refresh"
        )

        response.raise_for_status()

        data = response.json()

        self.access_token = data["data"]["access_token"]

    async def request(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> httpx.Response:

        if self.access_token is None:
            raise RuntimeError("Not authenticated")

        headers = kwargs.pop("headers", {})

        headers["Authorization"] = (
            f"Bearer {self.access_token}"
        )

        response = await self.client.request(
            method,
            url,
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
            url,
            headers=headers,
            **kwargs,
        )

    async def close(self) -> None:
        await self.client.aclose()