KEY = 'key'
POINTER = 'pointer'
NONE = 'none'
SOURCE_TYPES = set([KEY, POINTER, NONE])

POINTER_MOUSE = 'mouse'
POINTER_TOUCH = 'touch'
POINTER_PEN = 'pen'

POINTER_KINDS = set([POINTER_MOUSE, POINTER_TOUCH, POINTER_PEN])


class BaseInteraction:
    def __init__(self, source, action_type, key):
        self.source = source
