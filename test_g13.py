

from __future__ import print_function #py3 makes print a function print()
import unittest
import random
from operator import add
import g13

class g13Test(unittest.TestCase):
    def setUp(self):
        self.g = g13.g13()
        self.gk, self.lcdk = self.KeysLists()

    def tearDown(self):
        self.g.cleanup()

    def KeysLists(self):
        _GkeyList = {
            "G1": [1,0,0],
            "G2": [2,0,0],
            "G3": [4,0,0],
            "G4": [8,0,0],
            "G5": [16,0,0],
            "G6": [32,0,0],
            "G7": [64,0,0],
            "G8": [128,0,0],
            "G9": [0,1,0],
            "G10": [0,2,0],
            "G11": [0,4,0],
            "G12": [0,8,0],
            "G13": [0,16,0],
            "G14": [0,32,0],
            "G15": [0,64,0],
            "G16": [0,128,0],
            "G17": [0,0,1],
            "G18": [0,0,2],
            "G19": [0,0,4],
            "G20": [0,0,8],
            "G21": [0,0,16],
            "G22": [0,0,32]
        }
        _LCDKeyList = {
            "LCDK1": 1, # Selector
            "LCDK2": 2,
            "LCDK3": 4,
            "LCDK4": 8,
            "LCDK5": 16
        }
        return _GkeyList, _LCDKeyList

    # Check Methods
    def test_getGKeys_G1_22(self):
        for i in range(1,22):
            _Keystr = "G{}".format(i)
            res = self.g.getGKeys(self.gk[_Keystr])
            self.assertEqual(len(res), 1)
            self.assertEqual(res[0], _Keystr)

    def test_getGKeys_MultiKey(self):
        _key1 = random.choice(self.gk.keys())
        _key2 = None
        while True:
            _key2 = random.choice(self.gk.keys())
            if _key1 != _key2:
                break
        _keys = map(add,self.gk[_key1],self.gk[_key2])
        res = self.g.getGKeys(_keys)
        self.assertIn(_key1, res)
        self.assertIn(_key2, res)

    def test_getGKeys_NonExistant_andG1(self):
        _k1 = [1,0,192]
        res = self.g.getGKeys(_k1)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], "G1")

    def test_getLCDKeys_LCDK1_5(self):
        for i in range(1,5):
            _keystr = "LCDK{}".format(i)
            res = self.g.getLCDKeys(self.lcdk[_keystr])
            self.assertEqual(len(res), 1)
            self.assertEqual(res[0], _keystr)

    def test_getDevice_Raise(self):
        with self.assertRaises(ValueError):
            self.g.getDevice(0x0000,0x0000)

    def test_isLCDLightOn_True(self):
        self.assertTrue(self.g.isLCDLightOn(128))
        self.assertTrue(self.g.isLCDLightOn(129))

    def test_isLCDLightOn_False(self):
        self.assertFalse(self.g.isLCDLightOn(0))
        self.assertFalse(self.g.isLCDLightOn(64))

if __name__ == '__main__':
    unittest.main()
