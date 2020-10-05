from zacoby.driver.base import WebDriver
from zacoby.browsers import capabilities

class Edge(WebDriver):
    """Represents the Edge browser"""
    capabilities = capabilities.EDGE


class Chrome(WebDriver):
    """Represents the Chrome browser"""
    capabilities = capabilities.CHROME
