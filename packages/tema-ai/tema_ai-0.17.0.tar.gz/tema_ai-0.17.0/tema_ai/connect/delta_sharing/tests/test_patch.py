import json
from copy import deepcopy
from json import dumps, loads
from unittest.mock import MagicMock, patch

import pandas as pd
from delta_sharing.protocol import Format, Metadata
from delta_sharing.rest_client import QueryTableMetadataResponse
from parameterized import parameterized_class

from ..patch import (
    AddFile,
    DataSharingRestClient,
    DeltaSharingProfile,
    DeltaSharingReader,
    HintsStore,
    JSONPredicateHints,
    ListFilesInTableResponse,
    NewDataSharingRestClient,
    Table,
    _access_ds,
    get_files_in_table,
    get_table_schema,
    load_as_pandas,
    query_table_metadata,
)

STATS = '{"numRecords":359844,"minValues":{"id":"000000473d733ba5635f211c4897a61e","administrative_area_id":"01001","date":"2010-01-01","value":-35.56,"coverage":6.62,"updated_on":"2024-07-15T10:20:56.959Z"},"maxValues":{"id":"06e0411dbb165cda486d9f6a91930c2f\x7f","administrative_area_id":"ZWE","date":"2024-10-22","value":41.46,"coverage":100.00,"updated_on":"2024-10-27T21:55:36.198Z"},"nullCount":{"id":0,"administrative_area_id":0,"date":0,"value":0,"coverage":0,"updated_on":0}}'
SCHEMA_STRING = json.dumps(
    {
        "fields": [
            {"metadata": {}, "name": "h3_hex_id", "nullable": True, "type": "string"},
            {"metadata": {}, "name": "month", "nullable": True, "type": "string"},
        ],
        "type": "struct",
    }
)
METADATA_RESPONSE = QueryTableMetadataResponse(
    delta_table_version=382,
    protocol=None,
    metadata=Metadata(
        id="id",
        name=None,
        description="desc",
        format=Format(provider="parquet", options={}),
        schema_string=SCHEMA_STRING,
        partition_columns=["month", "h3_hex_id"],
        size=77857195570,
        num_files=768,
        created_time=None,
    ),
)
COLUMNS = [f["name"] for f in json.loads(SCHEMA_STRING)["fields"]]
FILES = [
    AddFile(
        url="file1",
        id="id1",
        partition_values={"resource": "cassava", "variable": "dewp"},
        size=120,
        stats=STATS,
    ),
    AddFile(
        url="file2",
        id="id2",
        partition_values={"resource": "cotton", "variable": "dewp"},
        size=120,
        stats=STATS,
    ),
    AddFile(
        url="file3",
        id="id3",
        partition_values={"resource": "cassava", "variable": "temp"},
        size=120,
        stats=STATS,
    ),
    AddFile(
        url="file4",
        id="id4",
        partition_values={"resource": "cotton", "variable": "temp"},
        size=120,
        stats=STATS,
    ),
]
ROWS = [("hex", file.partition_values["resource"]) for file in FILES]
FULL_DF = pd.DataFrame(ROWS, columns=COLUMNS)


