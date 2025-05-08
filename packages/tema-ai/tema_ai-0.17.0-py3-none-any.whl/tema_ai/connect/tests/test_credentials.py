import json
import os
from datetime import datetime
from unittest.mock import patch

from freezegun import freeze_time

from ..constants import (
    ACTIVATION_API_SUBPATH,
    CLIENT_ID_KEY,
    CLIENT_SECRET_KEY,
    HOST_KEY,
)
from ..credentials import DeltaSharingCredentials, SingleUseTemaAIDeltaSharingToken

HOST = "https://host.url"
ENVIRON = {
    HOST_KEY: HOST,
    CLIENT_ID_KEY: "CLIENT_ID",
    CLIENT_SECRET_KEY: "CLIENT_SECRET",
}
TOKEN = "TOKEN"
ACTIVATION_URL = f"https://activation.url?{TOKEN}"
MOCKED_TOKEN = {
    "tokens": [
        {
            "id": "c1a...5ee",
            "created_at": 1724432788621,
            "created_by": "2a....b2",
            "activation_url": ACTIVATION_URL,
            "expiration_time": 1724436388623,
            "updated_at": 1724432788623,
            "updated_by": "2a6...b2",
        }
    ]
}
MOCKED_CREDENTIALS = {
    "shareCredentialsVersion": 1,
    "bearerToken": "NBkmVr.........AJepiXq",
    "endpoint": "https://host.url",
    "expirationTime": "2024-08-23T00:01:00.0Z",
}


@freeze_time("2024-08-23T00:00:00Z")
class TestCredentials:
    @patch.dict(os.environ, ENVIRON)
    @patch("requests.get")
    @patch.object(SingleUseTemaAIDeltaSharingToken, "rotate")
    def test_refresh(self, mock_rotate, mock_get):
        mock_rotate.return_value = MOCKED_TOKEN
        mock_get().json.return_value = MOCKED_CREDENTIALS
        credentials = DeltaSharingCredentials.refresh(connection_name="test")
        mock_get.assert_called_with(
            f"{HOST}/{ACTIVATION_API_SUBPATH}/{TOKEN}", allow_redirects=True
        )
        assert credentials.bearer_token == MOCKED_CREDENTIALS["bearerToken"]
        assert credentials.endpoint == MOCKED_CREDENTIALS["endpoint"]
        assert credentials.expiration_time_str == MOCKED_CREDENTIALS["expirationTime"]
        assert credentials.expiration_time == datetime.strptime(
            MOCKED_CREDENTIALS["expirationTime"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert credentials.expires_in == 60
        assert credentials.connection_name == "test"
        print(credentials)

    def test_to_file(self, tmp_path):
        credentials = DeltaSharingCredentials(
            MOCKED_CREDENTIALS, connection_name="test"
        )
        cred_path = credentials.to_file(tmp_path, filename="configs.share")
        assert cred_path == f"{tmp_path}/configs.share"
        with open(cred_path) as f:
            content = json.loads(f.read())
            assert content == MOCKED_CREDENTIALS
