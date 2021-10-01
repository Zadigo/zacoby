import unittest
from zacoby.wait import Wait, Pause


class Driver:
    def something_to_execute(self):
        return True

    def another_to_execute(self):
        return [1, 2]


class TestWait(unittest.TestCase):
    def setUp(self):
        self.wait = Wait('name', Driver(), timeout=5)
        self.pause = Pause(Driver(), timeout=5)

    def test_pause_callback(self):
        def callback(driver, result):
            result.append(driver.something_to_execute())
            
        result = self.pause._start_pause(callback=callback)
        self.assertTrue(result)

    def test_pause_callback2(self):
        def callback(driver, result):
            result.append(driver.another_to_execute())

        result = self.pause._start_pause(callback=callback)
        self.assertListEqual(result, [[1, 2]])

    def test_pause_no_callback(self):
        self.pause._start_pause()

if __name__ == "__main__":
    unittest.main()
