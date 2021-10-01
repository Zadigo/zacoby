from zacoby.driver import Zacoby
# from zacoby.browsers import capabilities
from zacoby.settings import settings

class EdgeBrowser(Zacoby):
    capabilities = settings.CAPABILITIES.get('EDGE')


class ChromeBrowser(Zacoby):
    capabilities = settings.CAPABILITIES.get('CHROME')
