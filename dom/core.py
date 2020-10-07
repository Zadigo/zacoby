from zacoby.service.commands import BrowserCommands
from zacoby.dom.strategies import LocationStrategies
import hashlib
# from zacoby.dom.mixins import SimpleDomMixins


class DomElement:
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
    def __init__(self, response_value:dict={}, element_id=None, element_value=None):
        if (response_value and 
                element_id is None and 
                    element_value is None):
            element_id = list(response_value.keys())[-1]
            element_value = list(response_value.values())[-1]
            
        self.element_id = element_id
        self.element_value = element_value
        self.tag_name = None
        self.session = None

    def __repr__(self):
        # class_name = self.tag_name or self.__class__.__name__
        class_name = self.__class__.__name__
        return f'< {class_name} ([{self.element_id}]) >'

    def __eq__(self, element):
        pass

    def __ne__(self, element):
        pass

    def __hash__(self):
        return int(hashlib.md5(self.element_id.encode('UTF-8')).hexdigest(), 16)

    def __setattr__(self, name, value):
        if name == 'tag_name':
            name = name.title()
        super().__setattr__(name, value)

    def _copy(self, element_id=None, element_value=None, response_value=None):
        instance = self.__class__(element_id=element_id, element_value=element_value, response_value=response_value)
        instance.session = self.session
        return instance

    @property
    def text(self):
        command = BrowserCommands.GET_ELEMENT_TEXT
        response = self.new_remote_connection._execute_command(
            BrowserCommands.substitute(command, self.session, self.element_id),
            session = self.session
        )
    
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
