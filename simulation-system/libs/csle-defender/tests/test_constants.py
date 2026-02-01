from csle_defender.__version__ import __version__


class TestConstantsSuite:
    """
    Test suite for defender constants
    """

    def test_version(self) -> None:
        """
        Tests the version constant
        """
        assert __version__ is not None
