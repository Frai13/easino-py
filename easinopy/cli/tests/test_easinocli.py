import unittest
import io
import sys
import unittest.mock
from easinopy.cli.easinocli import *
import re

class TestEasInoCli(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @unittest.mock.patch('sys.stderr', new_callable=io.StringIO)
    def parse_args_mocked(self, args, mock_stderr, mock_stdout):
        result = None
        try:
            result = parse_args(args)
        except: pass
        return (result, (mock_stdout.getvalue() + mock_stderr.getvalue()).split('\n'))
    
    def test_version(self):
        result, output = self.parse_args_mocked([ '-v' ])
        self.assertTrue(True in [bool(re.match(r'v\d+\.\d+\.\d+', x)) for x in output])

if __name__ == '__main__':
    unittest.main()
