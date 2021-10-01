import uuid
from collections import OrderedDict
from functools import partial, wraps

from zacoby.signals import signal
from zacoby import global_logger

class BaseListeners:
    registry = OrderedDict()

    def __init__(self):
        self.driver = None
        self.listening = False
        self._listeners = OrderedDict()

    def __call__(self, sender, signal):
        s = signal.has_signal(signal)
        if s:
            return signal.send(signal, sender)
        return False

    def __str__(self):
        return str(self._listeners)

    def _register(self, name, listener, signal_name=None):
        current_listeners = self._listeners.keys()
        if name in current_listeners:
            raise TypeError('Listener is alreay registered')
        self._listeners.setdefault(name, [listener, signal_name])
        # Connect each respective signals
        signal.connect(listener, signal_name, self)
        if self._listeners:
            self.listening = True
            self.logger.info(f'Registered listener {name}')
        return self, signal_name

    def _dispatch(self, name):
        event_id = uuid.uuid4()
        self.registry.update({name: event_id})

    def get(self, name):
        return self._listeners.get(name, None)

listeners = BaseListeners()


# def receiver(name):
#     def update_list(func):
#         listeners._register(name, func, signal_name=name)
#         func('driver')
#     return update_list


# def before_navigate_to(func):
#     def updated_listener(**kwargs):
#         return listeners._register(
#             'before_navigate_to', func, signal_name='ListenerSignal.Navigate.Before'
#         )
#     return updated_listener


# def after_navigate_to(func):
#     def updated_listener(**kwargs):
#         return listeners._register(
#             'after_navigate_to', func, signal_name='ListenerSignal.Navigate.After'
#         )
#     return updated_listener


# @receiver('before_navigate_back')
# def before_navigate_back(driver):
#     def inner(*args, **kwargs):
#         return driver
#     return inner

# @before_navigate_back
# def test(driver):
#     pass


# def after_navigate_back(driver):
#     pass


# def before_navigate_forward(driver):
#     pass


# def after_navigate_forward(driver):
#     pass


# def before_find(self, by, value, driver):
#     pass


# def after_find(self, by, value, driver):
#     pass


# def before_click(driver, element):
#     pass


# def after_click(driver, element):
#     pass


# def before_change_value_of(driver, element):
#     pass


# def after_change_value_of(driver, element):
#     pass


# def before_execute_script(script, driver):
#     pass


# def after_execute_script(script, driver):
#     pass


# def before_close(driver):
#     pass


# def after_close(driver):
#     pass


# def before_quit(driver):
#     pass


# def after_quit(driver):
#     pass


# def on_exception(exception, driver):
#     pass
