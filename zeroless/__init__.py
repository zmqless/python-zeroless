from .zeroless import *

def version():
    """
    Returns the version of the zeroless module.

    :rtype: string
    """
    with open('VERSION') as f:
        return f.read().strip()

__version__ = version()