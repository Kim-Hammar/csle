from typing import List
from unittest.mock import MagicMock
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_common.dao.emulation_observation.attacker.emulation_attacker_machine_observation_state import (
    EmulationAttackerMachineObservationState
)
from csle_common.dao.emulation_observation.common.emulation_port_observation_state import (
    EmulationPortObservationState
)
from csle_common.dao.emulation_observation.common.emulation_vulnerability_observation_state import (
    EmulationVulnerabilityObservationState
)
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_config.credential import Credential


class TestEnvDynamicsUtilSuite:
    """
    Test suite for env_dynamics_util
    """

    def test_merge_os_new_os_detected(self) -> None:
        """
        Test merge_os when a new OS is detected
        """
        o_os = "unknown"
        n_os = "linux"
        merged_os, new_os = EnvDynamicsUtil.merge_os(o_os, n_os)
        assert merged_os == "linux"
        assert new_os == 1

    def test_merge_os_preserve_old_os(self) -> None:
        """
        Test merge_os when new OS is unknown and old OS is known
        """
        o_os = "linux"
        n_os = "unknown"
        merged_os, new_os = EnvDynamicsUtil.merge_os(o_os, n_os)
        assert merged_os == "linux"
        assert new_os == 0

    def test_merge_os_no_change(self) -> None:
        """
        Test merge_os when both are the same
        """
        o_os = "linux"
        n_os = "linux"
        merged_os, new_os = EnvDynamicsUtil.merge_os(o_os, n_os)
        assert merged_os == "linux"
        assert new_os == 0

    def test_merge_ports_empty_new_ports(self) -> None:
        """
        Test merge_ports when new ports list is empty
        """
        o_ports = [
            EmulationPortObservationState(port=22, open=True, service="ssh", protocol=TransportProtocol.TCP)
        ]
        n_ports: List[EmulationPortObservationState] = []
        merged_ports, num_new = EnvDynamicsUtil.merge_ports(o_ports, n_ports)
        assert merged_ports == o_ports
        assert num_new == 0

    def test_merge_ports_new_port_found(self) -> None:
        """
        Test merge_ports when a new port is found
        """
        o_ports = [
            EmulationPortObservationState(port=22, open=True, service="ssh", protocol=TransportProtocol.TCP)
        ]
        n_ports = [
            EmulationPortObservationState(port=80, open=True, service="http", protocol=TransportProtocol.TCP)
        ]
        merged_ports, num_new = EnvDynamicsUtil.merge_ports(o_ports, n_ports, acc=True)
        assert len(merged_ports) == 2
        assert num_new == 1

    def test_merge_ports_no_accumulation(self) -> None:
        """
        Test merge_ports with accumulation disabled
        """
        o_ports = [
            EmulationPortObservationState(port=22, open=True, service="ssh", protocol=TransportProtocol.TCP)
        ]
        n_ports = [
            EmulationPortObservationState(port=80, open=True, service="http", protocol=TransportProtocol.TCP)
        ]
        merged_ports, num_new = EnvDynamicsUtil.merge_ports(o_ports, n_ports, acc=False)
        assert len(merged_ports) == 1
        assert merged_ports[0].port == 80
        assert num_new == 1

    def test_merge_vulnerabilities_empty_new_vulns(self) -> None:
        """
        Test merge_vulnerabilities when new vulnerabilities list is empty
        """
        o_vuln = [
            EmulationVulnerabilityObservationState(name="CVE-2021-1234", port=22, protocol=TransportProtocol.TCP,
                                                   cvss=7.5, credentials=[], service="ssh")
        ]
        n_vuln: List[EmulationVulnerabilityObservationState] = []
        merged_vuln, num_new = EnvDynamicsUtil.merge_vulnerabilities(o_vuln, n_vuln)
        assert merged_vuln == o_vuln
        assert num_new == 0

    def test_merge_vulnerabilities_new_vuln_found(self) -> None:
        """
        Test merge_vulnerabilities when a new vulnerability is found
        """
        o_vuln = [
            EmulationVulnerabilityObservationState(name="CVE-2021-1234", port=22, protocol=TransportProtocol.TCP,
                                                   cvss=7.5, credentials=[], service="ssh")
        ]
        n_vuln = [
            EmulationVulnerabilityObservationState(name="CVE-2021-5678", port=80, protocol=TransportProtocol.TCP,
                                                   cvss=5.0, credentials=[], service="http")
        ]
        merged_vuln, num_new = EnvDynamicsUtil.merge_vulnerabilities(o_vuln, n_vuln, acc=True)
        assert len(merged_vuln) == 2
        assert num_new == 1

    def test_merge_shell_access_new_access(self) -> None:
        """
        Test merge_shell_access when new shell access is gained
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.shell_access = False
        o_m.shell_access_credentials = []

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.shell_access = True
        n_m.shell_access_credentials = [Credential(username="admin", pw="admin", service="ssh")]

        result_m, new_access = EnvDynamicsUtil.merge_shell_access(o_m, n_m)
        assert result_m.shell_access is True
        assert new_access == 1
        assert len(result_m.shell_access_credentials) == 1

    def test_merge_shell_access_preserve_old(self) -> None:
        """
        Test merge_shell_access preserves old access when new has none
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.shell_access = True
        o_m.shell_access_credentials = [Credential(username="admin", pw="admin", service="ssh")]

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.shell_access = False
        n_m.shell_access_credentials = []

        result_m, new_access = EnvDynamicsUtil.merge_shell_access(o_m, n_m)
        assert result_m.shell_access is True
        assert new_access == 0
        assert len(result_m.shell_access_credentials) == 1

    def test_merge_reachable(self) -> None:
        """
        Test merge_reachable combines reachable sets
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.reachable = {"192.168.1.2", "192.168.1.3"}

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.reachable = {"192.168.1.4"}

        result_m = EnvDynamicsUtil.merge_reachable(o_m, n_m)
        assert len(result_m.reachable) == 3
        assert "192.168.1.2" in result_m.reachable
        assert "192.168.1.3" in result_m.reachable
        assert "192.168.1.4" in result_m.reachable

    def test_merge_backdoor_credentials(self) -> None:
        """
        Test merge_backdoor_credentials combines credential lists
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.backdoor_credentials = [Credential(username="backdoor1", pw="pw1", service="ssh")]

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.backdoor_credentials = [Credential(username="backdoor2", pw="pw2", service="ssh")]

        result_m = EnvDynamicsUtil.merge_backdoor_credentials(o_m, n_m)
        assert len(result_m.backdoor_credentials) == 2

    def test_merge_logged_in_new_login(self) -> None:
        """
        Test merge_logged_in when new login occurs
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.logged_in = False

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.logged_in = True

        result_m, num_new = EnvDynamicsUtil.merge_logged_in(o_m, n_m)
        assert result_m.logged_in is True
        assert num_new == 1

    def test_merge_logged_in_preserve_old(self) -> None:
        """
        Test merge_logged_in preserves old login state
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.logged_in = True

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.logged_in = False

        result_m, num_new = EnvDynamicsUtil.merge_logged_in(o_m, n_m)
        assert result_m.logged_in is True
        assert num_new == 0

    def test_merge_tools_installed_new_install(self) -> None:
        """
        Test merge_tools_installed when tools are newly installed
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.tools_installed = False

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.tools_installed = True

        result_m, num_new = EnvDynamicsUtil.merge_tools_installed(o_m, n_m)
        assert result_m.tools_installed is True
        assert num_new == 1

    def test_merge_backdoor_installed_new_install(self) -> None:
        """
        Test merge_backdoor_installed when backdoor is newly installed
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.backdoor_installed = False

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.backdoor_installed = True

        result_m, num_new = EnvDynamicsUtil.merge_backdoor_installed(o_m, n_m)
        assert result_m.backdoor_installed is True
        assert num_new == 1

    def test_merge_backdoor_tried(self) -> None:
        """
        Test merge_backdoor_tried preserves tried flag
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.backdoor_tried = True

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.backdoor_tried = False

        result_m = EnvDynamicsUtil.merge_backdoor_tried(o_m, n_m)
        assert result_m.backdoor_tried is True

    def test_merge_tools_tried(self) -> None:
        """
        Test merge_tools_tried preserves tried flag
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.install_tools_tried = True

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.install_tools_tried = False

        result_m = EnvDynamicsUtil.merge_tools_tried(o_m, n_m)
        assert result_m.install_tools_tried is True

    def test_merge_root_new_root(self) -> None:
        """
        Test merge_root when new root access is gained
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.root = False

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.root = True

        result_m, new_root = EnvDynamicsUtil.merge_root(o_m, n_m)
        assert result_m.root is True
        assert new_root == 1

    def test_merge_flags(self) -> None:
        """
        Test merge_flags combines flag sets
        """
        from csle_common.dao.emulation_config.flag import Flag

        flag1 = Flag(name="flag1", path="/tmp/flag1", dir="/tmp", id=1, requires_root=False, score=10)
        flag2 = Flag(name="flag2", path="/tmp/flag2", dir="/tmp", id=2, requires_root=False, score=20)

        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.flags_found = {flag1}

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.flags_found = {flag2}

        result_m, new_points = EnvDynamicsUtil.merge_flags(o_m, n_m)
        assert len(result_m.flags_found) == 2
        assert new_points == 20

    def test_merge_connections(self) -> None:
        """
        Test merge_connections combines connection lists
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.ssh_connections = [MagicMock()]
        o_m.ftp_connections = []
        o_m.telnet_connections = []

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.ssh_connections = [MagicMock()]
        n_m.ftp_connections = [MagicMock()]
        n_m.telnet_connections = []

        result_m = EnvDynamicsUtil.merge_connections(o_m, n_m)
        assert len(result_m.ssh_connections) == 2
        assert len(result_m.ftp_connections) == 1

    def test_merge_filesystem_scanned(self) -> None:
        """
        Test merge_filesystem_scanned preserves scanned flag
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.filesystem_searched = True

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.filesystem_searched = False

        result_m = EnvDynamicsUtil.merge_filesystem_scanned(o_m, n_m, new_root=0)
        assert result_m.filesystem_searched is True

    def test_merge_filesystem_scanned_reset_on_new_root(self) -> None:
        """
        Test merge_filesystem_scanned resets when new root access gained
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.filesystem_searched = True

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.filesystem_searched = True

        result_m = EnvDynamicsUtil.merge_filesystem_scanned(o_m, n_m, new_root=1)
        assert result_m.filesystem_searched is False

    def test_merge_trace(self) -> None:
        """
        Test merge_trace preserves old trace when new is None
        """
        mock_trace = MagicMock()

        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.trace = mock_trace

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.trace = None

        result_m = EnvDynamicsUtil.merge_trace(o_m, n_m)
        assert result_m.trace == mock_trace

    def test_merge_exploit_tried(self) -> None:
        """
        Test merge_exploit_tried preserves all exploit tried flags
        """
        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.telnet_brute_tried = True
        o_m.ssh_brute_tried = True
        o_m.ftp_brute_tried = False

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.telnet_brute_tried = False
        n_m.ssh_brute_tried = False
        n_m.ftp_brute_tried = False

        result_m = EnvDynamicsUtil.merge_exploit_tried(o_m, n_m)
        assert result_m.telnet_brute_tried is True
        assert result_m.ssh_brute_tried is True
        assert result_m.ftp_brute_tried is False

    def test_check_if_telnet_connection_is_alive(self) -> None:
        """
        Test check_if_telnet_connection_is_alive always returns True
        """
        mock_conn = MagicMock()
        result = EnvDynamicsUtil.check_if_telnet_connection_is_alive(mock_conn)
        assert result is True

    def test_check_if_ftp_connection_is_alive(self) -> None:
        """
        Test check_if_ftp_connection_is_alive always returns True
        """
        mock_conn = MagicMock()
        result = EnvDynamicsUtil.check_if_ftp_connection_is_alive(mock_conn)
        assert result is True

    def test_exploit_tried_flags_ftp(self) -> None:
        """
        Test exploit_tried_flags sets FTP brute tried flag
        """
        action = MagicMock()
        action.id = EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST

        m_obs = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        m_obs.untried_credentials = True

        result = EnvDynamicsUtil.exploit_tried_flags(action, m_obs)
        assert result.ftp_brute_tried is True

    def test_exploit_tried_flags_ssh(self) -> None:
        """
        Test exploit_tried_flags sets SSH brute tried flag
        """
        action = MagicMock()
        action.id = EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST

        m_obs = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])

        result = EnvDynamicsUtil.exploit_tried_flags(action, m_obs)
        assert result.ssh_brute_tried is True

    def test_exploit_tried_flags_sambacry(self) -> None:
        """
        Test exploit_tried_flags sets sambacry tried flag
        """
        action = MagicMock()
        action.id = EmulationAttackerActionId.SAMBACRY_EXPLOIT

        m_obs = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])

        result = EnvDynamicsUtil.exploit_tried_flags(action, m_obs)
        assert result.sambacry_tried is True

    def test_ssh_backdoor_tried_flags(self) -> None:
        """
        Test ssh_backdoor_tried_flags sets backdoor tried flag
        """
        action = MagicMock()
        action.id = EmulationAttackerActionId.SSH_BACKDOOR

        m_obs = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])

        result = EnvDynamicsUtil.ssh_backdoor_tried_flags(action, m_obs)
        assert result.backdoor_tried is True

    def test_install_tools_tried(self) -> None:
        """
        Test install_tools_tried sets install tools tried flag
        """
        action = MagicMock()
        action.id = EmulationAttackerActionId.INSTALL_TOOLS

        m_obs = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])

        result = EnvDynamicsUtil.install_tools_tried(action, m_obs)
        assert result.install_tools_tried is True

    def test_merge_duplicate_machines(self) -> None:
        """
        Test merge_duplicate_machines combines machines with overlapping IPs
        """
        m1 = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        m2 = EmulationAttackerMachineObservationState(ips=["192.168.1.2"])

        action = MagicMock()
        action.id = EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST

        machines = [m1, m2]
        result = EnvDynamicsUtil.merge_duplicate_machines(machines, action)
        assert len(result) == 2

    def test_merge_untried_credentials_preserve(self) -> None:
        """
        Test merge_untried_credentials preserves old state when action is not network login
        """
        action = MagicMock()
        action.id = EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST

        o_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        o_m.untried_credentials = True

        n_m = EmulationAttackerMachineObservationState(ips=["192.168.1.1"])
        n_m.untried_credentials = False
        n_m.shell_access = False

        result_m = EnvDynamicsUtil.merge_untried_credentials(o_m, n_m, action)
        assert result_m.untried_credentials is True

    def test_exploit_get_vuln_name_ftp(self) -> None:
        """
        Test exploit_get_vuln_name returns correct vulnerability name for FTP
        """
        action = MagicMock()
        action.id = EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL

        result = EnvDynamicsUtil.exploit_get_vuln_name(action)
        assert "ftp" in result.lower() or "weak" in result.lower()

    def test_exploit_get_vuln_name_ssh(self) -> None:
        """
        Test exploit_get_vuln_name returns correct vulnerability name for SSH
        """
        action = MagicMock()
        action.id = EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL

        result = EnvDynamicsUtil.exploit_get_vuln_name(action)
        assert "ssh" in result.lower() or "weak" in result.lower()

    def test_exploit_get_service_name_ftp(self) -> None:
        """
        Test exploit_get_service_name returns correct service name for FTP
        """
        action = MagicMock()
        action.id = EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL

        result = EnvDynamicsUtil.exploit_get_service_name(action)
        assert "ftp" in result.lower()

    def test_exploit_get_service_name_ssh(self) -> None:
        """
        Test exploit_get_service_name returns correct service name for SSH
        """
        action = MagicMock()
        action.id = EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL

        result = EnvDynamicsUtil.exploit_get_service_name(action)
        assert "ssh" in result.lower()
