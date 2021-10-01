# class Pipeline:
#     _resolutions = []

#     def __init__(self, *funcs):
#         self._funcs = list(funcs)

#     @property
#     def resolved_to_true(self):
#         return all(self._resolutions)

#     def resolve(self, driver, name):
#         for func in self._funcs:
#             self._resolutions.append(
#                 func(driver, name)
#             )
#         return self._resolutions


from collections import defaultdict
from typing import Any, Callable, OrderedDict, Tuple



class SequenceAction:
    def __init__(self, driver: Callable, method: str, action: str, param: str=None):
        self.method = method
        self.action = action
        self.param = param

        try:
            function = getattr(driver, self.action)
        except:
            raise ValueError('Driver is not a valid method')
        else:
            self.sequence_method = function

        self.result = function(name=self.param)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.method.upper()} -> {self.action.upper()})'

    @property
    def is_success(self):
        if not isinstance(self.result, bool):
            self.result = False
        return self.result is True


class Sequence:
    """Create a sequence that results in a Truthy or Falsey
    condition and then eventually executes a callback based
    on the result"""
    registry = []

    def __init__(self, *sequences, callback: Callable=None, on_sucess: Any='driver'):
        self.driver = None
        self.sequences = sequences
        self.on_success = on_sucess

    def build_sequences(self):
        for sequence in self.sequences:
            if not isinstance(sequence, str):
                raise ValueError('Action should be a valid string')

            method, action, param = self._parse_action(sequence)
            instance = SequenceAction(self.driver, method, action, param)
            self.registry.append(instance)

    def __str__(self):
        placeholder = '> THEN <'.join(str(sequence) for sequence in self.registry)
        placeholder = f'<{placeholder}>'
        return f'{self.__class__.__name__}({placeholder})'
            
    @staticmethod
    def _parse_action(action):
        method, action, param = action.split('__')
        allowed_actions = ['page', 'element', 'driver']
        if method not in allowed_actions:
            raise ValueError('Method should be one of page, element or driver')
        return method, action, param

    def resolve(self):
        return [sequence.is_success for sequence in self.registry]


class GoToIf(Sequence):
    def resolve(self):
        for sequence in self.registry:
            if sequence.is_sucess:
                self.driver.get('')
                break
    

class EndIf(Sequence):
    def resolve(self):
        results = super().resolve()
        if not all(results):
            self.driver.quit()


# class Driver:
#     def find_element_by_id(self, name):
#         print(name) 

# s = Sequence('page__find_element_by_id__name', 'page__find_element_by_id__surname')
# s.driver = Driver()
# s.build_sequences()
# s.resolve()

g = GoToIf('page__find_elemnt_by_id__name')
