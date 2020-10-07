import unittest
from zacoby.dom.mixins import DomElementMixins


class Remote:
    def _execute_command(self, url, **kwargs):
        return {'value': []}

class CustomClass(DomElementMixins):
    session = 'tre-14545-gar'
    
    def __init__(self):
        self.new_remote_connection = Remote()




class TestDomMixins(unittest.TestCase):
    def setUp(self):
        self.mixins = CustomClass()

    def test_returns_an_instance(self):
        div = self.mixins.get_element_by_tag_name('test')
        self.assertNotIsInstance(div, type)


if __name__ == "__main__":
    unittest.main()
