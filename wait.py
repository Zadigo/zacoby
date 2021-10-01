import time
from threading import Timer
from typing import Callable

from pydispatch import dispatcher

from zacoby import global_logger
from zacoby.exceptions import ElementDoesNotExist, MethodError
# from zacoby.pipeline import Pipeline
from zacoby.settings import settings
from zacoby.signals import signal


class DriverMixin:
    def __init__(self, driver: Callable, timeout: int):
        self.driver = driver
        self.timeout = timeout
        # signal.send(dispatcher.Any, self, timeout=timeout)


class Wait(DriverMixin):
    def __init__(self, name: str, driver: Callable, timeout: int=10):
        super().__init__(driver, timeout)
        self.name = name
        self.exceptions = []
        self.results = []

    def _start_polling(self, func, **kwargs):
        # result = None
        # results = []
        end_time = sum([time.time(), self.timeout])
        
        global_logger.info(f'Waiting for element [{self.name}] - ({self.timeout}s)...')
        while True:
            try:
                result = func(driver=self.driver, **kwargs)
            except Exception:
                raise
            else:
                # return result
                self.results.append(result)
            
            time.sleep(self.timeout)
            if time.time() > end_time:
                break
        # raise TimeoutError()

    def until(self, func: Callable, **kwargs):
        self._start_polling(func, **kwargs)
        return self
    
    def until_not(self, func: Callable, **kwargs):
        self._start_polling(func, **kwargs)
        return self

    def chains(self, *funcs: Callable, method='until'):
        authorized_methods = ['until', 'until_not']
        if method not in authorized_methods:
            raise MethodError()
        for func in funcs:
            pass

    def logical_map(self, methods: dict):
        container = []
        for key, method in methods.items():
            container.append(method())
        return self


class Pause(DriverMixin):
    def _start_pause(self, callback = None):
        result = []
        if callback is not None:
            if not callable(callback):
                raise TypeError('Callback should be a callable')
            timer = Timer(self.timeout, function=callback, kwargs={'driver': self.driver, 'result': result})
        else:
            timer = Timer(self.timeout, function=lambda: True)
        timer.start()
        global_logger.info(f'Entering sleep mode ({self.timeout}s)')
        timer.join()
        if not timer.is_alive():
            timer.cancel()
        return result if result else None
