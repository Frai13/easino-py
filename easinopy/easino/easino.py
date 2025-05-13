"""
easino module

Provides
  1. EasIno class used to communicate with its protocol.

"""

from enum import IntEnum
from abc import ABC, abstractmethod
import inspect
from easinopy.easino.datacom import *

__version__ = '0.0.1'

import os
import os.path
import time


class DataReceivedArgs:
    """
    A class representing a DataReceivedArgs object that contains information about EasIno received data event.

    Attributes:
        data (DataCom): Data received
    """

    def __init__(self, data) -> None:
        """
        Inits DataReceivedArgs class.
        
        Args:
            data (DataCom): Data received
        """
        self.data = data


class _ReceiveState(IntEnum):
    IDLE = 0
    WAITING = 1
    RECEIVED = 2


class EasIno(ABC):
    """
    A class representing an EasIno communication protocol object.

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

    _data = DataCom()
    _receive_state = _ReceiveState.IDLE
    __data_received_event = []

    @property
    @abstractmethod
    def timeout(self):
        """Timeout of the response received"""
        pass
    
    @abstractmethod
    def start(self):
        """Starts active communication"""
        pass
    
    @abstractmethod
    def stop(self):
        """Stops active communication"""
        pass
    
    @abstractmethod
    def _derived_send(self, line):
        pass

    def subscribe_data_received_callback(self, callback):
        """
        Subscribes to new data received events.
        
        Args:
            callback (Function(DataReceivedArgs)): Will be executed when new data arrives.
        """
        self.__data_received_event.append(callback)

    def unsubscribe_data_received_callback(self, callback):
        """
        Unsubscribes to new data received events.
        
        Args:
            callback (Function): Function that will be removed from callbacks list.
        """
        self.__data_received_event.remove(callback)

    def _call_data_received_callback(self, data_received_args):
        if self._receive_state == _ReceiveState.WAITING:
            self._data = data_received_args.data
            self._receive_state = _ReceiveState.RECEIVED
        else:
            for c in self.__data_received_event:
                c(data_received_args)
    
    def send(self, data):
        """
        Sends data through the active communication.
        
        Args:
            data (DataCom): Data to be sent.
        """
        line = str(data) if data else ''
        self._derived_send(line)
    
    def receive(self, timeout=None):
        """
        Receives data through the active communication until a maximum of specified timeout milliseconds.
        
        Args:
            timeout (int): Milliseconds until timeout.
        
        Returns:
            DataCom: Data received.
        
        Raises:
            TimeoutError : Timeout has been reached before receive any message.
        """
        if timeout is None: 
            timeout = self.timeout
        
        self._receive_state = _ReceiveState.WAITING
        date_now = time.time()
        while self._receive_state != _ReceiveState.RECEIVED:
            if (time.time() - date_now) * 1000 > timeout:
                self._receive_state = _ReceiveState.IDLE
                raise TimeoutError(f'timeout {timeout}ms')
            time.sleep(0.01)
        
        self._receive_state = _ReceiveState.IDLE
        return self._data
    
    def send_and_receive(self, data, timeout=None):
        """
        Sends and receives data through the active communication until a maximum of specified timeout milliseconds.
        
        Args:
            data (DataCom): Data to be sent.
            timeout (int): Milliseconds until timeout.
        
        Returns:
            DataCom: Data received.
        
        Raises:
            TimeoutError : Timeout has been reached before receive any message.
        """
        if timeout is None: 
            timeout = self.timeout
        
        self._receive_state = _ReceiveState.WAITING
        self.send(data)
        return self.receive(timeout)
    
    def try_send_and_receive(self, data, retries, timeout=None):
        """
        Tries to send and receive data a maximum number of retries through the active communication
            until a maximum of specified timeout milliseconds.
        
        Args:
            data (DataCom): Data to be sent.
            retries (int): Maximum number of retries to receive.
            timeout (int): Milliseconds until timeout.
        
        Returns:
            DataCom: Data received.
        
        Raises:
            TimeoutError : Timeout has been reached before receive any message.
        """
        if timeout is None: 
            timeout = self.timeout
        
        i = 0
        while i < retries:
            try:
                self._receive_state = _ReceiveState.WAITING
                self.send(data)
                return self.receive(timeout)
            except:
                i += 1
                if i >= retries:
                    raise
        
        return DataCom()

    
    @staticmethod
    def get_api_version():
        """
        Gets EasInoPy version.
        
        Returns:
            str: EasInoPy version.
        """
        return __version__
    
    def get_board_version(self, timeout=None):
        """
        Request the EasIno board version through the active communication until a maximum of specified timeout milliseconds.
        
        Args:
            timeout (int): Milliseconds until timeout.
        
        Returns:
            str: EasIno board version.
        
        Raises:
            TimeoutError : Timeout has been reached before receive any message.
            NameError : 
        """
        if timeout is None: 
            timeout = self.timeout
        
        data_received = self.send_and_receive(DataCom(operation='VERSION'), timeout)
        if data_received.operation == 'VERSION':
            return data_received.args[0]
        
        raise NameError(f'Incorrect response received')

    