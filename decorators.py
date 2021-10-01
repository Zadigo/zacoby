from functools import partial
from typing import Callable

from pydispatch import dispatcher


def require_DRIVER(func: Callable):
    def condition(**kwargs):
        driver = kwargs.pop('driver')
        new_func = partial(func, driver=driver)
        return new_func(**kwargs)
    return condition


def receiver(name: str=None):
    def wrapper(func):
        from zacoby.signals import signal
        signal.connect(func, signal=name or dispatcher.Any)
    return wrapper
