import base64

from zacoby.service.commands import BrowserCommands


class DomElementMixins:
    @property
    def title(self):
        """
        Return the title of the current HTML document
        """
        response = self.new_remote_connection._run_command(BrowserCommands.get('getTitle'))
        return response.get('value', None)

    @property
    def window_size(self):
        pass
    
    @property
    def html(self):
        return self._run_command(BrowserCommands.get('getPageSource'))

    def get_element_by_tag_name(self, name, multiple=False):
        pass

    def _get_elements_by_tag_name(self, name):
        pass

    def get_element_by_id(self, name, multiple=False):
        return self._run_command(BrowserCommands.get(''))

    def _get_elements_by_id(self, name):
        pass

    def get_element_by_class(self, name, multiple=False):
        """
        Get an element in the DOM by it's class name

        -----
        
        Parameters
        ----------

            - name (str): the name within the tag

            - multiple (bool, optional): determines whether it should return 
              multiple matching tags. Defaults to False.
        """
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
