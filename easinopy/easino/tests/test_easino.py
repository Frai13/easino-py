import unittest
import io
import os
import unittest.mock
from easinopy.easino.easino import *

class TestEasIno(unittest.TestCase):
    
    def test_version(self):
        self.assertRegex(EasIno.get_api_version(), r'\d+\.\d+\.\d+')

if __name__ == '__main__':
    unittest.main()
