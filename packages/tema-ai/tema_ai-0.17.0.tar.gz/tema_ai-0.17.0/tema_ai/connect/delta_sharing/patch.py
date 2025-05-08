"""
Patched to the delta_sharing library until the pre-filter
of files by partition is implemented
"""

from json import dumps, loads
from numbers import Number
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union

import pandas as pd
from delta_sharing import Table
from delta_sharing.delta_sharing import _parse_url
from delta_sharing.protocol import AddFile, DeltaSharingProfile, Metadata
from delta_sharing.reader import DeltaSharingReader
from delta_sharing.rest_client import DataSharingRestClient, ListFilesInTableResponse

from .json_predicate_hints import HintsStore, JSONPredicateHints

PartitionValuesType = Dict[str, List[Union[str, Number]]]


class Column(TypedDict):
    name: str
    type: str
    nullable: bool
    metadata: Dict


class FileStats(TypedDict):
    numRecords: int
    minValues: Dict[str, Any]
    maxValues: Dict[str, Any]
    nullCount: Dict[str, Any]


class File(FileStats):
    id: str
    size: int
    partition_values: Dict[str, str]
    timestamp: Optional[int]
    version: Optional[int]


def _check_partition(file: AddFile, partition_values: PartitionValuesType) -> bool:
    if isinstance(file, AddFile):
        file_partition_values = file.partition_values
    else:
        file_partition_values = file["partitionValues"]

    for pk, pv in partition_values.items():
        # let if fail if the key is not a partition key
        if file_partition_values[pk] not in pv:
            return False
    return True


class NewDataSharingRestClient(DataSharingRestClient):
    @staticmethod
    def _clean_lines(lines: List[str], partition: Dict) -> List[str]:
        check = lambda l: (
            "file" not in loads(l)
            or _check_partition(loads(l)["file"]["deltaSingleAction"]["add"], partition)
        )
        return [l for l in lines if check(l)]

    @classmethod
    def post_predicate_hints(
        cls, files: ListFilesInTableResponse, jsonPredicateHints: Optional[str] = None
    ) -> Tuple[List[AddFile], List[str]]:
        add_files = files.add_files
        lines = files.lines
        if jsonPredicateHints is not None:
            hint_store = HintsStore.instance()  # type: ignore
            partition = hint_store.get(loads(jsonPredicateHints))
            # check the available partitions
            add_files = [f for f in add_files if _check_partition(f, partition)]
            lines = cls._clean_lines(lines, partition)
        return add_files, lines

    def list_files_in_table(
        self, *args: Any, jsonPredicateHints: Optional[str] = None, **kwargs: Any
    ) -> ListFilesInTableResponse:
        files = super().list_files_in_table(
            *args, jsonPredicateHints=jsonPredicateHints, **kwargs
        )
        add_files = files.add_files
        lines = files.lines
        if jsonPredicateHints is not None:
            add_files, lines = self.post_predicate_hints(files, jsonPredicateHints)

        return ListFilesInTableResponse(
            delta_table_version=files.delta_table_version,
            protocol=files.protocol,
            metadata=files.metadata,
            add_files=add_files,
            lines=lines,
        )


def _access_ds(
    url: str,
    limit: Optional[int] = None,
    version: Optional[int] = None,
    timestamp: Optional[str] = None,
    **kwargs: Any,
) -> DeltaSharingReader:
    """
    Load the DeltaSharingReader object

    Parameters
    ----------
    url: str
        a url under the format "<profile>#<share>.<schema>.<table>"

    limit: int
        a non-negative int. Load only the ``limit`` rows if the parameter is specified.
        Use this optional parameter to explore the shared table without loading the entire table to
        the memory.

    version: int
        an optional non-negative int. Load the snapshot of table at version

    Returns
    -------
    : DeltaSharingReader
        Instance of DeltaSharingReader with access to the delta share table
    """
    profile_json, share, schema, table = _parse_url(url)
    profile = DeltaSharingProfile.read_from_file(profile_json)
    rest_client = NewDataSharingRestClient(profile)
    return DeltaSharingReader(
        table=Table(name=table, share=share, schema=schema),
        rest_client=rest_client,
        limit=limit,
        version=version,
        timestamp=timestamp,
        **kwargs,
    )


def _load_stats(file: AddFile) -> FileStats:
    stats = loads(file.stats)
    return {
        "numRecords": stats["numRecords"],
        "minValues": stats["minValues"],
        "maxValues": stats["maxValues"],
        "nullCount": stats["nullCount"],
    }


def _create_file_dict(file: AddFile) -> File:
    stats = _load_stats(file)
    return {
        "id": file.id,
        "size": file.size,
        "partition_values": file.partition_values,
        "timestamp": file.timestamp,
        "version": file.version,
        **stats,  # type: ignore
    }


def _get_files_in_table(*args: Any, **kwargs: Any) -> ListFilesInTableResponse:
    ds = _access_ds(*args, use_delta_format=True, **kwargs)
    return ds._rest_client.list_files_in_table(
        ds._table,
        predicateHints=ds._predicateHints,
        limitHint=ds._limit,
        version=ds._version,
        timestamp=ds._timestamp,
    )


def get_files_in_table(*args: Any, **kwargs: Any) -> List[File]:
    files = _get_files_in_table(*args, **kwargs)
    # Assume the files are in the format of AddFile
    add_files = files.add_files
    # If the files are in the format of lines, we need to parse them
    if files.lines:
        lines = [l for l in files.lines if "file" in l]
        files = [loads(file)["file"] for file in lines]
        # inject the partitionValues
        files = [{**file, **file["deltaSingleAction"]["add"]} for file in files]
        add_files = [AddFile.from_json(file) for file in files]

    return [_create_file_dict(file) for file in add_files]


def query_table_metadata(*args: Any, **kwargs: Any) -> Metadata:
    ds = _access_ds(*args, use_delta_format=True, **kwargs)
    metadata_resp = ds._rest_client.query_table_metadata(ds._table)
    print(metadata_resp)
    return metadata_resp.metadata


def get_table_schema(*args: Any, **kwargs: Any) -> List[Column]:
    metadata = query_table_metadata(*args, **kwargs)
    schema = metadata.schema_string
    if isinstance(schema, str):
        schema = loads(schema)
    return schema["fields"]


def load_as_pandas(
    *args: Any, partition_values: Optional[PartitionValuesType] = None, **kwargs: Any
) -> pd.DataFrame:
    """
    Load the shared table using the given url as a pandas DataFrame.

    Parameters
    ----------
    url: str
        a url under the format "<profile>#<share>.<schema>.<table>"

    limit: int
        a non-negative int. Load only the ``limit`` rows if the parameter is specified.
        Use this optional parameter to explore the shared table without loading the entire table to
        the memory.

    version: int
        an optional non-negative int. Load the snapshot of table at version

    partition_values: PartitionValuesType
        An optional dictionary of partition key and values.
        Only values specified in the partition will be loaded
        Partition keys must exist on the target table or the code will fail
        Example: if the table is partitioned by a column month
            {"month": ["202003", "202004"]}


    Returns
    -------
    : pd.DataFrame
        A pandas DataFrame representing the shared table.
    """
    hint_store = HintsStore.instance()  # type: ignore
    jsonPredicateHints = None
    if partition_values is not None:
        predicate = JSONPredicateHints.from_dict_of_valid_values(partition_values)
        hint_store.add(partition_values, predicate)
        jsonPredicateHints = dumps(predicate)

    reader = _access_ds(
        *args, jsonPredicateHints=jsonPredicateHints, use_delta_format=True, **kwargs
    )
    return reader.to_pandas()
