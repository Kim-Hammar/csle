"""
Tests for csle-cluster constants module.
"""
from csle_cluster.constants.constants import KIBANA_TUNNELS, RYU_TUNNELS, FIVE_G_CORE_TUNNELS


class TestKibanaTunnelsConstants:
    """
    Test suite for KIBANA_TUNNELS constants
    """

    def test_kibana_tunnels_dict_exists(self) -> None:
        """
        Tests that KIBANA_TUNNELS_DICT is defined and is a dict

        :return: None
        """
        assert hasattr(KIBANA_TUNNELS, 'KIBANA_TUNNELS_DICT')
        assert isinstance(KIBANA_TUNNELS.KIBANA_TUNNELS_DICT, dict)

    def test_kibana_tunnels_dict_initially_empty(self) -> None:
        """
        Tests that KIBANA_TUNNELS_DICT is initially empty

        :return: None
        """
        # Note: We check the type, not the exact value, since it may be modified at runtime
        assert isinstance(KIBANA_TUNNELS.KIBANA_TUNNELS_DICT, dict)

    def test_kibana_tunnel_base_port(self) -> None:
        """
        Tests that KIBANA_TUNNEL_BASE_PORT is defined correctly

        :return: None
        """
        assert hasattr(KIBANA_TUNNELS, 'KIBANA_TUNNEL_BASE_PORT')
        assert KIBANA_TUNNELS.KIBANA_TUNNEL_BASE_PORT == 17000
        assert isinstance(KIBANA_TUNNELS.KIBANA_TUNNEL_BASE_PORT, int)

    def test_kibana_thread_property(self) -> None:
        """
        Tests that THREAD_PROPERTY is defined correctly

        :return: None
        """
        assert hasattr(KIBANA_TUNNELS, 'THREAD_PROPERTY')
        assert KIBANA_TUNNELS.THREAD_PROPERTY == "thread"
        assert isinstance(KIBANA_TUNNELS.THREAD_PROPERTY, str)


class TestRyuTunnelsConstants:
    """
    Test suite for RYU_TUNNELS constants
    """

    def test_ryu_tunnels_dict_exists(self) -> None:
        """
        Tests that RYU_TUNNELS_DICT is defined and is a dict

        :return: None
        """
        assert hasattr(RYU_TUNNELS, 'RYU_TUNNELS_DICT')
        assert isinstance(RYU_TUNNELS.RYU_TUNNELS_DICT, dict)

    def test_ryu_tunnels_dict_initially_empty(self) -> None:
        """
        Tests that RYU_TUNNELS_DICT is initially empty

        :return: None
        """
        assert isinstance(RYU_TUNNELS.RYU_TUNNELS_DICT, dict)

    def test_ryu_tunnel_base_port(self) -> None:
        """
        Tests that RYU_TUNNEL_BASE_PORT is defined correctly

        :return: None
        """
        assert hasattr(RYU_TUNNELS, 'RYU_TUNNEL_BASE_PORT')
        assert RYU_TUNNELS.RYU_TUNNEL_BASE_PORT == 18000
        assert isinstance(RYU_TUNNELS.RYU_TUNNEL_BASE_PORT, int)

    def test_ryu_thread_property(self) -> None:
        """
        Tests that THREAD_PROPERTY is defined correctly

        :return: None
        """
        assert hasattr(RYU_TUNNELS, 'THREAD_PROPERTY')
        assert RYU_TUNNELS.THREAD_PROPERTY == "thread"
        assert isinstance(RYU_TUNNELS.THREAD_PROPERTY, str)


class TestFiveGCoreTunnelsConstants:
    """
    Test suite for FIVE_G_CORE_TUNNELS constants
    """

    def test_five_g_core_tunnels_dict_exists(self) -> None:
        """
        Tests that FIVE_G_CORE_TUNNELS_DICT is defined and is a dict

        :return: None
        """
        assert hasattr(FIVE_G_CORE_TUNNELS, 'FIVE_G_CORE_TUNNELS_DICT')
        assert isinstance(FIVE_G_CORE_TUNNELS.FIVE_G_CORE_TUNNELS_DICT, dict)

    def test_five_g_core_tunnels_dict_initially_empty(self) -> None:
        """
        Tests that FIVE_G_CORE_TUNNELS_DICT is initially empty

        :return: None
        """
        assert isinstance(FIVE_G_CORE_TUNNELS.FIVE_G_CORE_TUNNELS_DICT, dict)

    def test_five_g_core_tunnel_base_port(self) -> None:
        """
        Tests that FIVE_G_CORE_TUNNEL_BASE_PORT is defined correctly

        :return: None
        """
        assert hasattr(FIVE_G_CORE_TUNNELS, 'FIVE_G_CORE_TUNNEL_BASE_PORT')
        assert FIVE_G_CORE_TUNNELS.FIVE_G_CORE_TUNNEL_BASE_PORT == 19000
        assert isinstance(FIVE_G_CORE_TUNNELS.FIVE_G_CORE_TUNNEL_BASE_PORT, int)

    def test_five_g_core_thread_property(self) -> None:
        """
        Tests that THREAD_PROPERTY is defined correctly

        :return: None
        """
        assert hasattr(FIVE_G_CORE_TUNNELS, 'THREAD_PROPERTY')
        assert FIVE_G_CORE_TUNNELS.THREAD_PROPERTY == "thread"
        assert isinstance(FIVE_G_CORE_TUNNELS.THREAD_PROPERTY, str)

    def test_five_g_core_webui_port(self) -> None:
        """
        Tests that FIVE_G_CORE_WEBUI_PORT is defined correctly

        :return: None
        """
        assert hasattr(FIVE_G_CORE_TUNNELS, 'FIVE_G_CORE_WEBUI_PORT')
        assert FIVE_G_CORE_TUNNELS.FIVE_G_CORE_WEBUI_PORT == 9999
        assert isinstance(FIVE_G_CORE_TUNNELS.FIVE_G_CORE_WEBUI_PORT, int)


class TestTunnelPortsUnique:
    """
    Test suite to verify tunnel ports are unique across different tunnel types
    """

    def test_base_ports_are_unique(self) -> None:
        """
        Tests that all base ports are unique to avoid port conflicts

        :return: None
        """
        ports = [
            KIBANA_TUNNELS.KIBANA_TUNNEL_BASE_PORT,
            RYU_TUNNELS.RYU_TUNNEL_BASE_PORT,
            FIVE_G_CORE_TUNNELS.FIVE_G_CORE_TUNNEL_BASE_PORT,
        ]
        assert len(ports) == len(set(ports)), "Base ports should be unique"

    def test_base_ports_are_in_valid_range(self) -> None:
        """
        Tests that all base ports are in valid port range (1024-65535)

        :return: None
        """
        ports = [
            KIBANA_TUNNELS.KIBANA_TUNNEL_BASE_PORT,
            RYU_TUNNELS.RYU_TUNNEL_BASE_PORT,
            FIVE_G_CORE_TUNNELS.FIVE_G_CORE_TUNNEL_BASE_PORT,
            FIVE_G_CORE_TUNNELS.FIVE_G_CORE_WEBUI_PORT,
        ]
        for port in ports:
            assert 1024 <= port <= 65535, f"Port {port} is not in valid range"
