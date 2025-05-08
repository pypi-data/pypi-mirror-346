import os
from unittest.mock import patch

from delta_sharing import Schema, Share, Table  # type: ignore
from delta_sharing.protocol import Format, Metadata, Protocol
from delta_sharing.rest_client import QueryTableMetadataResponse
from parameterized import parameterized_class
from requests.auth import HTTPBasicAuth

from ..constants import (
    ACTIVATION_API_SUBPATH,
    CLIENT_ID_KEY,
    CLIENT_SECRET_KEY,
    CONNECTION_KEY,
    CREDENTIALS_API_SUBPATH,
    HOST_KEY,
)
from ..sharing import DeltaSharingCredentials, SharingClient, TemaAIShareAPI
from .test_credentials import ENVIRON, MOCKED_CREDENTIALS, MOCKED_TOKEN

CONNECTION_NAME = "recipient"
SHARE = Share("share")
SCHEMA = Schema(name="schema", share="share")
TABLE = Table(name="table", share="share", schema="schema")


class TestDeltaShare:
    @property
    @patch.dict(os.environ, ENVIRON)
    def sharer(self):
        return TemaAIShareAPI(CONNECTION_NAME)

    def test_connection_name(self):
        assert self.sharer.connection_name == CONNECTION_NAME

    @patch.object(DeltaSharingCredentials, "refresh")
    def test_credentials(self, mock_cred):
        sharer = self.sharer
        cred = sharer.credentials
        mock_cred.assert_called_with(CONNECTION_NAME, host=None, env_file=".env")
        sharer.credentials
        #  because there is a caching mechanism we should only hve 1 call
        assert mock_cred.call_count == 1

    @patch.object(DeltaSharingCredentials, "refresh")
    def test_client(self, mock_cred):
        mock_cred.return_value = DeltaSharingCredentials(
            MOCKED_CREDENTIALS, CONNECTION_NAME
        )
        sharer = self.sharer
        sharer.client
        mock_cred.assert_called_with(CONNECTION_NAME, host=None, env_file=".env")
        client = sharer.client
        # only 1 call because of the cache for 1 hour
        assert mock_cred.call_count == 1
        assert client._profile.bearer_token == MOCKED_CREDENTIALS["bearerToken"]
        assert client._profile.endpoint == MOCKED_CREDENTIALS["endpoint"]

    @patch.object(DeltaSharingCredentials, "refresh")
    def _test_fnc(
        self, fnc, mock_cred, args=()
    ):  # the with args is to to interfere with the mock
        mock_cred.return_value = DeltaSharingCredentials(
            MOCKED_CREDENTIALS, CONNECTION_NAME
        )
        return getattr(self.sharer, fnc)(*args)

    @patch.object(SharingClient, "list_shares")
    def test_shares(self, mock_c):
        self._test_fnc("shares")
        mock_c.assert_called_with()

    @patch.object(SharingClient, "list_schemas")
    def test_schemas(self, mock_c):
        self._test_fnc("schemas", args=[SHARE])
        mock_c.assert_called_with(SHARE)

    @patch.object(SharingClient, "list_tables")
    def test_tables(self, mock_c):
        self._test_fnc("tables", args=[SCHEMA])
        mock_c.assert_called_with(SCHEMA)

    @patch.object(SharingClient, "list_all_tables")
    def test_list_all_tables(self, mock_c):
        self._test_fnc("list_all_tables")
        mock_c.assert_called_with()

    @patch.object(DeltaSharingCredentials, "to_file")
    @patch.object(DeltaSharingCredentials, "refresh")
    def _test(self, fnc, path, mock_cred, mock_to_file):
        mock_to_file.return_value = path
        mock_cred.return_value = DeltaSharingCredentials(
            MOCKED_CREDENTIALS, CONNECTION_NAME
        )
        return getattr(self.sharer, fnc)(TABLE)

    @patch("tema_ai.connect.sharing.load_as_pandas")
    def test_table_to_pandas(self, mock_table):
        path = "file.config"
        self._test("table_to_pandas", path)
        mock_table.assert_called_with(f"{path}#share.schema.table")

    @patch("tema_ai.connect.sharing.get_table_schema")
    def test_table_schema(self, mock_table):
        path = "file.config"
        self._test("table_schema", path)
        mock_table.assert_called_with(f"{path}#share.schema.table")

    @patch("tema_ai.connect.sharing.get_files_in_table")
    def test_get_files_in_table(self, mock_table):
        path = "file.config"
        self._test("table_files", path)
        mock_table.assert_called_with(f"{path}#share.schema.table")

    @patch.object(TemaAIShareAPI, "table_files")
    def test_table_report(self, mock_table):
        mock_table.return_value = [
            {"numRecords": 10, "size": 10, "partition_values": {"years": "2023"}}
        ]
        path = "file.config"
        report = self._test("table_report", path)
        print(report)
        assert report == {
            "num_files": 1,
            "partition_columns": ["years"],
            "total_records": 10,
            "avg_records_per_file": 10,
            "size": 10,
            "avg_size_per_file": 10,
        }


