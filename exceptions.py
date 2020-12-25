class SpiderEerror(Exception):
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
