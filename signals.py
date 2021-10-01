from pydispatch import dispatcher

class Signal:
    def connect(self, receiver, signal=dispatcher.Any, sender=dispatcher.Any, **kwargs):
        return dispatcher.connect(receiver, signal=signal, sender=sender, **kwargs)

    def send(self, signal=dispatcher.Any, sender=dispatcher.Any, *arguments, **named):
        return dispatcher.send(signal=signal, sender=sender, *arguments, **named)

signal = Signal()


def receiver(name: str = None):
    def wrapper(func):
        signal.connect(func, signal=name or dispatcher.Any)
    return wrapper


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
