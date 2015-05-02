from .zeroless import *

def version():
    with open('VERSION') as f:
        return f.read().strip()

__version__ = version()