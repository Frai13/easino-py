import unittest
import io
import os
import unittest.mock
from easinopy.easino.configuration import *

class TestConfiguration(unittest.TestCase):
    def test_generic_config_init(self):
        config = GenericConfiguration()
        self.assertEqual(config.com_type, CommunicationType.NONE)
        self.assertEqual(config.timeout, 2000)
    
    def test_generic_config_serialize(self):
        def helper_serialize(com_type, timeout):
            config = GenericConfiguration(com_type, timeout)
            config._serialize()
            config2 = GenericConfiguration._deserialize()
            self.assertEqual(config2.com_type, com_type)
            self.assertEqual(config2.timeout, timeout)
        
        helper_serialize(CommunicationType.NONE, 2000)
        helper_serialize(CommunicationType.NONE, 0)
        helper_serialize(CommunicationType.NONE, 100)
        helper_serialize(CommunicationType.NONE, -1)
        helper_serialize(CommunicationType.SERIAL, 2000)
        helper_serialize(CommunicationType.SERIAL, 0)
        helper_serialize(CommunicationType.SERIAL, 100)
        helper_serialize(CommunicationType.SERIAL, -1)
    
    def test_generic_config_str(self):
        def helper_str(com_type, timeout):
            config = GenericConfiguration(com_type, timeout)
            self.assertEqual(str(config), f'    - timeout = {timeout}\n')
            
        helper_str(CommunicationType.NONE, 2000)
        helper_str(CommunicationType.NONE, 0)
        helper_str(CommunicationType.NONE, 100)
        helper_str(CommunicationType.NONE, -1)
        helper_str(CommunicationType.SERIAL, 2000)
        helper_str(CommunicationType.SERIAL, 0)
        helper_str(CommunicationType.SERIAL, 100)
        helper_str(CommunicationType.SERIAL, -1)
    
    def test_serial_config_init(self):
        config = SerialComConfiguration()
        self.assertEqual(config.com_type, CommunicationType.SERIAL)
        self.assertEqual(config.com_port, '')
        self.assertEqual(config.baud_rate, 9600)
        self.assertEqual(config.parity, serial.PARITY_NONE)
        self.assertEqual(config.byte_size, serial.EIGHTBITS)
        self.assertEqual(config.stop_bits, serial.STOPBITS_ONE)
        self.assertEqual(config.timeout, 2000)
        
        config = SerialComConfiguration('COM1', 115200, serial.PARITY_EVEN, 6, serial.STOPBITS_ONE_POINT_FIVE, 1500)
        self.assertEqual(config.com_type, CommunicationType.SERIAL)
        self.assertEqual(config.com_port, 'COM1')
        self.assertEqual(config.baud_rate, 115200)
        self.assertEqual(config.parity, serial.PARITY_EVEN)
        self.assertEqual(config.byte_size, serial.SIXBITS)
        self.assertEqual(config.stop_bits, serial.STOPBITS_ONE_POINT_FIVE)
        self.assertEqual(config.timeout, 1500)
        
        def helper_init_serial_com(baud_rate = 9600, parity = serial.PARITY_NONE, byte_size = serial.EIGHTBITS, stop_bits = serial.STOPBITS_ONE):
            SerialComConfiguration(baud_rate=baud_rate, parity=parity, byte_size=byte_size, stop_bits=stop_bits)
        self.assertRaises(ValueError, helper_init_serial_com, baud_rate=100)
        self.assertRaises(ValueError, helper_init_serial_com, baud_rate='9600')
        self.assertRaises(ValueError, helper_init_serial_com, parity=0)
        self.assertRaises(ValueError, helper_init_serial_com, parity='p')
        self.assertRaises(ValueError, helper_init_serial_com, byte_size=4)
        self.assertRaises(ValueError, helper_init_serial_com, byte_size=9)
        self.assertRaises(ValueError, helper_init_serial_com, stop_bits=0)
        self.assertRaises(ValueError, helper_init_serial_com, stop_bits='2')
        
    def test_serial_config_init_list(self):
        def helper_init_list(timeout, com_port, baud_rate, parity, byte_size, stop_bits):
            config = SerialComConfiguration._from_list([com_port, baud_rate, parity, byte_size, stop_bits, timeout])
            self.assertEqual(config.com_type, CommunicationType.SERIAL)
            self.assertEqual(config.com_port, com_port)
            self.assertEqual(config.baud_rate, baud_rate)
            self.assertEqual(config.parity, parity)
            self.assertEqual(config.byte_size, byte_size)
            self.assertEqual(config.stop_bits, stop_bits)
            self.assertEqual(config.timeout, timeout)

        def helper_init_list_exception(baud_rate = 9600, parity = serial.PARITY_NONE, byte_size = serial.EIGHTBITS, stop_bits = serial.STOPBITS_ONE):
            SerialComConfiguration._from_list([baud_rate, parity, byte_size, stop_bits])
        
        helper_init_list(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(100, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(-1, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
    
        helper_init_list(0, 'COM1', 110, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 300, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 1200, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 2400, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 4800, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 14400, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 19200, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 38400, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 57600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 115200, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 128000, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 256000, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        self.assertRaises(ValueError, helper_init_list_exception, baud_rate=1)
        self.assertRaises(ValueError, helper_init_list_exception, baud_rate=-1)
        self.assertRaises(ValueError, helper_init_list_exception, baud_rate=9599)
        
        helper_init_list(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 9600, serial.PARITY_EVEN, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 9600, serial.PARITY_MARK, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 9600, serial.PARITY_ODD, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 9600, serial.PARITY_SPACE, 6, serial.STOPBITS_ONE)
        
        helper_init_list(0, 'COM1', 9600, serial.PARITY_NONE, 5, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 9600, serial.PARITY_NONE, 7, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 9600, serial.PARITY_NONE, 8, serial.STOPBITS_ONE)
        self.assertRaises(ValueError, helper_init_list_exception, byte_size=4)
        self.assertRaises(ValueError, helper_init_list_exception, byte_size=9)
        self.assertRaises(ValueError, helper_init_list_exception, byte_size=0)
        self.assertRaises(ValueError, helper_init_list_exception, byte_size=-1)
        
        helper_init_list(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_init_list(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE_POINT_FIVE)
        helper_init_list(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_TWO)
    
    def test_serial_config_serialize(self):
        def helper_serialize(timeout, com_port, baud_rate, parity, byte_size, stop_bits):
            config = SerialComConfiguration(com_port, baud_rate, parity, byte_size, stop_bits, timeout)
            config._serialize()
            config2 = SerialComConfiguration._deserialize()
            self.assertEqual(config2.com_type, CommunicationType.SERIAL)
            self.assertEqual(config.com_port, com_port)
            self.assertEqual(config.baud_rate, baud_rate)
            self.assertEqual(config.parity, parity)
            self.assertEqual(config.byte_size, byte_size)
            self.assertEqual(config.stop_bits, stop_bits)
            self.assertEqual(config.timeout, timeout)

        def helper_serialize_exception(baud_rate = 9600, parity = serial.PARITY_NONE, byte_size = serial.EIGHTBITS, stop_bits = serial.STOPBITS_ONE):
            config = SerialComConfiguration('', baud_rate, parity, byte_size, stop_bits)
            config._serialize()
            config2 = SerialComConfiguration._deserialize()
        
        helper_serialize(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(100, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(-1, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
    
        helper_serialize(0, 'COM1', 110, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 300, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 1200, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 2400, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 4800, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 14400, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 19200, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 38400, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 57600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 115200, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 128000, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 256000, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        self.assertRaises(ValueError, helper_serialize_exception, baud_rate=1)
        self.assertRaises(ValueError, helper_serialize_exception, baud_rate=-1)
        self.assertRaises(ValueError, helper_serialize_exception, baud_rate=9599)
        
        helper_serialize(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 9600, serial.PARITY_ODD, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 9600, serial.PARITY_EVEN, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 9600, serial.PARITY_MARK, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 9600, serial.PARITY_SPACE, 6, serial.STOPBITS_ONE)
        
        helper_serialize(0, 'COM1', 9600, serial.PARITY_NONE, 5, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 9600, serial.PARITY_NONE, 7, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 9600, serial.PARITY_NONE, 8, serial.STOPBITS_ONE)
        self.assertRaises(ValueError, helper_serialize_exception, byte_size=4)
        self.assertRaises(ValueError, helper_serialize_exception, byte_size=9)
        self.assertRaises(ValueError, helper_serialize_exception, byte_size=0)
        self.assertRaises(ValueError, helper_serialize_exception, byte_size=-1)

        helper_serialize(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_serialize(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_TWO)
        helper_serialize(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE_POINT_FIVE)
    
    def test_serial_config_str(self):
        def helper_str(timeout, com_port, baud_rate, parity, byte_size, stop_bits):
            config = SerialComConfiguration(com_port, baud_rate, parity, byte_size, stop_bits, timeout)
            self.assertEqual(str(config), (
                f'    - baud_rate = {baud_rate}\n' +
                f'    - byte_size = {byte_size}\n' +
                f'    - com_port = {com_port}\n' +
                f'    - parity = {parity}\n' +
                f'    - stop_bits = {stop_bits}\n' +
                f'    - timeout = {timeout}\n'))
            
        helper_str(0, 'COM1', 110, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 300, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 1200, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 2400, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 4800, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 14400, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 19200, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 38400, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 57600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 115200, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 128000, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 256000, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        
        helper_str(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 9600, serial.PARITY_ODD, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 9600, serial.PARITY_EVEN, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 9600, serial.PARITY_MARK, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 9600, serial.PARITY_SPACE, 6, serial.STOPBITS_ONE)
        
        helper_str(0, 'COM1', 9600, serial.PARITY_NONE, 5, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 9600, serial.PARITY_NONE, 7, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 9600, serial.PARITY_NONE, 8, serial.STOPBITS_ONE)

        helper_str(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE)
        helper_str(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_TWO)
        helper_str(0, 'COM1', 9600, serial.PARITY_NONE, 6, serial.STOPBITS_ONE_POINT_FIVE)


if __name__ == '__main__':
    unittest.main()
