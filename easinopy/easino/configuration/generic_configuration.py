"""
generic_configuration module

Provides
  1. CommunicationType enumeration.
  2. GenericConfiguration class used as the base communication configuration.

"""

from enum import IntEnum
import json


class CommunicationType(IntEnum):
    NONE = 0
    SERIAL = 1


class GenericConfiguration(object):
    """
    A class representing a GenericConfiguration object that contains information about EasIno communication configuration.

    Attributes:
        com_type (CommunicationType): Communication type used.
        timeout (int): Timeout of the response received.
    """

    def __init__(self, com_type = CommunicationType.NONE, timeout = 2000) -> None:
        """
        Inits GenericConfiguration class.
        
        Args:
            com_type (CommunicationType): Communication type used.
            timeout (int): Timeout of the response received.
        """
        self.com_type = com_type
        self.timeout = timeout

    def __str__(self):
        """Overrides the default implementation"""
        text = ''
        members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("_")]
        for m in [x for x in members if not isinstance(getattr(self, x), CommunicationType)]:
            text += f'    - {m} = {getattr(self, m)}\n'
        return text

    def _serialize(self):
        text = json.dumps(self.__dict__, sort_keys=True, indent=4)
        with open('CommunicationConfiguration.json', 'w') as f:
            f.write(text)
    
    @staticmethod
    def _deserialize():
        from easinopy.easino.configuration.serial_configuration import SerialComConfiguration

        with open('CommunicationConfiguration.json', 'r') as f:
            text = f.read()
        conf = GenericConfiguration(**{ k: v for k, v in json.loads(text).items() if k == 'com_type' or k == 'timeout'})

        if not conf:
            return GenericConfiguration()
        
        if conf.com_type == CommunicationType.SERIAL:
            return SerialComConfiguration(**{ k.lstrip('_'): v for k, v in json.loads(text).items() if not k == 'com_type'})
        else:
            return conf
    