HOST = "https://host.url"
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"


@parameterized_class(
    [
        {"env_file": ".envOther", "temp": True},
        {"env_file": ".env.prod", "temp": True},
        {"env_file": ".env.test", "temp": True},
        # this is the default value
        {"env_file": ".env", "temp": False},
    ]
)
class TestTemaAIShareAPIEnvFiles:
    @property
    def env_file_content(self):
        return f"{HOST_KEY}={HOST}\n{CONNECTION_KEY}={CONNECTION_NAME}\n{CLIENT_ID_KEY}={CLIENT_ID}\n{CLIENT_SECRET_KEY}={CLIENT_SECRET}"

    @patch("requests.get")
    @patch("requests.request")
    def test(self, mock_request, mock_get, tmp_path):
        mock_get().json.return_value = MOCKED_CREDENTIALS
        mock_request().json.return_value = MOCKED_TOKEN
        mock_request().status_code = 200

        # First we generate the file and store it
        env_file = self.env_file
        if self.temp:
            with open(tmp_path / self.env_file, "w") as file:
                file.write(self.env_file_content)
            env_file = str(tmp_path / self.env_file)
        else:
            with open(self.env_file, "w") as file:
                file.write(self.env_file_content)

        if self.temp:
            api = TemaAIShareAPI(env_file=env_file)
        else:
            # the non temp uses the default value
            api = TemaAIShareAPI()

        api.credentials
        mock_get.assert_called_with(
            f"{HOST}/{ACTIVATION_API_SUBPATH}/TOKEN", allow_redirects=True
        )
        mock_request.assert_called_with(
            "post",
            f"{HOST}/{CREDENTIALS_API_SUBPATH}/{CONNECTION_NAME}/rotate-token",
            json={"existing_token_expire_in_seconds": 0},
            auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
            data=None,
        )
        # delete the file if it was no temp
        if not self.temp:
            os.remove(self.env_file)


PARTITION_CASES = [
    {
        "files": [
            {"partition_values": {"years": "2023"}},
            {"partition_values": {"years": "2024"}},
        ],
        "expected": {"years": ["2023", "2024"]},
    },
    {
        "files": [
            {"partition_values": {"years": "2023", "months": "01"}},
            {"partition_values": {"years": "2023", "months": "02"}},
        ],
        "expected": {"years": ["2023"], "months": ["01", "02"]},
    },
    {
        "files": [
            {"partition_values": {"years": "2023", "months": "01"}},
            {"partition_values": {"years": "2023", "months": "02"}},
            {"partition_values": {"years": "2024", "months": "01"}},
        ],
        "expected": {"years": ["2023", "2024"], "months": ["01", "02"]},
    },
    {
        "files": [
            {"partition_values": {"years": "2023", "months": "01", "days": "01"}},
            {"partition_values": {"years": "2023", "months": "02", "days": "01"}},
            {"partition_values": {"years": "2024", "months": "01", "days": "01"}},
        ],
        "expected": {"years": ["2023", "2024"], "months": ["01", "02"], "days": ["01"]},
    },
]


@parameterized_class(PARTITION_CASES)
class TestAvailablePartitions:
    """
    Tests the available partitions method
    """

    @patch.object(TemaAIShareAPI, "table_files")
    def test(self, mock_files):
        mock_files.return_value = self.files

        connection = TemaAIShareAPI()
        table = Table(name="table", share="share", schema="schema")
        partitions = connection.available_partitions(table)
        mock_files.assert_called_with(table)

        assert partitions == self.expected


class TestTableDetails:
    @patch.object(TemaAIShareAPI, "table_files")
    @patch.object(TemaAIShareAPI, "table_metadata")
    def test(self, mock_metadata, mock_files):
        mock_files.return_value = [
            {"numRecords": 650, "size": 10, "partition_values": {"years": "2023"}}
        ]
        mock_metadata.return_value = QueryTableMetadataResponse(
            1,
            Protocol(min_reader_version=1),
            Metadata(
                id="id",
                name="name",
                description="description",
                format=Format(provider="parquet", options={}),
                schema_string='{"type":"struct","fields":[{"name":"file","type":"string","nullable":true,"metadata":{}}]}',
                partition_columns=["partition_columns"],
                configuration={},
                version=None,
                size=6635846314,
                num_files=493,
            ),
        )
        connection = TemaAIShareAPI()
        table = Table(name="table", share="share", schema="schema")
        details = connection.table_details(table)
        assert details == {
            "table": table.name,
            "schema": table.schema,
            "share": table.share,
            "description": "description",
            "num_files": 493,
            "partition_columns": ["partition_columns"],
            "total_records": 650,
            "avg_records_per_file": int(650 / 493),
            "size": 6635846314,
            "avg_size_per_file": int(6635846314 / 493),
            "table_schema": {
                "type": "struct",
                "fields": [
                    {"name": "file", "type": "string", "nullable": True, "metadata": {}}
                ],
            },
        }
