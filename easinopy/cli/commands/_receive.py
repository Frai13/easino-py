import sys
from easinopy.cli.commands._Command import *
from easinopy.cli._common import *
from easinopy import *

class ReceiveData(Command):
    cmd = [ '-r', '--receive' ]
    args = dict()
    opt_args = dict()
    descr = 'Receive data from EasIno board'
    
    @staticmethod
    def data_received(args):
        #print(f'Received \"{args.data.operation}\" with args: {" ".join(args.data.args)}')
        #print(f'Received \"{args.data.operation}\"')
        print('A')

    def run(args_provided):
        try:
            configuration = SerialComConfiguration()._deserialize()
        except:
            print(f'ERROR: no default configuration saved')
            return
        
        try:
            easino = Common.get_easino(configuration)
            easino.subscribe_data_received_callback(ReceiveData.data_received)
            input(f'Waiting data. Press enter to stop.\n')
        except Exception as e:
            print(f'ERROR: {e}')
            return
        
