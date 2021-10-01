import unittest
from zacoby.driver import Zacoby

driver = Zacoby('')

class TestDriver(unittest.TestCase):
    def test_base_page(self):
        driver.get('http://example.com')
        self.assertEqual(driver.title, 'Exmple Domain')
        
