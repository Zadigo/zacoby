class Expressions:
    pass


class Q:
    def __init__(self, *expressions):
        self.element = None

    def __setattr__(self, name, value):
        pass

    def __repr__(self):
        pass

    def __eq__(self, o):
        pass

    def __ne__(self, o):
        pass

    def __and__(self):
        pass
    
    def resolve(self):
        pass
