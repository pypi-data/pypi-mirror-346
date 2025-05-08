import os
from typing import Union

from dotenv import find_dotenv, load_dotenv


def load_parameter(
    value: Union[str, None], env_key: str, env_file: str = ".env"
) -> str:
    """
    Loads a parameter from a provided value or environment variable.

    This function returns the provided `value` if it is not `None`. If `value` is `None`,
    it attempts to retrieve the value from the environment variable specified by `env_key`.
    If the environment variable is not found, a `ValueError` is raised.

    Args:
        value (Union[str, None]): The value to be returned if not `None`. If `None`,
                                  the function will attempt to retrieve the value from the environment variable.
        env_key (str): The key of the environment variable to look up if `value` is `None`.

    Returns:
        str: The `value` if it is not `None`, otherwise the value of the environment variable specified by `env_key`.

    Raises:
        ValueError: If `value` is `None` and the environment variable `env_key` is not set.

    """

    # Find the env file in the current directory or any above
    env_file = find_dotenv(env_file)
    # Load the env file
    load_dotenv(env_file)

    if value is not None:
        return value
    if env_key not in os.environ:
        raise ValueError(f"Missing required env variable {env_key}")
    return os.environ[env_key]
