import uuid
from collections import OrderedDict
from functools import partial, wraps

# from zacoby.signals import signal
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
        # signal.connect(listener, signal_name, self)
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
