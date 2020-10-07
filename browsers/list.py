from zacoby.browsers import capabilities as browser_capabilities
from zacoby.dom.mixins import DomElementMixins
from zacoby.driver.base import BaseDriver


class BaseBrowser(DomElementMixins, BaseDriver):
    """Represents a browser"""

class Edge(BaseBrowser):
    """Represents the Edge browser"""
    capabilities = browser_capabilities.EDGE


class Chrome(BaseBrowser):
    """Represents the Chrome browser"""
    capabilities = browser_capabilities.CHROME
