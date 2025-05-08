import os
from unittest.mock import patch

import pytest
from requests.auth import HTTPBasicAuth

from ..constants import CLIENT_ID_KEY, CLIENT_SECRET_KEY, HOST_KEY
from ..tokens import SingleUseTemaAIDeltaSharingToken
from .test_credentials import ENVIRON, MOCKED_TOKEN


class TestSingleUseTemaAIDeltaSharingToken:
    status_code = 200
    json = MOCKED_TOKEN

    @patch("requests.request")
    def basic(self, mock_request, **kwargs):
        mock_request().json.return_value = self.json
        mock_request().status_code = self.status_code
        token = SingleUseTemaAIDeltaSharingToken(**kwargs).rotate("test")
        assert token == MOCKED_TOKEN
        mock_request.assert_called_with(
            "post",
            f"{ENVIRON[HOST_KEY]}/credentials/test/rotate-token",
            json={"existing_token_expire_in_seconds": 0},
            auth=HTTPBasicAuth(ENVIRON[CLIENT_ID_KEY], ENVIRON[CLIENT_SECRET_KEY]),
            data=None,
        )

    @patch.dict(os.environ, ENVIRON)
    def test_from_environment(self):
        self.basic()

    def test_from_variables(self):
        self.basic(
            host=ENVIRON[HOST_KEY],
            client_id=ENVIRON[CLIENT_ID_KEY],
            client_secret=ENVIRON[CLIENT_SECRET_KEY],
        )


class TestSingleUseTemaAIDeltaSharingTokenError:
    status_code = 403
    json = {"error": {"detail": "Forbidden"}}

    @patch.dict(os.environ, ENVIRON)
    def test_from_environment(self):
        with pytest.raises(Exception):
            self.basic()

    def test_from_variables(self):
        with pytest.raises(Exception):
            self.basic(
                host=ENVIRON[HOST_KEY],
                client_id=ENVIRON[CLIENT_ID_KEY],
                client_secret=ENVIRON[CLIENT_SECRET_KEY],
            )
