import base64

from zacoby import commands
from zacoby.dom.element import DomElement


class LocationStrategies:
    """
    Location strategies are a list of selectors
    to be used in order to locate elements on the DOM
    """
    selectors = {
        'CSS_SELECTOR': 'css selector',
        'LINK_TEXT_SELECTOR': 'link text',
        'PARTIAL_LINK_TEXT_SELECTOR': 'partial link text',
        'TAG_NAME': 'tag name',
        'XPATH_SELECTOR': 'xpath'
    }

    def _build_strategy(self, selector, value, dict_to_update: dict = {}):
        """Build a new location strategy in order to get an element on the page

        Parameters
        ---------

            selector (str): the type of attribute to get on the page
            value (str): the value of the attribute to get
            dict_to_update (dict, optional): An additional dict to return. Defaults to None.

        Returns
        -------

            dict: A dictionnary for the new strategy
        """
        selector_value = self.selectors.get(selector, None)
        if selector_value is None:
            raise ValueError(f"{selector_value} is not valid selector. Use: {', '.join(self.selectors.keys())}")

        # strategy = {'strategy': dict(selector=selector_value, value=value)}
        # strategy = {'location_strategy': dict(using=selector_value, value=value)}
        strategy = dict(using=selector_value, value=value)

        if dict_to_update is not None:
            dict_to_update.update(strategy)
        return dict_to_update or strategy


class ScreenShotMixins:
    def _screen_shot(self, filename=None, as_file=False, **kwargs):
        response = self.remote_connection._execute_command(
            commands.SCREENSHOT, session=self.session_id
        )
        response_value = response.get('value')
        if filename is not None:
            try:
                with open(filename, 'wb') as f:
                    f.write(response_value)
            except IOError:
                return False
            else:
                del response_value
        else:
            return response_value

    def screen_shot_as_file(self, filename):
        return self._screen_shot(filename=filename)

    def screen_shot_as_png(self, filename=None):
        return base64.b64encode(self._screen_shot(filename=filename)).encode('ascii')

    def screen_shot_as_base64(self):
        pass

class LocationMixins(LocationStrategies):
    """ A set of various methods that can be used to
    interact with the DOM
    """
    dom_element = DomElement()

    @property
    def title(self):
        """
        Return the title of the current HTML document
        """
        response = self.remote_connection._execute_command(
            commands.GET_TITLE, session=self.session_id
        )
        return response.get('data', None)

    @property
    def html(self):
        response = self.remote_connection._execute_command(
            commands.GET_PAGE_SOURCE, session=self.session_id
        )
        return response.get('data')['value']

    def get_element_by(self, selector, name):
        if selector == 'id':
            return self.get_elements_by_id(name)
        elif selector == 'class':
            return self.get_elements_by_class(name)
        elif selector == 'tag':
            return self.get_element_by_tag_name(name)

    def get_element_by_tag_name(self, name):
        parameters = self._build_strategy(
            'TAG_NAME', name, dict_to_update={'session': self.session_id}
        )
        response = self.remote_connection._execute_command(
            commands.FIND_ELEMENT, **parameters
        )
        return self.dom_element.as_class(
            response['value'], remote=self.remote_connection
        )

    def get_elements_by_tag_name(self, name):
        pass

    def get_element_by_id(self, name):
        pass

    def get_elements_by_id(self, name):
        pass

    def get_element_by_class(self, name):
        pass

    def get_elements_by_class(self, name):
        pass

    def get_element_by_xpath(self, xpath, multiple=False):
        pass

    def get_elements_by_xpath(self, xpath):
        pass

    def get_element_by_link_text(self, text, multiple=False):
        pass

    def get_elements_by_link_text(self, text):
        pass

    def partial_link_text_match(self, text, multiple=False):
        pass

    def partial_links_text_match(self, text, multiple=False):
        pass

    def get_element_by_name(self, name, multiple=False):
        pass

    def get_elements_by_name(self, name, multiple=False):
        pass

    def get_element_text(self, name):
        pass


class DomElementMixins(LocationMixins, ScreenShotMixins):
    """Regroups all the mixins for the app

    Returns
    -------

        (dict, str, type): a response dictionnary, a value
        or a DomElement class instance is returned
    """

    @property
    def window_size(self):
        pass

    def back(self):
        pass

    def forward(self):
        pass

    def refresh(self):
        pass

    def write_skeleton(self):
        """
        From the current element, product a document
        skeleton that will be rendered as a JSON file.

        Returns
        -------

            document structure (dict)

            {
                "html": {
                    position: 0
                    attrs: [],
                    text: ""
                },
                "div": {
                    position 1,
                    attrs: [],
                    text: ""
                },
                "current_item {
                    position: 2,
                    attrs: [],
                    text: ""
                }
            }
        """
        pass
