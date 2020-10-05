class BaseExceptions(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class SessionNotCreated(BaseException):
    """
    Session was not created
    """


class CapabilitiesTypeError(BaseException):
    def __init__(self):
        msg = 'The  capabilities attribute should be a dictionnary'
        super().__init__(msg)


class NoResponseError(BaseException):
    """Raises an error when the request to the
    remote server does not return a response"""
    def __init__(self):
        super().__init__(
            'The request did not return a response. It returned None'
        )