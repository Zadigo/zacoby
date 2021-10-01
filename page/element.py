import hashlib
import re
from typing import Any, Callable, Type

from zacoby import global_logger
from zacoby.page import browser_commands


class DOMElementMixin:
    @property
    def is_enabled(self):
        command = browser_commands.get_command('is_element_enabled')
        return self.remote_connection._execute_command(command, requires_session_id=True)

    @property
    def is_visible(self):
        pass

    @property
    def text(self):
        pass

    def _element_meta(self, command: str, attr: str):
        pass

    def get_property(self, attr: str):
        # modified_command = self._element_meta('GET_ELEMENT_PROPERTY', attr)
        # return self._new_request(modified_command)['value']
        pass

    def get_attribute(self, attr: str):
        # modified_command = self._element_meta('GET_ELEMENT_ATTRIBUTE', attr)
        # return self._new_request(modified_command)['value']
        pass

    def clear(self):
        pass

    def click(self):
        # new_command = self._create_url(commands.CLICK_ELEMENT)
        # global_logger.info(f'Clicking on element {self.element_id}')
        # return self.remote_connection._execute_command(
        #     new_command, session=self.session_id, element=self.element_value
        # )
        # browser_commands.CLICK_ELEMENT.implement_attribute(element_id=self.ELEMENT_ID)
        # return self.remote_connection.execute_command(browser_commands.CLICK_ELEMENT)
        command = browser_commands.get_command('click_element')
        return self.remote_connection._execute_command(command, requires_session_id=True, id=self.ELEMENT_ID)
        

    def keyboard_keys(self, value):
        pass

    def tokenized_text(self, using=None):
        from nltk.tokenize import WordPunctTokenizer
        if using is None:
            using = WordPunctTokenizer()
        return using.tokenize(self.text)


class DomElement(DOMElementMixin):
    """
    Represents an element (or tag) on the DOM and implements
    additional functionalities to that element
    """
    remote_connection = None

    def __init__(self, response: Any=None, remote_connection: Callable=None):
        self.response = response

        self.ELEMENT_ID = None
        self.element_value = None

        # self.SESSION_ID = getattr(driver, 'SESSION_ID', None) 

        if remote_connection is not None:
            self.remote_connection = remote_connection
        self._element_url = None

    def __hash__(self):
        return hash(self.ELEMENT_ID, self.element_value)

    @classmethod
    def as_class(cls, response, remote_connection=None):
        instance = cls(response, remote_connection=remote_connection)
        # instance.remote_connection = remote_connection or cls.remote_connection

        # key, value = cls._decompose(response)
        key, value = response.decompose()
        instance.ELEMENT_ID = key
        instance.element_value = value
        # instance.session_id = remote_connection.SESSION_ID
        return instance

    # @staticmethod
    # def _decompose(response):
    #     keys = list(response.keys())[0]
    #     value = list(response.values())[0]
    #     return keys, value
