import sys
from easinopy.cli.commands._Command import *
from easinopy.easino.easino import *

class GetApiVersion(Command):
    cmd = [ '-v', '--version' ]
    args = dict()
    opt_args = dict()
    descr = 'Get easinopy version'

    def run(args_provided):
        version = Easino.get_api_version()
        print(f'v{version}')
