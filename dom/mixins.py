import base64

from zacoby.service.commands import BrowserCommands
from zacoby.dom.strategies import LocationStrategies

class DomElementMixins:
    """ A set of various methods that can be used to
    interact with the DOM

    Returns
    -------

        (dict, str, type): a response dictionnary, a value
        or a DomElement class instance is returned
    """
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

    def get_element_by_tag_name(self, name):
        pass

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
        return self.new_remote_connection._run_command(
            BrowserCommands.FIND_ELEMENT,
            self.location_strategies.build_strategy('CSS_SELECTOR', name)
        )

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

    def back(self):
        pass

    def forward(self):
        pass

    def refresh(self):
        pass

    def _screen_shot(self, filename=None, as_file=False, **kwargs):
        pass

    def screen_shot_as_file(self):
        pass

    def screen_shot_as_png(self):
        pass

    def screen_shot_as_base64(self):
        pass
