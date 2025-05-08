"""
Casts columns to the correct data type for pandas data frames retrieved from the API.
Particularly useful for Decimal columns which are returned as strings.
"""

from typing import List

import pandas as pd

from .types import Field


def cast_dataframe(df: pd.DataFrame, schema: List[Field]) -> pd.DataFrame:
    """
    Casts columns to the correct data type for pandas data frames retrieved from the API.
    Particularly useful for Decimal columns which are returned as strings.
    """
    for col_schema in schema:
        col_name = col_schema["name"]
        col_type = col_schema["type"]
        if col_name in df.columns:
            # Convert decimal types (in string format) to float
            if col_type.startswith("decimal"):
                df[col_name] = pd.to_numeric(df[col_name], errors="coerce")
    return df
