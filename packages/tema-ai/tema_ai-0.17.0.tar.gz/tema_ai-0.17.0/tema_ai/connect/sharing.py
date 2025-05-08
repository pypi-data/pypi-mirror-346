import json
import time
import warnings
from contextlib import contextmanager
from functools import lru_cache
from tempfile import TemporaryDirectory
from typing import Any, Dict, Generator, List, Optional

import pandas as pd
from delta_sharing import SharingClient
from delta_sharing.protocol import Metadata

from .constants import CONNECTION_KEY
from .credentials import DeltaSharingCredentials
from .delta_sharing import (
    Column,
    File,
    get_files_in_table,
    get_table_schema,
    load_as_pandas,
    query_table_metadata,
)
from .protocol import Schema, Share, Table
from .types import TableDetails, TableReport
from .utils import load_parameter


class TemaAIShareAPI:
    """
    A class to facilitate interaction with a Delta Sharing API, providing methods to
    authenticate, access, and retrieve data from Delta Sharing tables. This class is
    designed to simplify the process of working with Delta Sharing, offering a
    straightforward interface to manage credentials, list available resources, and
    query tables for data.

    You require the following variables to access the Delta Sharing API:
        connection: The name of the connection to use for accessing the Delta Sharing API.
            You can create new connections in the https://tema.ai platform.
            Each connection has short lived credentials used to authenticate with the Delta Sharing API.
            Issuing new short lived credentials invalidates the previous ones. So using the same connection
            in several applications will invalidate the credentials for the other applications.
            Use 1 connection per application.

        host: The host URL for the Delta Sharing service. This is used to establish the connection to the service.
            This value is provided across your keys in the tema.ai platform.

        client_id: The client id for the recipient. Retrieve this from the tema.ai platform.
            Or generate a new one in the tema.ai platform.

        client_secret: The client secret for the recipient. You should have stored this value
            securely when you generated the client id. If you don't have it, you can remove
            the client id and client secret from the tema.ai platform and generate
            a new one.

    All these values can be provided to the class or loaded from the environment variables.

    Attributes
    ----------
    connection_name : str, optional
        The name of the connection to use for accessing the Delta Sharing API. If not
        provided, it will be loaded from a predefined parameter.
    host : str, optional
        The host URL for the Delta Sharing service. This is used to establish the
        connection to the service.
    env_file : str, optional
        The name of the environment file to load the connection name from. The default
        value is '.env'.
    kwargs : dict
        Additional keyword arguments that may be passed for connection or client
        configuration. This includes client_id and client_secret for authentication.
    """

    def __init__(
        self,
        connection_name: Optional[str] = None,
        host: Optional[str] = None,
        env_file: str = ".env",
        **kwargs: Any,
    ) -> None:
        self.connection_name = load_parameter(
            connection_name, CONNECTION_KEY, env_file=env_file
        )
        self.kwargs = kwargs
        self.host = host
        self.env_file = env_file

    @lru_cache()
    def _credentials(self, ttl_hash: Optional[int] = None) -> DeltaSharingCredentials:
        return DeltaSharingCredentials.refresh(
            self.connection_name, host=self.host, env_file=self.env_file, **self.kwargs
        )

    @staticmethod
    def ttl_hash(seconds: int = 3600) -> int:
        return round(time.time() / seconds)

    @property
    def credentials(self) -> DeltaSharingCredentials:
        """
        Builds the Delta share credentials
        You will need access to the ssm parameter with the
        appropriate Client and Secret ID
        """
        # 1 hour cache for the credentials
        return self._credentials(ttl_hash=self.ttl_hash())

    @lru_cache()
    def _client(self, ttl_hash: Optional[int] = None) -> SharingClient:
        with TemporaryDirectory() as tmp_folder:
            cred_path = self.credentials.to_file(tmp_folder)
            return SharingClient(cred_path)

    @property
    def client(self) -> SharingClient:
        """
        Builds a delta sharing client with the appropriate
        credentials to access the Share
        """
        return self._client(ttl_hash=self.ttl_hash())

    @property
    def shares(self) -> List[Share]:
        """
        Returns all shares the connection has access to
        """
        return self.client.list_shares()

    def schemas(self, share: Share) -> List[Schema]:
        """
        Given a share returns all schemas the
        connection has access to given a share
        """
        return self.client.list_schemas(share)

    def tables(self, schema: Schema) -> List[Table]:
        """
        Lists the tables the connection has access to
        given a schema
        """
        return self.client.list_tables(schema)

    @contextmanager
    def _table_with_credentials(self, table: Table) -> Generator[str, None, None]:
        with TemporaryDirectory() as tmp_folder:
            cred_path = self.credentials.to_file(tmp_folder)
            yield f"{cred_path}#{table.share}.{table.schema}.{table.name}"

    def table_schema(self, table: Table, **kwargs: Any) -> List[Column]:
        """
        Schema for the requested table as a list of columns with their names
        type and nullable property
        """
        with self._table_with_credentials(table) as _table:
            return get_table_schema(_table, **kwargs)

    def table_files(self, table: Table, **kwargs: Any) -> List[File]:
        """
        Returns a list of all files in the table
        """
        with self._table_with_credentials(table) as _table:
            return get_files_in_table(_table, **kwargs)

    def table_metadata(self, table: Table, **kwargs: Any) -> Metadata:
        """
        Returns the metadata for the table
        """
        with self._table_with_credentials(table) as _table:
            return query_table_metadata(_table, **kwargs)

    def available_partitions(self, table: Table, **kwargs: Any) -> Dict[str, List[Any]]:
        """
        Returns a list of all partitions available in the table with its values.
        For example for a table with partition columns year and month. And partition values
        year=2021 and month=01, year=2021 and month=02, year=2022 and month=01
        it returns {
            "year": [2021, 2022],
            "month": [01, 02]
        }
        """
        files = self.table_files(table, **kwargs)
        partitions = [f["partition_values"] for f in files]
        partition_columns = {key for row in partitions for key in row.keys()}
        return {
            key: sorted({item.get(key) for item in partitions if item.get(key)})
            for key in partition_columns
        }

    def table_report(self, table: Table, **kwargs: Any) -> TableReport:
        """
        Builds a report with the number of files and possible
        partitions and values on the target delta share table

        Parameters
        ----------
        table: Table
            Delta Share table to build the report for

        Returns
        -------
        : TableReport
            A dictionary with the keys:
            - num_files
            - partition_columns
            - total_records
            - avg_records_per_file
            - size
            - avg_size_per_file
        """
        # Deprecation warning
        warnings.warn(
            "The 'table_report' method is deprecated and will be removed in a future release. "
            "Please use the method 'table_details' for a more detailed report.",
            DeprecationWarning,
            stacklevel=2,
        )
        files = self.table_files(table, **kwargs)
        num_files = len(files)
        total_records = sum([file["numRecords"] for file in files])
        size = sum([file["size"] for file in files])
        return {
            "num_files": num_files,
            "partition_columns": list(
                {key for file in files for key in file["partition_values"].keys()}
            ),
            "total_records": total_records,
            "avg_records_per_file": int(total_records / num_files),
            "size": size,  # in bytes
            "avg_size_per_file": int(size / num_files),  # in bytes
        }

    def table_details(self, table: Table, **kwargs: Any) -> TableDetails:
        # get files and metadata
        files = self.table_files(table, **kwargs)
        num_records = sum([file["numRecords"] for file in files])
        metadata = self.table_metadata(table, **kwargs)
        size = metadata.metadata.size
        num_files = metadata.metadata.num_files
        return {
            "table": table.name,
            "schema": table.schema,
            "share": table.share,
            "description": metadata.metadata.description,
            "num_files": num_files,
            "partition_columns": metadata.metadata.partition_columns,
            "total_records": num_records,
            "avg_records_per_file": int(num_records / num_files),
            "size": size,
            "avg_size_per_file": int(size / num_files),
            "table_schema": json.loads(metadata.metadata.schema_string),
        }

    def list_all_tables(self) -> List[Table]:
        """
        Lists all tables the user has access to in the Delta Sharing API
        """
        return self.client.list_all_tables()

    def table_to_pandas(self, table: Table, **kwargs: Any) -> pd.DataFrame:
        """
        Retrieves a table as a pandas DataFrame
        """
        with self._table_with_credentials(table) as _table:
            return load_as_pandas(_table, **kwargs)