def build_lines():
    meta = [
        '{"protocol":{"deltaProtocol":{"minReaderVersion":1,"minWriterVersion":2}}}',
        '{"metaData":{"size":77857195570,"numFiles":946,"deltaMetadata":{"id":"2d6da623-628a-4048-b006-4c64b43ca31d","description":"The table contains detailed weather-related data for various environmental resources. It includes information about the resource, administrative area, date, weather variable, value, and coverage. This data can be used to analyze weather patterns and their impact on environmental resources, enabling better resource management and disaster preparedness. It can also help in understanding the reliability of weather data sources and their coverage.","format":{"provider":"parquet","options":{}},"schemaString":"{\\"type\\":\\"struct\\",\\"fields\\":[{\\"name\\":\\"id\\",\\"type\\":\\"string\\",\\"nullable\\":true,\\"metadata\\":{\\"comment\\":\\"Unique identifier for the row\\"}},{\\"name\\":\\"resource\\",\\"type\\":\\"string\\",\\"nullable\\":true,\\"metadata\\":{\\"comment\\":\\"Name of the resource to which the variable applies to\\"}},{\\"name\\":\\"administrative_area_id\\",\\"type\\":\\"string\\",\\"nullable\\":true,\\"metadata\\":{\\"comment\\":\\"ISO 3166-1 alpha-3 country code for countries. WORLD for the global aggregated view. Other id for suberiongs. Plese check the reference table for more details\\"}},{\\"name\\":\\"date\\",\\"type\\":\\"date\\",\\"nullable\\":true,\\"metadata\\":{\\"comment\\":\\"Date of the variable taking place\\"}},{\\"name\\":\\"variable\\",\\"type\\":\\"string\\",\\"nullable\\":true,\\"metadata\\":{\\"comment\\":\\"Name of the variable reported\\"}},{\\"name\\":\\"value\\",\\"type\\":\\"decimal(7,2)\\",\\"nullable\\":true,\\"metadata\\":{\\"comment\\":\\"Variable value\\"}},{\\"name\\":\\"coverage\\",\\"type\\":\\"decimal(5,2)\\",\\"nullable\\":true,\\"metadata\\":{\\"comment\\":\\"Percentage of the total production covered\\"}},{\\"name\\":\\"updated_on\\",\\"type\\":\\"timestamp\\",\\"nullable\\":true,\\"metadata\\":{\\"comment\\":\\"Date when the row was last updated\\"}}]}","partitionColumns":["resource","variable"],"configuration":{},"createdTime":1730110529054}}}',
    ]
    lines = [
        '{"file": {"id": "1", "url": "url", "expirationTimestamp": 1746637327000, "deltaSingleAction": {"add": {"path": "...", "partitionValues": {"resource": "cassava", "variable": "dewp"}, "size": 2436, "modificationTime": 1738306474000, "dataChange": true}}}}',
        '{"file": {"id": "2", "url": "url", "expirationTimestamp": 1746637327000, "deltaSingleAction": {"add": {"path": "...", "partitionValues": {"resource": "cotton", "variable": "dewp"}, "size": 2436, "modificationTime": 1738306474000, "dataChange": true}}}}',
        '{"file": {"id": "3", "url": "url", "expirationTimestamp": 1746637327000, "deltaSingleAction": {"add": {"path": "...", "partitionValues": {"resource": "cassava", "variable": "temp"}, "size": 2436, "modificationTime": 1738306474000, "dataChange": true}}}}',
        '{"file": {"id": "4", "url": "url", "expirationTimestamp": 1746637327000, "deltaSingleAction": {"add": {"path": "...", "partitionValues": {"resource": "cotton", "variable": "temp"}, "size": 2436, "modificationTime": 1738306474000, "dataChange": true}}}}',
    ]
    lines = [json.loads(line) for line in lines]
    lines = [
        {
            "file": {
                **line["file"],
                "deltaSingleAction": {
                    **line["file"]["deltaSingleAction"],
                    "add": {**line["file"]["deltaSingleAction"]["add"], "stats": STATS},
                },
            }
        }
        for line in lines
    ]
    lines = [*meta, *[json.dumps(line) for line in lines]]
    return lines


LINES = build_lines()

LINE_CASES = [
    {
        "lines": LINES,
        "expected": LINES,
        "partition": {"resource": ["cassava", "cotton"], "variable": ["dewp", "temp"]},
    },
    {
        "lines": LINES,
        "expected": [LINES[0], LINES[1], LINES[2], LINES[4]],
        "partition": {"resource": ["cassava"]},
    },
    {
        "lines": LINES,
        "expected": [LINES[0], LINES[1], LINES[3], LINES[5]],
        "partition": {"resource": ["cotton"]},
    },
    {
        "lines": LINES,
        "expected": [LINES[0], LINES[1], LINES[2], LINES[3]],
        "partition": {"variable": ["dewp"]},
    },
    {
        "lines": LINES,
        "expected": [LINES[0], LINES[1], LINES[3]],
        "partition": {"resource": ["cotton"], "variable": ["dewp"]},
    },
]


@parameterized_class(LINE_CASES)
class TestNewDataSharingRestClientCleanLines:
    def test(self):
        result = NewDataSharingRestClient._clean_lines(
            deepcopy(self.lines), self.partition
        )
        assert result == self.expected


