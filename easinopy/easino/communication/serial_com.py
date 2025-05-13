"""
serial_com module

Provides
  1. SerialCom class used to communicate with its protocol.

"""

from easinopy.easino.easino import *
from easinopy.easino.datacom import *
from easinopy.easino.configuration import *

import serial
import time
import threading

class SerialCom(EasIno):
    """
    A class representing a SerialCom communication protocol object.

    Attributes:
        timeout (int): Timeout of the response received.

    Methods:
        start () -> None: Starts active communication.
        stop () -> None: Stops active communication.
        subscribe_data_received_callback () -> None: Subscribes to new data received events.
        unsubscribe_data_received_callback () -> None: Unsubscribes to new data received events.
        send (DataCom) -> None: Sends data through the active communication.
        receive (int) -> DataCom: Receives data through the active communication until a maximum of timeout milliseconds.
        send_and_receive (DataCom, int) -> DataCom: Sends and receives data through the active communication until a maximum
            of specified timeout milliseconds.
        try_send_and_receive (DataCom, int, int) -> DataCom: Tries to send and receive data a maximum number of retries through
            the active communication until a maximum of specified timeout milliseconds.
        get_api_version () -> str: Returns EasInoPy version.
        get_board_version (int) -> str: Request the EasIno board version through the active communication until a maximum of specified timeout milliseconds.
    """

    def __init__(self, configuration = None) -> None:
        """
        Inits SerialCom class.
        
        Args:
            configuration (SerialComConfiguration): Serial communication configuration.
        """
        self.__buffer = ''
        self.__started = False
        self.__configuration = configuration
        self.__thread = None
        self.__alive = threading.Event()

        if configuration is None: 
            return
        
        self.__serial_port = serial.Serial()
        self.__serial_port.port = configuration.com_port
        self.__serial_port.baudrate = configuration.baud_rate
        self.__serial_port.parity = configuration.parity
        self.__serial_port.bytesize = configuration.byte_size
        self.__serial_port.stopbits = configuration.stop_bits
        self.__serial_port.dtr = 0
        self.__serial_port.rts = 0

    @property
    def timeout(self):
        return self.__configuration.timeout
    
    @timeout.setter
    def timeout(self, value):
        self.__configuration.timeout = value

    def start(self):
        """Starts active communication"""
        if self.__started:
            return
        self.__started = True
        self.__serial_port.open()
        self.__serial_port.flushInput()
        self.__serial_port.flushOutput()    
        self.__thread = threading.Thread(target=self.__receive_thread)
        self.__thread.daemon = True
        self.__alive.set()
        self.__thread.start()
        time.sleep(2) # Arduino reset when connected to serial port

    def stop(self):
        """Stops active communication"""
        if not self.__started:
            return
        self.__started = False
        self.__serial_port.close()
        if self.__thread is not None:
            self.__alive.clear()
            self.__thread.join()
            self.__thread = None

    def __receive_thread(self):
        while self.__alive.is_set():
            line_rec = str(self.__serial_port.read(self.__serial_port.in_waiting))
            if line_rec:
                self.__buffer += line_rec
                if DataCom._TAIL in self.__buffer:
                    line = self.__buffer
                    self.__buffer = ''
                    if line:
                        #print(len(line))
                        #print(":".join("{:02x}".format(ord(c)) for c in line))
                        data_args = DataReceivedArgs(DataCom._from_str(line))
                        self._call_data_received_callback(data_args)
        
    def _derived_send(self, line):
        if self.__started:
            self.__serial_port.write(bytes(line, 'utf-8'))
