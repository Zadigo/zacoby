from zacoby.utils.datastructures.enumeration import Enum


class BrowserCommands(Enum):
    """
    This class encapsulates all the base commands
    that are sent to the browser in order to
    retrieve elements
    """
    CLOSE = ['close', ['DELETE', '/session/$sessionId/window']]
    
    GET = ['get', ['POST', '/session/$sessionId/url']]
    GET_TITLE = ['getTitle', ['GET', '/session/$sessionId/title']]
    GET_PAGE_SOURCE = ['getPageSource', ['GET', '/session/$sessionId/source']]

    NEW_SESSION = ['session', ['POST', '/session']]
    
    QUIT = ['quit', ['DELETE', '/session/$sessionId']]

    STATUS = ['GET', ['status', '/status']]
