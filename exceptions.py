class SpiderError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NoReponseError(Exception):
    def __init__(self, *args):
        message = 'No response returned'
        super().__init__(message)


class ServiceError(Exception):
    def __init__(self, *args):
        message = 'The service could not be started. An exception occured'
        super().__init__(message)


class ElementDoesNotExist(Exception):
    def __init__(self, *args):
        message = 'Element does not exist'
        super().__init__(message)


class MethodError(Exception):
    def __init__(self, *args):
        message = 'Method error. Authoriez methods are until, until_not'
        super().__init__(message)


class CommandExistsError(Exception):
    def __init__(self, command: str):
        super().__init__(f"The given command does not exist.")


class SelectorExistsError(Exception):
    def __init__(self, selector: str):
        super().__init__(f"The given selector does not exist.")
