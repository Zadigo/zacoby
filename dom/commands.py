CLICK_ELEMENT = ['clickElement', ['POST', '/session/$sessionId/element/$elementId/click']]
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

SCREENSHOT = ['screenshot', ['GET', '/session/$sessionId/screenshot']]
STATUS = ['GET', ['status', '/status']]
