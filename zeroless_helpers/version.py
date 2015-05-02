__major_version__ = 0
__minor_version__ = 6
__patch_version__ = 0

def version():
    """
    Returns the version of the zeroless module.

    :rtype: string
    """
    return '{major}.{minor}.{patch}'.format(major=__major_version__,
                                            minor=__minor_version__,
                                            patch=__patch_version__)
