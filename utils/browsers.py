from zacoby.driver import Zacoby
from zacoby.settings import settings


class Edge(Zacoby):
    capabilities = settings.CAPABILITIES.get('EDGE')


class Chrome(Zacoby):
    capabilities = settings.CAPABILITIES.get('CHROME')
