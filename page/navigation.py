from typing import Callable

from zacoby.exceptions import SelectorExistsError
from zacoby.page import browser_commands
from zacoby.page.element import DomElement
from zacoby.page.mixins import LocationMixin, ScreenShotMixin


class Location(LocationMixin, ScreenShotMixin):
    """
    A set of methods that can be used to locate or
    interract with elemnts on the HTML page

    Parameters
    ----------

        remote_connection (Type): [description]
    """
    def __init__(self, remote_connection: Callable):
        self.remote_connection = remote_connection
        self.dom_element = DomElement(remote_connection=remote_connection)

    @property
    def title(self):
        command = browser_commands.get_command('get_title')
        response = self.remote_connection._execute_command(command, requires_session_id=True)
        return response.data

    # @property
    # def html(self):
    #     response = self._remote_connection._execute_command(
    #         browser_commands.GET_PAGE_SOURCE, session=self.session_id
    #     )
    #     return response.get('data')['value']

    # @property
    # def text(self):
    #     """
    #     Returns the whole text of the page
    #     """
    #     response = self._remote_connection._execute_command(
    #         browser_commands.TEXT)
    #     return response.get('data')['value']

    # @property
    # def window_size(self):
    #     pass

    def _send_command_to_remote(self, command, requires_session_id=False, **strategy):
        attrs = {
            'command': command,
            'requires_session_id': requires_session_id,
            'remote_connection': self.remote_connection,
            **strategy
        }
        response = self.remote_connection._execute_command(**attrs)
        # return response.get('data', None)
        # return response.data
        return response

    def get_element_by(self, attribute: str, name: str):
        """
        Use an attribute such as ID, CLASS or TAG to
        select an element on the page

        Parameters
        ----------

            attribute (str): ID, CLASS or TAG
            name (str): value within the attribute

        Raises
        ------

            SelectorExistsError: [description]

        Returns
        -------

            [type]: [description]
        """
        if attribute == 'id':
            return self.get_element_by_id(name)
        elif attribute == 'class':
            return self.get_element_by_class(name)
        elif attribute == 'tag':
            return self.get_element_by_tag_name(name)
        else:
            raise SelectorExistsError(name)

    def get_element_by_tag_name(self, name: str):
        strategy = self._build_strategy('TAG_NAME', name)
        command = browser_commands.get_command('find_element')
        response = self._send_command_to_remote(command, requires_session_id=True, **strategy)
        return self.dom_element.as_class(response, remote_connection=self.remote_connection)

    def get_element_by_id(self, name: str):
        strategy = self._build_strategy('CSS_SELECTOR', name)
        command = browser_commands.get_command('find_element')
        response = self._send_command_to_remote(command, requires_session_id=True, **strategy)
        return self.dom_element.as_class(response, remote_connection=self.remote_connection)

    def get_element_by_class(self, name: str):
        strategy = self._build_strategy('CSS_SELECTOR', name)
        command = browser_commands.get_command('find_element')
        response = self._send_command_to_remote(command, requires_session_id=True, **strategy)
        return self.dom_element.as_class(response, remote_connection=self.remote_connection)
        
    # def get_elements_by_tag_name(self, name):
    #     pass

    # def get_element_by_id(self, name):
    #     pass

    # def get_elements_by_id(self, name):
    #     pass

    # def get_element_by_class(self, name):
    #     pass

    # def get_elements_by_class(self, name):
    #     pass

    # def get_element_by_xpath(self, xpath, multiple=False):
    #     pass

    # def get_elements_by_xpath(self, xpath):
    #     pass

    # def get_element_by_link_text(self, text, multiple=False):
    #     pass

    # def get_elements_by_link_text(self, text):
    #     pass

    # def partial_link_text_match(self, text, multiple=False):
    #     pass

    # def partial_links_text_match(self, text, multiple=False):
    #     pass

    # def get_element_by_name(self, name, multiple=False):
    #     pass

    # def get_elements_by_name(self, name, multiple=False):
    #     pass

    # def back(self):
    #     return self._remote_connection._execute_command(
    #         browser_commands.GO_BACK, session=self.session_id
    #     )

    # def forward(self):
    #     return self._remote_connection._execute_command(
    #         browser_commands.GO_FOWARD, session=self.session_id
    #     )

    # def refresh(self):
    #     return self._remote_connection._execute_command(
    #         browser_commands.REFRESH, session=self.session_id
    #     )

    # def as_beautiful_soup(self):
    #     return BeautifulSoup(self.html, 'html.parser')
