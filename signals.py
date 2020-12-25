from pydispatch import dispatcher

class Signal:
    def connect(self, receiver, signal, sender):
        return dispatcher.connect(
            receiver, signal=signal, sender=sender
        ) 

    def send(self, signal, sender, **kwargs):
        return dispatcher.send(
            signal=signal, sender=sender, **kwargs
        )

signal = Signal()
