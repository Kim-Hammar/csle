import numpy as np
from csle_common.util.general_util import GeneralUtil


class TestGeneralUtilSuite:
    """
    Test suite for general_util.py
    """

    def test_replace_first_octet_of_ip(self) -> None:
        """
        Tests the replace_first_octet_of_ip function

        :return: None
        """
        assert GeneralUtil.replace_first_octet_of_ip(ip="127.0.0.1", ip_first_octet=1) == "1.0.0.1"
        assert GeneralUtil.replace_first_octet_of_ip(ip="<execution_id>.0.0.1", ip_first_octet=19) == "19.0.0.1"
        assert GeneralUtil.replace_first_octet_of_ip(ip="<execution_id>.125.251.19", ip_first_octet=128) == \
               "128.125.251.19"

    def test_replace_first_octet_of_ip_tuple(self) -> None:
        """
        Tests the replace_first_octet_of_ip_tuple function

        :return: None
        """
        ips = ("127.0.0.1", "192.168.0.1")
        replaced = GeneralUtil.replace_first_octet_of_ip_tuple(ips, 10)
        assert replaced == ("10.0.0.1", "10.168.0.1")

    def test_list_to_tuple(self) -> None:
        """
        Tests the list_to_tuple function

        :return: None
        """
        L = [1, [2, 3], [4, [5, 6]]]
        expected = (1, (2, 3), (4, (5, 6)))
        assert GeneralUtil.list_to_tuple(L) == expected
        assert isinstance(GeneralUtil.list_to_tuple(L), tuple)

    def test_one_hot_encode_integer(self) -> None:
        """
        Tests the one_hot_encode_integer function

        :return: None
        """
        encoded = GeneralUtil.one_hot_encode_integer(value=2, max_value=4)
        expected = np.array([0, 0, 1, 0, 0], dtype=np.int32)
        assert np.array_equal(encoded, expected)

        try:
            GeneralUtil.one_hot_encode_integer(value=5, max_value=4)
            assert False
        except ValueError:
            assert True

    def test_one_hot_encode_vector(self) -> None:
        """
        Tests the one_hot_encode_vector function

        :return: None
        """
        vector = [0, 2, 1]
        max_val = 2
        encoded = GeneralUtil.one_hot_encode_vector(vector, max_val)
        expected = np.array([1, 0, 0, 0, 0, 1, 0, 1, 0], dtype=np.int32)
        assert np.array_equal(encoded, expected)

        try:
            GeneralUtil.one_hot_encode_vector([3, 1], 2)
            assert False
        except ValueError:
            assert True

    def test_get_host_ip(self) -> None:
        """
        Tests the get_host_ip function

        :return: None
        """
        ip = GeneralUtil.get_host_ip()
        assert isinstance(ip, str)
        assert len(ip.split(".")) == 4
