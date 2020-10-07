from zacoby.utils.datastructures.enumeration import Enum


class BrowserCommands(Enum):
    """
    This class encapsulates all the base commands
    that are sent to the browser in order to
    retrieve elements
    """
    CLOSE = ['close', ['DELETE', '/session/$sessionId/window']]

    FIND_ELEMENT = ['findElement', ['POST', '/session/$sessionId/element']]
    FIND_ELEMENTS = ['findElement', ['POST', '/session/$sessionId/elements']]
    FIND_CHILD_ELEMENT = ['findChildElement', ['POST', '/session/$sessionId/element/$id/element']]
    FIND_CHILD_ELEMENTS = ['findChildElements', ['POST', '/session/$sessionId/element/$id/elements']]
    
    GET = ['get', ['POST', '/session/$sessionId/url']]
    GET_TITLE = ['getTitle', ['GET', '/session/$sessionId/title']]
    GET_PAGE_SOURCE = ['getPageSource', ['GET', '/session/$sessionId/source']]
    GET_ELEMENT_TAG_NAME = ['getElementTagName', ['GET', '/session/$sessionId/element/$id/name']]
    GET_CURRENT_URL = ['getCurrentUrl', ['GET', '/session/$sessionId/url']]

    NEW_SESSION = ['session', ['POST', '/session']]
    
    QUIT = ['quit', ['DELETE', '/session/$sessionId']]

    STATUS = ['GET', ['status', '/status']]
