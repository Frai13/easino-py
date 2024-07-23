from easinopy.cli.commands import _Command, _GetApiVersion, _Help

class Helper:
    def get_commands(cmd = None):
        if cmd:
            return [f for f in _Command.Command.__subclasses__() if cmd in f.cmd]
        else:
            return [f for f in _Command.Command.__subclasses__()]
    
