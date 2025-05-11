import contextlib
from typing import Any, Dict

import requests


class SyncRequest:

    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout
        self.fetch = requests

    def _get(self, url: str, *args: Any, **kwargs: Any) -> Dict[Any, Any]:
        with contextlib.suppress(Exception):
            response = self.fetch.get(url=url, timeout=self.timeout, *args, **kwargs)
            return response.json()

        return {"ok": True, "error": "Contact the owner for repair @excute7."}

    def _post(self, url: str, *args: Any, **kwargs: Any) -> Dict[Any, Any]:
        with contextlib.suppress(Exception):
            response = self.fetch.get(url=url, timeout=self.timeout, *args, **kwargs)
            return response.json()

        return {"ok": True, "error": "Contact the owner for repair @excute7."}
