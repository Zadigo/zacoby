import base64
from typing import Any, Type

from bs4 import BeautifulSoup
from zacoby.exceptions import SelectorExistsError
from zacoby.page import browser_commands
from zacoby.page.element import DomElement

SELECTORS = {
    'CSS_SELECTOR': 'css selector',
    'LINK_TEXT_SELECTOR': 'link text',
    'PARTIAL_LINK_TEXT_SELECTOR': 'partial link text',
    'TAG_NAME': 'tag name',
    'XPATH_SELECTOR': 'xpath'
}

class LocationMixin:
    """
    List of selectors used in order to locate 
    elements on the DOM
    """
    def _build_strategy(self, selector_name: str, value: Any, dict_to_update: dict={}):
        selector = SELECTORS.get(selector_name, None)
        if selector is None:
            raise SelectorExistsError(selector)
        
        strategy = dict(using=selector, value=value)
        strategy.update(dict_to_update)
        return strategy


class ScreenShotMixin:
    """
    List of selectors used in order to screenshot 
    elements on the DOM
    """

    # def _screen_shot(self, filename: str = None, as_file: bool = False, **kwargs):
    #     response = self.remote_connection._execute_command(
    #         browser_commands.SCREENSHOT, session=self.session_id
    #     )
    #     response_value = response.get('value')
    #     if filename is not None:
    #         try:
    #             with open(filename, 'wb') as f:
    #                 f.write(response_value)
    #         except IOError:
    #             return False
    #         else:
    #             del response_value
    #     else:
    #         return response_value

    # def screen_shot_as_file(self, filename):
    #     return self._screen_shot(filename=filename)

    # def screen_shot_as_png(self, filename=None):
    #     return base64.b64encode(self._screen_shot(filename=filename)).encode('ascii')

    # def screen_shot_as_base64(self):
    #     pass
