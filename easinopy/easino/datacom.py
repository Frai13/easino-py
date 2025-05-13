"""
datacom module

Provides
  1. DataCom class used to communicate with its protocol.

"""

class DataCom:
    """
    A class representing a DataCom object that contains information exchanged by EasIno communication protocol.

    Attributes:
        operation (str): Operation to be performed.
        args (list): Arguments of the operation.
    """
    
    _HEAD = 'EINO::'
    _TAIL = '::END'
    _SEPARATOR = ';'

    def __init__(self, operation = '', args = []) -> None:
        """
        Inits DataCom class.
        
        Args:
            operation (str): Operation to be performed.
            args (list): Arguments of the operation.
        """
        self.operation = operation
        self.args = args

    @staticmethod
    def _from_str(line):
        datacom = DataCom()

        head_index = line.find(DataCom._HEAD)
        tail_index = line.find(DataCom._TAIL)

        if head_index == -1 or tail_index == -1 or head_index > tail_index:
            return datacom
        
        line_mod = line[head_index+len(DataCom._HEAD):tail_index]
        line_mod = line_mod if not line_mod.endswith(DataCom._SEPARATOR) else line_mod[:-1]

        groups = line_mod.split(DataCom._SEPARATOR)

        datacom.operation = groups[0]
        datacom.args = groups[1:]

        return datacom
    
    def __str__(self):
        """Overrides the default implementation"""
        if len(self.args) > 0:
            return f'{DataCom._HEAD}{self.operation}{DataCom._SEPARATOR}{f"{DataCom._SEPARATOR}".join(self.args)}{DataCom._SEPARATOR}{DataCom._TAIL}'
        else:
            return f'{DataCom._HEAD}{self.operation}{DataCom._SEPARATOR}{DataCom._TAIL}'
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if not isinstance(other, DataCom):
            return False
        
        return (self.operation == other.operation) and (self.args == other.args)
    
    def __ne__(self, other):
        """Overrides the default implementation"""
        return not (self == other)
