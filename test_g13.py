

from __future__ import print_function #py3 makes print a function print()
import unittest
import g13

class g13Test(unittest.TestCase):
    def setUp(self):
        self.g = g13.g13()

    def tearDown(self):
        self.g.cleanup(self.g.dev, self.g.interface)

    def test_isLCDLightOn_True(self):
        self.assertTrue(self.g.isLCDLightOn(128))
        self.assertTrue(self.g.isLCDLightOn(129))

    def test_isLCDLightOn_False(self):
        self.assertFalse(self.g.isLCDLightOn(0))
        self.assertFalse(self.g.isLCDLightOn(64))

if __name__ == '__main__':
    unittest.main()
