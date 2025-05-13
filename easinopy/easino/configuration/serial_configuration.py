"""
serial_configuration module

Provides
  1. SerialComConfiguration class of the serial communication configuration.

"""

from enum import IntEnum
import json
import serial
from easinopy.easino.configuration.generic_configuration import *

class SerialComConfiguration(GenericConfiguration):
    """
    A class representing a SerialComConfiguration object that contains information about EasIno serial communication configuration.

    Attributes:
        com_port (str): System serial port name.
        baud_rate (int): Baud rate to be used in the communication.
            Value should be: 110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000 or 256000
        parity (serial.parity): parity  to be used in the communication.
            Value should be: serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD, serial.PARITY_MARK or serial.PARITY_SPACE
        byte_size (int): Data bits to be used in the communication.
            Value should be: serial.FIVEBITS, serial.SIXBITS, serial.SEVENBITS or serial.EIGHTBITS
        stop_bits (serial.stop_bits): Stop bits to be used in the communication.
            Value should be: serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE or serial.STOPBITS_TWO
        com_type (CommunicationType): Communication type used.
        timeout (int): Timeout of the response received.
    """

    @property
    def baud_rate(self):
        return self._baud_rate
    
    @baud_rate.setter
    def baud_rate(self, value):
        """Value should be: 110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000 or 256000"""
        if (value != 110 and value != 300 and value != 600 and value != 1200 and value != 2400 and value != 4800 and value != 9600 and value != 14400
                    and value != 19200 and value != 38400 and value != 57600 and value != 115200 and value != 128000 and value != 256000):
            raise ValueError(f'baud_rate invalid value {value}')
        self._baud_rate = value

    @property
    def parity(self):
        return self._parity
    
    @parity.setter
    def parity(self, value):
        """Value should be: serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD, serial.PARITY_MARK or serial.PARITY_SPACE"""
        if (value != serial.PARITY_NONE and value != serial.PARITY_EVEN and value != serial.PARITY_ODD and value != serial.PARITY_MARK and value != serial.PARITY_SPACE):
            raise ValueError(f'parity invalid value {value}')
        self._parity = value

    @property
    def byte_size(self):
        return self._byte_size
    
    @byte_size.setter
    def byte_size(self, value):
        """Value should be: serial.FIVEBITS, serial.SIXBITS, serial.SEVENBITS or serial.EIGHTBITS"""
        if value != serial.FIVEBITS and value != serial.SIXBITS and value != serial.SEVENBITS and value != serial.EIGHTBITS:
            raise ValueError(f'byte_size invalid value {value}')
        self._byte_size = value

    @property
    def stop_bits(self):
        return self._stop_bits
    
    @stop_bits.setter
    def stop_bits(self, value):
        """Value should be: serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE or serial.STOPBITS_TWO"""
        if value != serial.STOPBITS_ONE and value != serial.STOPBITS_ONE_POINT_FIVE and value != serial.STOPBITS_TWO:
            raise ValueError(f'stop_bits invalid value {value}')
        self._stop_bits = value

    def __init__(self, com_port = '', baud_rate = 9600, parity = serial.PARITY_NONE, byte_size = 8, stop_bits = serial.STOPBITS_ONE, timeout = 2000) -> None:
        """
        Inits SerialComConfiguration class.
        
        Args:
            com_port (str): System serial port name.
            baud_rate (int): Baud rate to be used in the communication.
            parity (serial.parity): parity  to be used in the communication.
            byte_size (int): Data bits to be used in the communication.
            stop_bits (serial.stop_bits): Stop bits to be used in the communication.
            timeout (int): Timeout of the response received.
        
        Raises:
            ValueError
                baud_rate is not one of: 110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000 or 256000
                parity is not one of: serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD, serial.PARITY_MARK or serial.PARITY_SPACE
                byte_size is not one of: serial.FIVEBITS, serial.SIXBITS, serial.SEVENBITS or serial.EIGHTBITS
                stop_bits is not one of: serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE or serial.STOPBITS_TWO
        """
        self.com_type = CommunicationType.SERIAL
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.parity = parity
        self.byte_size = byte_size
        self.stop_bits = stop_bits
        self.timeout = timeout

    @staticmethod
    def _from_list(args):
        config = SerialComConfiguration()
        config.com_port = args[0] if len(args) >= 1 else config.com_port
        config.baud_rate = args[1] if len(args) >= 2 else config.baud_rate
        config.parity = args[2] if len(args) >= 3 else config.parity
        config.byte_size = args[3] if len(args) >= 4 else config.byte_size
        config.stop_bits = args[4] if len(args) >= 5 else config.stop_bits
        config.timeout = args[5] if len(args) >= 6 else config.timeout
        return config

    def _serialize(self):
        text = json.dumps(self.__dict__, sort_keys=True, indent=4)
        with open('CommunicationConfiguration.json', 'w') as f:
            f.write(text)
    