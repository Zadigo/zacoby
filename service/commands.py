from zacoby.utils.datastructures.enumeration import Enum
from string import Template

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
    GET_ELEMENT_TEXT  = ['getElementText', ['GET', '/session/$sessionId/element/$id/text']]

    NEW_SESSION = ['session', ['POST', '/session']]
    
    QUIT = ['quit', ['DELETE', '/session/$sessionId']]

    STATUS = ['GET', ['status', '/status']]

    def substitute(self, command:list, session_id, element_id=None, **kwargs):
        path = command[-1]

        keys = {'session_id': session_id}

        if element_id is not None:
            keys.update({'element_id': element_id})

        keys.update(kwargs)
        new_path = Template(path).substitute(**keys)
        return [command[-0], new_path]