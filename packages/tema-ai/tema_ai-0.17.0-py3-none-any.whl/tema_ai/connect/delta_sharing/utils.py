""" Defines a singleton """

from typing import Any, Dict, Tuple


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    kwd_mark = object()  # sentinel for separating args from kwargs

    def __init__(self, decorated: Any) -> None:
        self._decorated = decorated
        self._instance: Dict[Tuple[Any, ...], str] = {}

    def hash_call(self, *args: Any, **kwargs: Any) -> Tuple[Any, ...]:
        return args + (self.kwd_mark,) + tuple(sorted(kwargs.items()))

    def instance(self, *args: Any, **kwargs: Any) -> str:
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        key = self.hash_call(*args, **kwargs)
        try:
            return self._instance[key]
        except KeyError:
            self._instance[key] = self._decorated(*args, **kwargs)
            return self._instance[key]

    def __call__(self) -> None:
        raise TypeError("Singletons must be accessed through `instance()`.")

    def __instancecheck__(self, inst: Any) -> bool:
        # type: ignore
        return isinstance(inst, self._decorated)
