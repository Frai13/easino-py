from easinopy import *

class Common:

    @staticmethod
    def get_easino(configuration):
        if configuration.com_type == CommunicationType.SERIAL:
            easino = SerialCom(configuration)
            easino.start()
            return easino
        raise TypeError(f'ERROR: cannot create EasIno object')
    