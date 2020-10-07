class LocationStrategies:
    """ Location strategies are a list of selectors
    to be used in order to locate elements on the DOM
    """

    def __init__(self):
        self.selectors = {
            'CSS_SELECTOR': 'css selector',
            'LINK_TEXT_SELECTOR': 'link text',
            'PARTIAL_LINK_TEXT_SELECTOR': 'partial link text',
            'TAG_NAME': 'tag name',
            'XPATH_SELECTOR': 'xpath'
        }

    def __repr__(self):
        return str(self.selectors)

    def build_strategy(self, selector, value, dict_to_update: dict = None):
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
        selector = self.selectors[selector]
        if dict_to_update is not None:
            return dict_to_update.update({'using': selector, 'value': value})
        return dict(selector=selector, value=value)
