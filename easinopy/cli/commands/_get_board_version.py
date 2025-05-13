import sys
from easinopy.cli.commands._Command import *
from easinopy.cli._common import *
from easinopy import *

class GetBoardVersion(Command):
    cmd = [ '-gbv', '--getboardversion' ]
    args = dict()
    opt_args = dict()
    descr = 'Get EasIno board version'

    def run(args_provided):
        try:
            configuration = SerialComConfiguration()._deserialize()
        except:
            print(f'ERROR: no default configuration saved')
            return
        
        try:
            easino = Common.get_easino(configuration)
            version = easino.get_board_version()
            print(f'EasIno board Version is: {version}')
        except Exception as e:
            print(f'ERROR: {e}')
            return
        
