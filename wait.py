import time

from zacoby.exceptions import ElementDoesNotExist
from zacoby.logger import create_default_logger
from zacoby.pipeline import Pipeline


class Wait:
    def __init__(self, name, driver, timeout=10):
        self.logger = create_default_logger(self.__class__.__name__)
        self.driver = driver
        self.timeout = timeout
        self.name = name
        self.exceptions = []

    def __call__(self, sender, signal):
        self.driver = sender
        self.timeout = 10

    def _start_polling(self, func, name):
        end_time = sum(
            [time.time(), self.timeout]
        )
        self.logger.info('Entering sleep mode...')
        while True:
            try:
                if isinstance(func, Pipeline):
                    func.resolve(self.driver, name)
                    result = func.resolved_to_true
                else:
                    result = func(self.driver, name)
            except:
                self.exceptions.append('Exception')
            else:
                return result
            finally:
                time.sleep(self.timeout)
                if time.time() > end_time:
                    break
        # raise TimeoutError()

    def until(self, func):
        self._start_polling(func, self.name)
        return self
    
    def until_not(self, func):
        self._start_polling(func, self.name)
        return self


class Pause:
    def __init__(self, driver, timeout=10):
        self.driver = driver
    
    def _start_pause(self):
        while True:
            pass
