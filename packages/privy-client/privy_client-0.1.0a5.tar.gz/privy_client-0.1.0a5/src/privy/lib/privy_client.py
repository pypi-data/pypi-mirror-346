from typing import Union


class PrivyAPIExtension:
    _authorization_key: Union[str, None] = None

    def update_authorization_key(self, authorization_key: str) -> None:
        """Update the authorization key for the PrivyAPI client.

        Args:
          authorization_key: The new authorization key.
        """
        self._authorization_key = authorization_key.replace("wallet-auth:", "")
