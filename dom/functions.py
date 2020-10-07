from zacoby.dom.core import DomElement
from zacoby.dom.strategies import LocationStrategies


class Functions:
    pass


class Expressions(Functions):
    def resolve(self, expression):
        pass


class Q(Expressions):
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


class CaseIf:
    def __init__(self, *cases, default=None):
        pass


class When(Expressions):
    def __init__(self, then_statement, **ifs):
        pass
