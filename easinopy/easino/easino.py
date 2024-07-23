'''easino API module.'''

__version__ = '0.0.1'

import os
import os.path

class Easino:
    '''
    A class representing an easino communication protocol object.

    Attributes:
        timeout (int): Timeout of the response received.
    '''
    
    @staticmethod
    def get_api_version():
        '''
        Easino python API version.
        
        Returns:
            str: python API version.
        '''
        return __version__
