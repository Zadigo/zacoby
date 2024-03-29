from typing import List


class LazyFormat:
    """
    Lazily formats a string until it is called or required.

    Example
    -------

        message = LazyFormat('Kendall {name}', name='Jenner')

        >> str(message)
        >> Kendall Jenner
    """
    __slots__ = ('_cached_result', '_string_to_format', '_args', '_kwargs')

    def __init__(self, string_to_format: str, *args, **kwargs):
        self._cached_result = None
        self._string_to_format = string_to_format
        self._args = args
        self._kwargs = kwargs

    def __str__(self):
        if self._cached_result is None:
            self._cached_result = self._string_to_format\
                    .format(*self._args, **self._kwargs)
            self._string_to_format = None
            self._args = None
            self._kwargs = None
        return self._cached_result

    def __mod__(self, value):
        return str(self) % value
