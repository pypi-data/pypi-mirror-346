from typing import Dict, Optional

import requests
from requests import Response
from requests.auth import HTTPBasicAuth

from .constants import (
    CLIENT_ID_KEY,
    CLIENT_SECRET_KEY,
    CREDENTIALS_API_SUBPATH,
    HOST_KEY,
)
from .types import Recipient
from .utils import load_parameter


class SingleUseTemaAIDeltaSharingToken:
    """
    Connects to the Tema AI Share API and retrieves one use
    tokens that you can exchange for a Delta Sharing credential

    You need access to tema.ai API to use this class. Make sure
    you have generated the connection, client id and client secret
    in the tema.ai console. You can then use the client id and
    client secret to retrieve the one time use token that you can
    exchange for a Delta Sharing credential.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        env_file: str = ".env",
    ) -> None:
        """
        Builds an instance of the API

        Parameters
        ----------
        host: Optional[str] = None
            Workspace url. If not provided, the env variable HOST
            is used instead

        user_id: Optional[str]
            client id for the recipient. If not provided the env
            variable CLIENT_ID is used instead

        user_secret: Optional[str]
            client secret for the recipient. If not provided the env
            variable CLIENT_SECRET is used instead

        env_file: str
            The name of the environment file to load the connection name from.
            The default value is '.env'.
        """
        # default to the env variable if not set
        self.host = load_parameter(host, HOST_KEY, env_file=env_file)
        self.client_id = load_parameter(client_id, CLIENT_ID_KEY, env_file=env_file)
        self.client_secret = load_parameter(
            client_secret, CLIENT_SECRET_KEY, env_file=env_file
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        json: Optional[Dict] = None,
        data: Optional[str] = None,
    ) -> Response:
        return requests.request(
            method,
            f"{self.host}/{CREDENTIALS_API_SUBPATH}/{endpoint}",
            json=json,
            data=data,
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
        )

    def rotate(self, connection_name: str) -> Recipient:
        """
        Given a connection this method rotates its token

        Parameters
        ----------
        recipient_name: str
            Name of the recipient

        Returns
        -------
        : Recipient
            Nested dictionary with information about the recipient
            as well as the current active tokens after the rotation
        """
        response = self._request(
            "post",
            f"{connection_name}/rotate-token",
            json={"existing_token_expire_in_seconds": 0},
        )
        if response.status_code != 200:
            error = response.json()
            error = error.get("error", {}).get("detail", "")
            raise Exception(f"Failed to retrieve temporary credentials: {error}")
        return response.json()