PRED_HINTS_CASES = [
    {
        "add_files": [],
        "lines": LINES,
        "partition": {"resource": ["cotton"], "variable": ["dewp"]},
        "expected_add_files": [],
        "expected_lines": [LINES[0], LINES[1], LINES[3]],
    },
    {
        "add_files": [],
        "lines": LINES,
        "partition": {"resource": ["cotton"]},
        "expected_add_files": [],
        "expected_lines": [LINES[0], LINES[1], LINES[3], LINES[5]],
    },
    {
        "add_files": FILES,
        "lines": [],
        "partition": {"resource": ["cotton"], "variable": ["dewp"]},
        "expected_add_files": [FILES[1]],
        "expected_lines": [],
    },
    {
        "add_files": FILES,
        "lines": [],
        "partition": {"resource": ["cotton"]},
        "expected_add_files": [FILES[1], FILES[3]],
        "expected_lines": [],
    },
    {
        "add_files": FILES,
        "lines": [],
        "partition": None,
        "expected_add_files": FILES,
        "expected_lines": [],
    },
]


@parameterized_class(PRED_HINTS_CASES)
class TestNewDataSharingRestClientPostPredicateHints:
    @property
    def files(self):
        return ListFilesInTableResponse(
            delta_table_version=1,
            protocol=1,
            metadata=1,
            add_files=self.add_files,
            lines=deepcopy(self.lines),
        )

    @property
    def jsonPredicateHints(self):
        if self.partition is None:
            return None
        hint_store = HintsStore.instance()
        jsonPredicateHints = JSONPredicateHints.from_dict_of_valid_values(
            self.partition
        )
        hint_store.add(self.partition, jsonPredicateHints)
        return json.dumps(jsonPredicateHints)

    def test_post_predicate_hints(self):
        add_files, lines = NewDataSharingRestClient.post_predicate_hints(
            self.files, self.jsonPredicateHints
        )
        assert add_files == self.expected_add_files
        assert lines == self.expected_lines

    @patch.object(DataSharingRestClient, "list_files_in_table")
    def test_list_files_in_table(self, mock_list_files_in_table):
        mock_list_files_in_table.return_value = self.files
        # We build the client with a profile that is made up as we don't really access the data
        client = NewDataSharingRestClient(DeltaSharingProfile(1, ""))
        files = client.list_files_in_table(jsonPredicateHints=self.jsonPredicateHints)
        assert files.add_files == self.expected_add_files
        assert files.lines == self.expected_lines
        assert files.delta_table_version == self.files.delta_table_version
        assert files.protocol == self.files.protocol
        assert files.metadata == self.files.metadata


BUILDER_CASES = [
    {
        "path": "/tmp/tmpn825xoak/configs.share#noaa.environmental.weather_resource_metricsv2",
        "table": "weather_resource_metricsv2",
        "share": "noaa",
        "schema": "environmental",
        "profile": "/tmp/tmpn825xoak/configs.share",
        "limit": 1000,
        "version": 1,
        "timestamp": "2023-10-01T00:00:00Z",
    }
]


@parameterized_class(BUILDER_CASES)
class TestBuildReader:
    @patch.object(DeltaSharingProfile, "read_from_file")
    def test(self, mocked_profile):
        mocked_profile.return_value = DeltaSharingProfile(1, "")
        result = _access_ds(
            self.path, limit=self.limit, version=self.version, timestamp=self.timestamp
        )
        mocked_profile.assert_called_with(self.profile)
        assert isinstance(result, DeltaSharingReader)
        assert result._table.name == self.table
        assert result._table.share == self.share
        assert result._table.schema == self.schema
        assert result._limit == self.limit
        assert result._version == self.version
        assert result._timestamp == self.timestamp


FILES_IN_TABLE_CASES = [
    {
        "add_files": FILES,
        "lines": [],
        "partition": {"resource": ["cotton"], "variable": ["dewp"]},
        "expected": [
            {
                "id": file.id,
                "size": file.size,
                "partition_values": file.partition_values,
                "timestamp": None,
                "version": None,
                **json.loads(STATS),
            }
            for file in FILES
        ],
    },
    {
        "add_files": [],
        "lines": LINES,
        "partition": {"resource": ["cotton"], "variable": ["dewp"]},
        "expected": [
            {
                "id": loads(line)["file"]["id"],
                "size": loads(line)["file"]["deltaSingleAction"]["add"]["size"],
                "partition_values": loads(line)["file"]["deltaSingleAction"]["add"][
                    "partitionValues"
                ],
                "timestamp": None,
                "version": None,
                **json.loads(STATS),
            }
            for line in LINES
            if "file" in line
        ],
    },
]


