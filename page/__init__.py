import re
from collections import OrderedDict
from functools import cached_property
from importlib import import_module
from typing import Any

from zacoby.exceptions import CommandExistsError

SESSION_ID_PATTERN = re.compile(r'(\$sessionId)')

ELEMENT_ID_PATTERN = re.compile(r'(\$elementId)')


class Command:
    """
    Represents a browser command

    Parameters
    ----------

        name (str): command name
        command (list): command attributes containing a method and a path
    """

    def __init__(self, name: str, command_attrs: list):
        base_name, attrs = self._precheck_attributes(command_attrs)
        self.name = name
        self.base_name = base_name.lower()
        self.attrs = attrs
        self.method = self.attrs[0]
        self.path = self.attrs[1]

    def __str__(self):
        return self.path

    def __repr__(self):
        return f'{self.__class__.__name__}([{self.name}])'

    def __hash__(self):
        return hash(self.name + self.path + self.method + self.base_name)

    def __eq__(self, value: Any):
        logic = [
            # ex. CLICK_ELEMENT
            self.name == value,
            # ex. click_element
            self.name.lower() == value,
            # ex. clickelement
            self.base_name == value,
            # ex. /click/element
            self.path == value
        ]
        return any(logic)

    def _precheck_attributes(self, command: list):
        if not isinstance(command, list):
            raise TypeError('Command should be a list of properties.')

        name, attrs = command
        if not isinstance(attrs, list):
            raise TypeError('Command attributes should be a list containing a method and a path')

        return name, attrs

    def implement_attribute(self, session_id: str=None, element_id: str=None):
        """
        Create a new instance of the path by replacing
        the session ID, the element ID or the ... with
        a given parameter

        Parameters
        ----------

            session_id (str, optional): [description]. Defaults to None.
            element_id (str, optional): [description]. Defaults to None.
        """
        if session_id is not None:
            self.path = SESSION_ID_PATTERN.sub(session_id, self.path)

        if element_id is not None:
            self.path = ELEMENT_ID_PATTERN.sub(element_id, self.path)


class BrowserCommands:
    """
    Contains all the commands that can be sent to the
    browser from the commands module.
    """

    def __init__(self):
        module = import_module('zacoby.page.commands')
        module_dict = module.__dict__

        self._commands = OrderedDict()
        
        for name, attrs in module_dict.items():
            if name.isupper():
                instance = Command(name, attrs)
                self._commands[name.lower()] = instance
                setattr(self, name.lower(), instance)

    def __repr__(self):
        return f"{self.__class__.__name__}(commands={self.__len__()})"

    def __getitem__(self, key):
        return getattr(self, key)

    def __len__(self):
        return len(self.get_all_commands)

    @cached_property
    def get_all_commands(self):
        return self._commands

    def has_command(self, name: str) -> bool:
        return name in self.__dict__

    def get_command(self, name: str) -> Command:
        try:
            return getattr(self, name)
        except AttributeError:
            raise CommandExistsError(name)

browser_commands = BrowserCommands()
