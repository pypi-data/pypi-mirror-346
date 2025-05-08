from typing import Any, Dict, List

from .utils import Singleton


class JSONPredicateHints:
    """
    Helper class to build Delta Sharing JSON predicate hints for partition filtering.

    Provides utilities to construct predicate trees using 'equal', 'or', and 'and' operators
    in the simpler JSON format recognized by Delta Sharing servers.
    """

    @staticmethod
    def _build_single_op(
        op: str, column_name: str, value: Any, value_type: str = "string"
    ) -> Dict[str, Any]:
        """
        Build a binary operation node comparing a column to a literal value.

        :param op: The comparison operator (e.g., 'equal', 'lessThan').
        :param column_name: Name of the partition column.
        :param value: Literal value to compare against.
        :param value_type: The data type for casting ('int', 'string', 'date', etc.).
        :return: A dictionary representing the JSON predicate node.
        """
        return {
            "op": op,
            "children": [
                {"op": "column", "name": column_name, "valueType": value_type},
                {"op": "literal", "value": str(value), "valueType": value_type},
            ],
        }

    @staticmethod
    def _chain_operators(operator: str, nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine multiple predicate nodes under a logical operator ('and' / 'or').

        :param operator: Logical operator ('and' or 'or').
        :param nodes: List of predicate node dictionaries.
        :raises ValueError: If no nodes are provided.
        :return: A dictionary representing the combined predicate.
        """
        if len(nodes) == 0:
            raise ValueError("NotEnoughChildren")
        if len(nodes) == 1:
            return nodes[0]
        return {"op": operator, "children": nodes}

    @classmethod
    def from_dict_of_valid_values(
        cls, filters: Dict[str, List[Any]], value_type: str = "string"
    ) -> Dict[str, Any]:
        """
        :param filters: mapping from column name to list of allowed values
        :param value_type: data type for all literals (e.g. "string", "int")
        :return: a JSON predicate tree, or raises ValueError if filters is empty
        """
        # For each column generate records for each valid partition
        per_column_value_nodes = [
            [cls._build_single_op("equal", col, val, value_type) for val in vals]
            for col, vals in filters.items()
        ]
        # If a column has multiple partitions then join with OR
        per_column_or_nodes = [
            cls._chain_operators("or", nodes) for nodes in per_column_value_nodes
        ]
        # Finally if there are many Columns join with AND
        return cls._chain_operators("and", per_column_or_nodes)


@Singleton
class HintsStore:
    def __init__(self) -> None:
        self._hints: Dict[int, Any] = {}

    @classmethod
    def deep_freeze(cls, obj: Any) -> Any:
        """
        Recursively convert:
        • dicts  → frozenset of (key, frozen_value) pairs
        • lists/tuples → tuple of frozen elements
        • sets → frozenset of frozen elements
        so that the result is entirely composed of hashable types.
        """
        if isinstance(obj, dict):
            # turn each key/value into a (key, frozen_value) pair,
            # then build a frozenset so order of insertion doesn’t matter
            return frozenset((k, cls.deep_freeze(v)) for k, v in obj.items())
        elif isinstance(obj, (list, tuple)):
            # preserve order here (if list order matters)
            return tuple(cls.deep_freeze(v) for v in obj)
        elif isinstance(obj, set):
            # sets themselves are unordered
            return frozenset(cls.deep_freeze(v) for v in obj)
        else:
            # assume ints, strings, etc. are already hashable
            return obj

    @classmethod
    def hash(cls, val: Dict[str, Any]) -> int:
        return hash(cls.deep_freeze(val))

    def add(self, partitions: Dict, hints: Dict[str, Any]) -> None:
        """
        Add a new set of hints to the store.

        :param partitions: The partition values.
        :param hints: The hints to be stored.
        """
        hash = self.hash(hints)
        self._hints[hash] = partitions

    def get(self, hints: Dict[str, Any]) -> Dict[str, Any]:
        """ """
        hash = self.hash(hints)
        return self._hints.get(hash, None)
