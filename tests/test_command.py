import unittest
from zacoby.dom import Command, browser_commands

class TestCommand(unittest.TestCase):
    def setUp(self):
        test_command = ['clickElement', ['POST', '/session/$sessionId/element/$elementId/click']]
        name, attrs = test_command
        self.command = Command('CLICK_ELEMENT', attrs)

    def test_can_implement_attribute(self):
        self.command.implement_attribute('kendall', 'jenner')
        self.assertEqual(self.command.path, '/session/kendall/element/jenner/click')


class TestBrowserCommands(unittest.TestCase):
    def test_has_commands(self):
        self.assertTrue(len(browser_commands) > 0)
        self.assertTrue(browser_commands.has_command('click_element'))

    def test_can_get_commands(self):
        command = browser_commands.get_command('click_element')
        self.assertIsInstance(command, Command)

        # Tests on command
        command.implement_attribute('kendall', 'jenner')
        self.assertEqual(command.path, '/session/kendall/element/jenner/click')
        self.assertTrue(command == 'click_element')
        self.assertTrue(command == '/session/kendall/element/jenner/click')


if __name__ == '__main__':
    unittest.main()
