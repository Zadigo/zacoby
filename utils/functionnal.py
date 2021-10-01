import operator
from typing import Any


def create_proxy_function(func):
    def inner(self, *args, **kwargs):
        if self.cached_object is None:
            self._init()
        return func(self.cached_object, *args, **kwargs)
    return inner


class LazyObject:
    cached_object = None

    def __init__(self):
        self.cached_object = None

    def __getattr__(self, name: str):
        if self.cached_object is None:
            self._init()
        return getattr(self.cached_object, name)

    def __setattr__(self, name: str, value: Any):
        if name == 'cached_object':
            self.__dict__['cached_object'] = value
        if self.cached_object is None:
            self._init()
        setattr(self.cached_object, name, value)

    def _init(self):
        raise NotImplemented()

    __dir__ = create_proxy_function(dir)
    __str__ = create_proxy_function(str)
    __repr__ = create_proxy_function(repr)
    __getitem__ = create_proxy_function(operator.getitem)
    __setitem__ = create_proxy_function(operator.setitem)
