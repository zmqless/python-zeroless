import pytest

from zeroless import (version, __version__)

class TestVersion:
    def test_version(self):
        assert version()
        assert __version__

        assert version() == __version__
