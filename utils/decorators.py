from functools import partial
from typing import Callable


def require_DRIVER(func: Callable):
    def condition(**kwargs):
        driver = kwargs.pop('driver')
        new_func = partial(func, driver=driver)
        return new_func(**kwargs)
    return condition
