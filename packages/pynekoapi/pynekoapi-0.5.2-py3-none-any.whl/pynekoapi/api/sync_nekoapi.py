from typing import Any, Dict, Optional

from pynekoapi.tools import SyncRequest


class SyncNekoApi:

    def __init__(self, timeout: Optional[int] = None) -> None:
        """
        Initializes the SyncNekoApi class.

        Args:
            timeout (Optional[int]): The timeout in seconds for HTTP requests. Defaults to None.
        """
        self.fetch = SyncRequest(timeout)
        self.base_url = "https://api.rizkiofficial.com/v1/"

    def get_bin(self, key: str) -> Dict[Any, Any]:
        """
        Retrieves a bin from the NekoBin API based on the given key.

        Args:
            key (str): The key of the bin to retrieve.

        Returns:
            Dict[Any, Any]: A dictionary containing the bin data.
        """
        result = self.fetch._get(self.base_url + f"nekobin/get?key={key}")
        return result

    def save_bin(self, content: str) -> Dict[Any, Any]:
        """
        Saves a bin to the NekoBin API.

        Args:
            content (str): The content to save.

        Returns:
            Dict[Any, Any]: A dictionary containing the result of the save operation.
        """
        result = self.fetch._post(
            self.base_url + f"nekobin/save",
            json={"content": content},
        )
        return result

    def register_date(self, user_id: int, timezone: Optional[str] = None) -> Dict[Any, Any]:
        """
        Registers a date for a user with the given ID.

        Args:
            user_id (int): The ID of the user to register.
            timezone (Optional[str]): The timezone to use. Defaults to None -> 'UTC'.

        Returns:
            Dict[Any, Any]: A dictionary containing the result of the registration.
        """
        url = self.base_url + f"register_date?user_id={user_id}"
        if timezone is not None:
            url += f"&tz={timezone}"
        result = self.fetch._post(url)
        return result
