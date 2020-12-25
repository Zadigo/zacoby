import hashlib
import re

from zacoby.dom import commands
from zacoby.logger import create_default_logger

class DOMElementMixins:
    def click(self):
        new_command = self._create_url(commands.CLICK_ELEMENT)
        self.logger.info(f'Clicking on element {self.element_id}')
        return self.remote_connection._execute_command(
            new_command, session=self.session_id, element=self.element_value
        )


class DomElement(DOMElementMixins):
    """
    Represents an element (or tag) on the DOM and implements
    additional functionalities to that element
    """
    def __init__(self, response_value=None, driver=None):
        self.logger = create_default_logger(self.__class__.__name__)
        self.response_value = response_value
        self.element_id = None
        self.element_value = None
        self.session_id = None
        self.driver = driver
        self.remote_connection = None
        self._element_url = None

    def __hash__(self):
        return hash(
            self.element_id,
            self.element_value
        )

    @classmethod
    def as_class(cls, response_value, driver=None, remote=None):
        instance = cls(response_value)

        if driver is not None:
            instance.driver = driver
        if remote is not None:
            instance.remote_connection = remote

        key, value = cls._decompose(response_value)
        instance.element_id = key
        instance.element_value = value
        instance.session_id = remote.session_id
        return instance

    @staticmethod
    def _decompose(response_value):
        keys = list(response_value.keys())[0]
        value = list(response_value.values())[0]
        return keys, value

    def _create_url(self, command):
        """
        Creates a new command from an existing command by
        adding the element's ID in the url

        Parameters
        ----------

            command (str): an existing command to modify

        Returns
        -------

            list: the modified command list
        """
        name, characteristics = command
        self._element_url = re.sub(r'\$elementId', self.element_id, characteristics[-1])
        characteristics[1] = self._element_url
        return [name, characteristics]
