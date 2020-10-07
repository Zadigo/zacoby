from zacoby.service.commands import BrowserCommands
from zacoby.dom.mixins import SimpleDomMixins


class DomElement(SimpleDomMixins):
    """
    This class represents a DOM element on which
    multiple other functionnalites can be run a on it.

    Every DOM element retrieved from an HTML page gets
    wrapped within this class

    -----

    Parameters
    ----------

        parent (type): the parent tag of the element as a class
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.tag_name = None

    def __repr__(self):
        class_name = self.tag_name or self.__class__.__name__
        return f'< {class_name} >'

    def __eq__(self, element):
        pass

    def __ne__(self, element):
        pass

    def __hash__(self):
        pass

    def __setattr__(self, name, value):
        if name == 'tag_name':
            name = name.title()
        super().__setattr__(name, value)

    def _copy(self, parent):
        instance = self.__class__(parent=parent)
        return instance

    @property
    def text(self):
        pass
    
    @property
    def is_selected(self):
        pass
    
    @property
    def is_enabled(self):
        pass

    @property
    def is_displayed(self):
        pass

    @property
    def size(self):
        pass

    @property
    def location(self):
        pass

    def css_property(self):
        pass

    def click(self):
        pass

    def submit(self):
        pass

    def clear(self):
        pass

    def get_property(self, name):
        pass

    def get_attribute(self, name):
        pass

    def type_text_into(self, *text):
        pass

    def upload(self, filename):
        pass
