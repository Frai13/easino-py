"""
easino module

Provides
  1. EasIno class used to communicate with its protocol.

"""

__version__ = '0.0.1'

import os
import os.path

class EasIno:
    """
    A class representing an EasIno communication protocol object.

    Attributes:
        timeout (int): Timeout of the response received.

    Methods:
        get_api_version () -> str: Returns EasInoPy version.
    """
    
    @staticmethod
    def get_api_version():
        """
        Gets EasInoPy version.
        
        Returns:
            str: EasInoPy version.
        """
        return __version__
