import pytest

from ..protocol import Schema, Share, Table


class TestTable:
    def test(self):
        table = Table(name="table", share="share", schema="schema")
        assert table.name == "table"
        assert table.share == "share"
        assert table.schema == "schema"

    def test_as_object(self):
        share = Share("share")
        schema = Schema(name="schema", share="share")
        table = Table(name="table", share=share, schema=schema)
        assert table.name == "table"
        assert table.share == "share"
        assert table.schema == "schema"

    def test_not_provided(self):
        with pytest.raises(ValueError):
            Table(name="table", share="share")
        with pytest.raises(ValueError):
            Table(name="table", schema="schema")
        with pytest.raises(ValueError):
            Table(share="share", schema="schema")


class TestSchema:
    def test(self):
        schema = Schema(name="schema", share="share")
        assert schema.name == "schema"
        assert schema.share == "share"

    def test_as_object(self):
        share = Share("share")
        schema = Schema(name="schema", share=share)
        assert schema.name == "schema"
        assert schema.share == "share"

    def test_not_provided(self):
        with pytest.raises(ValueError):
            Schema(share="share")
        with pytest.raises(ValueError):
            Schema(name="schema")
