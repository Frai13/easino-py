import unittest
import io
import os
import unittest.mock
from easinopy.easino.datacom import *

class TestDataCom(unittest.TestCase):
    def test_from_str(self):
        def helper_from_str(line, expected_op, expected_args):
            datacom = DataCom._from_str(line)
            self.assertEqual(datacom.operation, expected_op)
            self.assertEqual(datacom.args, expected_args)
            
        helper_from_str('EINO::hello;world;::END', 'hello', [ 'world' ])
        helper_from_str('EINO::hello;world::END', 'hello', [ 'world' ])
        helper_from_str('EINO::hello;::END', 'hello', [])
        helper_from_str('EINO::hello;;world;::END', 'hello', [ '', 'world' ])
        helper_from_str('EINO::::END', '', [])
        helper_from_str('EINO::hello::END', 'hello', [])
    
        helper_from_str('EINO::hello;world;::EN', '', [])
        helper_from_str('INO::hello;world;::END', '', [])
        helper_from_str('EINO:hello;world;::END', '', [])
        helper_from_str('EINO::hello;world;:END', '', [])
        helper_from_str('hello;world;', '', [])
    
        helper_from_str('beginEINO::hello;world;::ENDend',  'hello', [ 'world' ])
        helper_from_str('beginEINO::hello;world;::END',  'hello', [ 'world' ])
        helper_from_str('EINO::hello;world;::ENDend',  'hello', [ 'world' ])
        helper_from_str(';EINO::hello;world;::END;',  'hello', [ 'world' ])
        helper_from_str(';EINO::hello;world;::END',  'hello', [ 'world' ])
        helper_from_str('EINO::hello;world;::END;',  'hello', [ 'world' ])
        helper_from_str('EINO:: hello ; world ;::END',  ' hello ', [ ' world ' ])
    
        helper_from_str('', '', [])
        
    def test_str(self):
        self.assertEqual(str(DataCom._from_str('EINO::hello;world;::END')), 'EINO::hello;world;::END')
        self.assertEqual(str(DataCom._from_str('EINO::hello;;::END')), 'EINO::hello;;::END')
        self.assertEqual(str(DataCom('hello', [ 'world' ])), 'EINO::hello;world;::END')
        
        self.assertEqual(str(DataCom._from_str('')), 'EINO::;::END')
        self.assertEqual(str(DataCom._from_str('INO::hello;world;::END')), 'EINO::;::END')
        
    def test_eq_ne(self):
        self.assertEqual(DataCom('hello', [ 'world' ]), DataCom._from_str('EINO::hello;world;::END'))
        self.assertEqual(DataCom('hello', [ 'world' ]), DataCom('hello', [ 'world' ]))
        self.assertEqual(DataCom('hello', [ 'world', 'hi' ]), DataCom('hello', [ 'world', 'hi' ]))
        self.assertEqual(DataCom('hello', []), DataCom('hello', []))
        self.assertEqual(DataCom._from_str('EINO::::END'), DataCom('', []))
        self.assertEqual(DataCom(), DataCom('', []))
        
        self.assertNotEqual(DataCom._from_str('EINO::hello;world;::END'), DataCom._from_str('EINO::helo;world;::END'))
        self.assertNotEqual(DataCom._from_str('EINO::hello;world;::END'), DataCom._from_str('EINO::hello;worl;::END'))
        self.assertNotEqual(DataCom._from_str('EINO::hello;::END'), DataCom('hello', [ 'a' ]))
        self.assertNotEqual(DataCom._from_str('EINO::hello;a;::END'), DataCom('hello', []))
        self.assertNotEqual(DataCom._from_str('EINO::hello;a;b;::END'), DataCom('hello', [ 'a' ]))
        self.assertNotEqual(DataCom._from_str('EINO::hello;a;::END'), DataCom('hello', [ 'a', 'b' ]))

if __name__ == '__main__':
    unittest.main()
