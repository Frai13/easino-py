import sys
from easinopy.easino.easino import *
from easinopy.cli.commands._Command import *

class Help(Command):
    cmd = [ '-h', '--help' ]
    args = dict()
    opt_args = dict()
    descr = 'Show easinopy help'

    def run(args_provided):
        version = Easino.get_api_version()
        
        help = ''

        help += f'This is EasIno CLI program to help user executing commands in a fast way.\n'
        help += f'    Version is v{version}\n\n'
        help += f'Command list:\n'
        
        for c in sorted(args_provided, key=lambda a : a.cmd[0]):
            help += f'    {" / ".join(c.cmd)}: {c.descr}\n'
            
            if c.args:
                help += f'    {" ".join(c.args.keys())} {" ".join([f"<{a}>" for a in c.opt_args.keys()])}\n'

        print(help)
