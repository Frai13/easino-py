import unittest
import io
import os
import unittest.mock
from easinopy.easino.easino import *

class TestEasino(unittest.TestCase):
    
    def test_version(self):
        self.assertRegex(Easino.get_api_version(), r'\d+\.\d+\.\d+')

if __name__ == '__main__':
    unittest.main()
