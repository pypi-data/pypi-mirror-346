"""
Delta Sharing Credentials Module

This module provides functionality to retrieve, manage, and store credentials
used for accessing Delta Sharing APIs. It includes classes and methods
that handle the retrieval of credentials from a Delta Sharing server,
refreshing tokens, and saving credentials to a file for future use.

Classes:
    - Credentials: A TypedDict that specifies the expected structure of
      the Delta Sharing credentials.
    - DeltaSharingCredentials: Handles the retrieval and management of
      Delta Sharing credentials, including methods for refreshing credentials
      and saving them to a file.

Dependencies:
    - json: To handle JSON encoding and decoding.
    - os: For interacting with the operating system, such as file path management.
    - datetime: For handling and manipulating date and time.
    - requests: To make HTTP requests to the Delta Sharing server.
    - typing: For type annotations and TypedDict.
    - .constants: Imports constants like HOST_KEY and ACTIVATION_API_SUBPATH
      specific to the Delta Sharing environment.
    - .connection: Imports the DeltaConnection class for managing API
      interactions related to token rotation.

This module is primarily used to facilitate secure access to files
shared through the Delta Sharing protocol, ensuring that credentials
are retrieved and managed efficiently.
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Optional, TypedDict

import requests

from .constants import ACTIVATION_API_SUBPATH, HOST_KEY
from .tokens import SingleUseTemaAIDeltaSharingToken


class Credentials(TypedDict):
    shareCredentialsVersion: int
    bearerToken: str
    endpoint: str
    expirationTime: str


class DeltaSharingCredentials:
    """
    Retrieves Delta Sharing protocol credentials. These credentials
    are used to access the Delta Share API and retrieve
    the files shared with the recipient. The credentials
    are valid for a certain amount of time specified in the
    delta share server. The credentials are retrieved using
    a one time use token issued to the recipient on creation
    or on refresh. The token can be retrieved from the
    delta share server using the recipient name and the
    service principal Oauth token.

    """

    def __init__(self, credentials: Credentials, connection_name: str) -> None:
        """ "
        Parameters
        ----------
        credentials: Credentials
            Delta Share credentials retrieved from the server

        connection_name: str
            Name of the recipient for which the credentials
            were retrieved
        """
        self.credentials = credentials
        self.connection_name = connection_name

    def __repr__(self) -> str:
        return self.__str__().replace("\n", "")

    def __str__(self) -> str:
        return (
            "<Delta Sharing Credentials: "
            f"connection {self.connection_name} "
            f"expiring in {self.expires_in}s>"
        )

    @property
    def bearer_token(self) -> str:
        """
        Bearer token used to access the Delta Sharing Api
        """
        return self.credentials["bearerToken"]

    @property
    def endpoint(self) -> str:
        """
        Endpoint to retrieve delta share files
        """
        return self.credentials["endpoint"]

    @property
    def expiration_time_str(self) -> str:
        """
        Expiration time as string
        """
        return self.credentials["expirationTime"]

    @property
    def expiration_time(self) -> datetime:
        """
        Expiration time as datetime
        """
        return datetime.strptime(self.expiration_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    @property
    def expires_in(self) -> int:
        """
        Number of seconds until expiration
        """
        return (
            self.expiration_time.replace(tzinfo=timezone.utc)
            - datetime.now(timezone.utc)
        ).seconds

    @classmethod
    def from_token(
        cls, token: str, *args: Any, host: Optional[str] = None
    ) -> "DeltaSharingCredentials":
        """
        Retrieves the delta share credentials from a public
        endpoint using the one time use token issued to the
        connection on creation or on refresh.

        This method does not require any authentication,
        service principal Oauth tokens, etc

        Each token can only be used once to retrieve the credentials

        Parameters
        ----------
        token: str
            Delta sharing one time use credentials retrieve token

        host: Optional[str]
            Delta sharing host. If not provided, the env variable specified
            in HOST_KEY is used instead

        Returns
        -------
        : DeltaSharingCredentials
            instance of the class with Delta sharing credentials valid
            for X seconds
        """
        host = host or os.environ[HOST_KEY]
        credentials = requests.get(
            f"{host}/{ACTIVATION_API_SUBPATH}/{token}", allow_redirects=True
        )
        return cls(credentials.json(), *args)

    @classmethod
    def refresh(
        cls, connection_name: str, host: Optional[str] = None, **kwargs: Any
    ) -> "DeltaSharingCredentials":
        """
        Refreshes the connection credentials and retrieves the new values
        This is a protected endpoint so you need access to tema ai credentials.
        Please generate a key and secret for the connection at https://tema.ai

        Parameters
        ----------
        connection_name: str
            Name of the delta sharing connection you need to update the
            token for
        """
        token = SingleUseTemaAIDeltaSharingToken(host=host, **kwargs).rotate(
            connection_name
        )
        activation_url = token["tokens"][0]["activation_url"]
        # extract the token from the activation url
        activation_url_token = activation_url.split("?")[-1]
        return cls.from_token(activation_url_token, connection_name, host=host)

    def to_file(self, folder: str, filename: str = "configs.share") -> str:
        """
        Stores the credentials as a credentials file
        so it can be used by delta_share
        """
        path = os.path.join(folder, filename)
        with open(path, "w") as file:
            json.dump(self.credentials, file)
        return path
