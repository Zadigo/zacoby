from zacoby.actions.interactions import BaseInteraction
from zacoby.actions import interactions
import uuid

class Keys:
    def __init__(self):
        pass


class BaseInteraction:
    def __init__(self, source, action_type, key):
        self.source = source


class Device:
    def __init__(self):
        self.name = uuid.uuid4()
        self.actions = []

    def add_action(self, action):
        pass

    def clear_actions(self):
        self.actions.clear()

    def pause(self):
        pass


class Input(Device):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.input_type = interactions.KEY

    def key_down(self, key):
        self.add_action(BaseInteraction(self, 'keyDown', key))

    def key_up(self, key):
        self.add_action(BaseInteraction(self, "keyUp", key))

    def send_keys(self, text):
        pass
