import sys

class Command:

    def __init__(self) -> None:
        cmd = list()
        args = dict()
        opt_args = dict()
        descr = ''
        run = lambda args : None
