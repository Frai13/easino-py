import sys
from easinopy.cli._helper import *


def parse_args(args):

    if len(args) == 0:
        help = Helper.get_commands('-h')
        help[0].run(Helper.get_commands())
        return
    
    cmd = args[0]
    cmd_args = args[1:]
    
    command = Helper.get_commands(cmd)

    if not command:
        print(f'No match for command: {cmd}')
        return
    
    if cmd in ['-h', '--help']:
        command[0].run(Helper.get_commands())
    else:
        command[0].run(cmd_args)

def main():
    sys_args = sys.argv[1:]
    parse_args(sys_args)

if __name__ == '__main__':
    main()