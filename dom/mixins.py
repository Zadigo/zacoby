import base64

from zacoby.dom.core import DomElement
from zacoby.dom.strategies import LocationStrategies
from zacoby.service.commands import BrowserCommands


class ScreenShotMixins:
    def _screen_shot(self, filename=None, as_file=False, **kwargs):
        pass

    def screen_shot_as_file(self):
        pass

    def screen_shot_as_png(self):
        pass

    def screen_shot_as_base64(self):
        pass


class LocationMixins:
    """ A set of various methods that can be used to
    interact with the DOM
    """
    dom_element = DomElement()

    def get_element_by_tag_name(self, name):
        parameters = self.location_strategies.build_strategy(
            'TAG_NAME', name, dict_to_update={'session': self.session}
        )
        response = self.new_remote_connection._execute_command(
            BrowserCommands.FIND_ELEMENT,
            **parameters
        )
        return self.dom_element._copy(
            response_value=response['value'],
            self.new_remote_connection
        )

    def _get_elements_by_tag_name(self, name):
        pass

    def get_element_by_id(self, name):
        """Find the first element that matches the given in ID

        Parameters
        ----------

            - name (str): name of the ID to find

        Returns
        -------

            - type: DomElement
        """
        dict_to_update = {'session': self.session}
        response = self.new_remote_connection._run_command(
            BrowserCommands.FIND_ELEMENT,
            self.location_strategies.build_strategy(
                'CSS_SELECTOR', name, dict_to_update=dict_to_update
            )
        )
        return DomElement(response)._copy(None)

    def _get_elements_by_id(self, name):
        pass

    def get_element_by_class(self, name):
        pass

    def _get_elements_by_class(self, name):
        pass

    def get_element_by_xpath(self, xpath, multiple=False):
        pass

    def _get_elements_by_xpath(self, xpath):
        pass

    def get_element_by_link_text(self, text, multiple=False):
        pass

    def _get_elements_by_link_text(self, text):
        pass

    def partial_link_text_match(self, text, multiple=False):
        pass

    def partial_links_text_match(self, text, multiple=False):
        pass

    def get_element_by_name(self, name, multiple=False):
        pass

    def _get_elements_by_name(self, name, multiple=False):
        pass


class SimpleDomMixins(LocationMixins):
    """
    Includes simple mixins such as locating an
    element on the page
    """


class DomElementMixins(LocationMixins, ScreenShotMixins):
    """Regroups all the mixins for the app

    Returns
    -------

        (dict, str, type): a response dictionnary, a value
        or a DomElement class instance is returned
    """
    dom_element = DomElement()
    location_strategies = LocationStrategies()

    @property
    def title(self):
        """
        Return the title of the current HTML document
        """
        command = BrowserCommands.GET_TITLE
        session = self.session
        response = self.new_remote_connection._execute_command(command, session=session)
        return response.get('value', None)

    @property
    def window_size(self):
        pass
    
    @property
    def html(self):
        return self.new_remote_connection._run_command(BrowserCommands.get('getPageSource'))

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
