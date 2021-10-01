from pydispatch import dispatcher

class Signal:
    def connect(self, receiver, signal=dispatcher.Any, sender=dispatcher.Any, **kwargs):
        return dispatcher.connect(receiver, signal=signal, sender=sender, **kwargs)

    def send(self, signal=dispatcher.Any, sender=dispatcher.Any, *arguments, **named):
        return dispatcher.send(signal=signal, sender=sender, *arguments, **named)

signal = Signal()
