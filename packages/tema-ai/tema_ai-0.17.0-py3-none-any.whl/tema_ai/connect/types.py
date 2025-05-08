from typing import Any, Callable, Dict, List, TypedDict


class Token(TypedDict):
    id: str
    created_at: int
    created_by: str
    activation_url: str
    expiration_time: int
    updated_at: int
    updated_by: str


class Properties(TypedDict):
    properties: Dict[str, str]


class Recipient(TypedDict):
    name: str
    authentication_type: str
    owner: str
    properties_kvpairs: Properties
    created_at: int
    created_by: str
    tokens: List[Token]
    updated_at: int
    updated_by: str
    full_name: str
    securable_type: str
    securable_kind: str


class Credentials(TypedDict):
    client_id: str
    secret_id: str


CredentialsFunction = Callable[[], Credentials]


class TableReport(TypedDict):
    num_files: int
    partition_columns: List[str]
    total_records: int
    avg_records_per_file: int
    size: int
    avg_size_per_file: int


class Field(TypedDict):
    name: str
    type: str
    nullable: bool
    metadata: Dict[str, Any]


class Schema(TypedDict):
    type: str
    fields: List[Field]


class TableDetails(TypedDict):
    table: str
    schema: str
    share: str
    description: str
    num_files: int
    partition_columns: List[str]
    total_records: int
    avg_records_per_file: int
    size: int
    avg_size_per_file: int
    table_schema: Schema