@parameterized_class(FILES_IN_TABLE_CASES)
class TestGetFilesInTable:
    path = (
        "/tmp/tmpn825xoak/configs.share#noaa.environmental.weather_resource_metricsv2"
    )

    @property
    def files(self):
        return ListFilesInTableResponse(
            delta_table_version=1,
            protocol=1,
            metadata=1,
            add_files=self.add_files,
            lines=deepcopy(self.lines),
        )

    @patch.object(DataSharingRestClient, "list_files_in_table")
    @patch.object(DeltaSharingProfile, "read_from_file")
    def test(self, mocked_profile, mock_list_files_in_table):
        mocked_profile.return_value = DeltaSharingProfile(1, "")
        mock_list_files_in_table.return_value = self.files
        files = get_files_in_table(self.path)
        assert files == self.expected


class TestGetTableMetadata:
    @patch.object(DataSharingRestClient, "query_table_metadata")
    @patch.object(DeltaSharingProfile, "read_from_file")
    def test(self, mocked_profile, mock_metadata):
        mocked_profile.return_value = DeltaSharingProfile(1, "")
        mock_metadata.return_value = METADATA_RESPONSE
        metadata = query_table_metadata("file.config#share.schema.table")
        assert metadata == METADATA_RESPONSE.metadata


class TestGetTableSchema:
    @patch.object(DataSharingRestClient, "query_table_metadata")
    @patch.object(DeltaSharingProfile, "read_from_file")
    def test(self, mocked_profile, mock_metadata):
        mocked_profile.return_value = DeltaSharingProfile(1, "")
        mock_metadata.return_value = METADATA_RESPONSE
        schema = get_table_schema("file.config#share.schema.table")
        expected_schema = METADATA_RESPONSE.metadata.schema_string
        expected_schema = json.loads(expected_schema)["fields"]
        assert schema == expected_schema


# A dummy ScanBuilder.build().execute() that returns an empty schema
class DummyScan:
    def execute(self, interface):
        class ExecResult:
            schema = type("S", (), {"names": []})

        return ExecResult()


# A constant DataFrame that we want from_batches(...) → .to_pandas() to yield
DUMMY_DF = pd.DataFrame({"x": [42]})


# A fake Arrow Table whose .to_pandas() returns our DUMMY_DF
class FakePaTable:
    def to_pandas(self):
        return DUMMY_DF


class FakePaTableFactory:
    @staticmethod
    def from_batches(batches):
        return FakePaTable()


LOAD_PANDAS_CASES = [
    {"lines": LINES, "partition_values": None},
    {"lines": LINES, "partition_values": {"resource": ["cassava"]}},
    {"lines": LINES, "partition_values": {"variable": ["dewp"]}},
]


@parameterized_class(LOAD_PANDAS_CASES)
class TestLoadAsPandas:
    @property
    def files(self):
        return ListFilesInTableResponse(
            delta_table_version=1,
            protocol=1,
            metadata=1,
            add_files=[],
            lines=deepcopy(self.lines),
        )

    @property
    def jsonPredicateHints(self):
        if self.partition_values is None:
            return None
        hint_store = HintsStore.instance()
        jsonPredicateHints = JSONPredicateHints.from_dict_of_valid_values(
            self.partition_values
        )
        hint_store.add(self.partition_values, jsonPredicateHints)
        return json.dumps(jsonPredicateHints)

    @patch("delta_sharing.reader.pa.Table", new=FakePaTableFactory)
    @patch(
        "delta_sharing.reader.delta_kernel_rust_sharing_wrapper.PythonInterface",
        new=lambda path: None,
    )
    @patch(
        "delta_sharing.reader.delta_kernel_rust_sharing_wrapper.Table",
        new=lambda path: type(
            "FakeTable", (), {"snapshot": lambda self, interface: None}
        )(),
    )
    @patch(
        "delta_sharing.reader.delta_kernel_rust_sharing_wrapper.ScanBuilder",
        new=lambda snapshot: type("Builder", (), {"build": lambda self: DummyScan()})(),
    )
    @patch.object(DataSharingRestClient, "list_files_in_table")
    @patch.object(DeltaSharingProfile, "read_from_file")
    def test(self, mocked_profile, mock_list_files_in_table, *args):
        mocked_profile.return_value = DeltaSharingProfile(1, "")
        mock_list_files_in_table.return_value = self.files
        load_as_pandas(
            "file.config#share.schema.table", partition_values=self.partition_values
        )
        mock_list_files_in_table.assert_called_with(
            Table(name="table", share="share", schema="schema"),
            jsonPredicateHints=self.jsonPredicateHints,
            predicateHints=None,
            limitHint=None,
            version=None,
            timestamp=None,
        )
