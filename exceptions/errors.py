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
