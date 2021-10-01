import unittest
from zacoby.dom import mixins
from zacoby.remote import RemoteConnection

class TestMixin(unittest.TestCase):
    def test_location_strategy(self):
        strategies = mixins.LocationStrategies()
        result = strategies._build_strategy('CSS_SELECTOR', {})
        self.assertIsInstance(result, dict)
        self.assertDictEqual(result, {'using': 'css selector', 'value': {}})

    def test_location(self):
        connection = RemoteConnection('127.0.0.1')
        locations = mixins.Location(connection)
        locations.get_element_by('')
        
        


if __name__ == '__main__':
    unittest.main()
