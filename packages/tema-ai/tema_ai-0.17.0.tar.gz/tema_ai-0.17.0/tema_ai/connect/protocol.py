from typing import Optional, Union

from delta_sharing import Schema as DSSchema  # type: ignore
from delta_sharing import Share
from delta_sharing import Table as DSTable


class Schema(DSSchema):
    """
    Represents a schema in the data sharing platform.

    Attributes:
        share (Union[str, Share]): The share to which this schema belongs.
                                    This can be either a string representing the share name or an instance of the Share class.
        schema (str): The name of the schema.

    Methods:
        __init__(share: Union[str, Share]=None, schema: str = None) -> None:
            Initializes a new Schema instance. The share and schema must be provided.
    """

    def __init__(
        self, name: Optional[str] = None, share: Optional[Union[str, Share]] = None
    ) -> None:
        """
        Initializes a Schema instance.

        Args:
            share (Union[str, Share]): The share to which this schema belongs. Must be provided.
            schema (str): The name of the schema. Must be provided.

        Raises:
            ValueError: If share or schema is not provided.
        """
        if share is None:
            raise ValueError("Share must be provided")
        if name is None:
            raise ValueError("Schema must be provided")
        share = share.name if isinstance(share, Share) else share
        super().__init__(share=share, name=name)


class Table(DSTable):
    """
    Represents a table in the data sharing platform.

    Attributes:
        name (str): The name of the table.
        share (Union[str, Share]): The share to which this table belongs.
                                   This can be either a string representing the share name or an instance of the Share class.
        schema (Union[str, Schema]): The schema to which this table belongs.
                                     This can be either a string representing the schema name or an instance of the Schema class.

    Methods:
        __init__(name: str = None, share: Union[str, Share]=None, schema: Union[str, Schema]=None) -> None:
            Initializes a new Table instance. The name, share, and schema must be provided.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        share: Optional[Union[str, Share]] = None,
        schema: Optional[Union[str, Schema]] = None,
    ) -> None:
        """
        Initializes a Table instance.

        Args:
            name (str): The name of the table. Must be provided.
            share (Union[str, Share]): The share to which this table belongs. Must be provided.
            schema (Union[str, Schema]): The schema to which this table belongs. Must be provided.

        Raises:
            ValueError: If name, share, or schema is not provided.
        """
        if share is None:
            raise ValueError("Share must be provided")
        if schema is None:
            raise ValueError("Schema must be provided")
        if name is None:
            raise ValueError("Table must be provided")

        share = share.name if isinstance(share, Share) else share
        schema = schema.name if isinstance(schema, Schema) else schema
        super().__init__(name=name, share=share, schema=schema)
