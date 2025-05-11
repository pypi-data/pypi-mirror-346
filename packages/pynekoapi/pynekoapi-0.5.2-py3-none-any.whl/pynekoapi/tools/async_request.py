import contextlib
from typing import Any, Dict

from httpx import AsyncClient, Timeout


class AsyncRequest(AsyncClient):

    def __init__(self, timeout: int = 30) -> None:
        super().__init__(
            http2=True,
            verify=False,
            headers={
                "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",  # noqa: E501
            },
            timeout=Timeout(timeout),
        )

    async def _get(self, *args: Any, **kwargs: Any) -> Dict[Any, Any]:
        with contextlib.suppress(Exception):
            response = await self.get(*args, **kwargs)
            return response.josn()

        return {"ok": False, "error": "Contact the owner for repair @excute7."}

    async def _post(self, *args: Any, **kwargs: Any) -> Dict[Any, Any]:
        with contextlib.suppress(Exception):
            response = await self.post(*args, **kwargs)
            return response.json()

        return {"ok": False, "error": "Contact the owner for repair @excute7."}
