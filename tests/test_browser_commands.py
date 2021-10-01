import unittest
from zacoby.dom import browser_commands
from zacoby.dom import Command

class TestCommands(unittest.TestCase):
    def test_get_command(self):
        command = browser_commands.GET
        self.assertIsInstance(command, Command)

    def test_contains(self):
        self.assertTrue(browser_commands.has_command('GET'))
        self.assertFalse(browser_commands.has_command('LET'))

    def test_with_element_id(self):
        browser_commands.CLICK_ELEMENT.implement_attribute(
            session_id='test-session-id',
            element_id='test-element-id'
        )
        self.assertEqual(
            browser_commands.CLICK_ELEMENT, 
            '/session/test-session-id/element/test-element-id/click'
        )

    def test_with_session_id(self):
        browser_commands.GET.implement_attribute(session_id='test-session-id')
        self.assertEqual(browser_commands.GET.path, '/session/test-session-id/url')


class TestCommand(unittest.TestCase):
    def setUp(self):
        cmd = ['get', ['POST', '/session/$sessionId/url']]
        command = Command('GET', cmd)
        self.assertEqual(command.path, '/session/$sessionId/url')


if __name__ == '__main__':
    unittest.main()
