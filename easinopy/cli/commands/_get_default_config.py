import sys
from easinopy.cli.commands._Command import *
from easinopy import *

class GetDefaultConfig(Command):
    cmd = [ '-gdc', '--getdefaultconfig' ]
    args = dict()
    opt_args = dict()
    descr = 'Get communication default configuration'

    def run(args_provided):
        try:
            configuration = SerialComConfiguration()._deserialize()
        except:
            print(f'ERROR: no default configuration saved')
            return
        
        print(configuration)
        print(f'Default configuration read successfully')
