import os

from parameterized import parameterized_class

from ..utils import load_parameter

CASES = [
    {
        # No value passed, env variable is set
        "environ_key": "KEY",
        "environ_value": "VALUE",
        "value": None,
        "expected": "VALUE",
    },
    {
        # Value passed, env variable is not set
        "environ_key": "KEY",
        "environ_value": None,
        "value": "VALUE2",
        "expected": "VALUE2",
    },
    {
        # Value passed, env variable is set. Value should take precedence
        "environ_key": "KEY",
        "environ_value": "VALUE",
        "value": "VALUE2",
        "expected": "VALUE2",
    },
]


@parameterized_class(CASES)
class TestLoadParameter:
    def test(self):
        if self.environ_value is not None:
            os.environ[self.environ_key] = self.environ_value
        assert load_parameter(self.value, self.environ_key) == self.expected
