
class Selectors:
    ID = 'id'
    CLASS = 'class'
    TAG_NAME = 'tag'
    X_PATH = 'None'

    def __init__(self, selector=None):
        self.related_function = None
        self._initialized = True
        self.related_functions = {
            'id': 'get_element_by_id',
            'class': 'get_element_by_class',
            'tag': 'get_element_by_tag',
        }
        print(getattr(self, 'get_related_function'))
        if selector is not None:
            self.related_function = self.get_related_function(selector)

    def __getattr__(self, name):
        print(name)
        if name == self.ID:
            raise AttributeError('Something')
        return super().__getattr__(name)

    def get_related_function(self, selected):
        return self.related_functions.get(selected, None)


print(Selectors('id').related_function)
