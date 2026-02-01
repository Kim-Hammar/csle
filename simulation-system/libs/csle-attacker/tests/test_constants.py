from csle_attacker.__version__ import __version__


class TestConstantsSuite:
    """
    Test suite for constants in csle-attacker
    """

    def test_version(self) -> None:
        """
        Tests the version constant
        """
        assert __version__ is not None
