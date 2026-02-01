from csle_collector.snort_ids_manager.snort_ids_manager_util import SnortIdsManagerUtil
from csle_collector.snort_ids_manager.snort_ids_manager_pb2 import SnortIdsMonitorDTO, SnortIdsLogDTO


class TestSnortIdsManagerUtilSuite:
    """
    Test suite for SnortIdsManagerUtil
    """

    def test_snort_ids_monitor_dto_to_dict(self) -> None:
        """
        Tests the snort_ids_monitor_dto_to_dict function
        """
        dto = SnortIdsMonitorDTO()
        dto.monitor_running = True
        dto.snort_ids_running = False
        
        d = SnortIdsManagerUtil.snort_ids_monitor_dto_to_dict(dto)
        assert d["monitor_running"] is True
        assert d["snort_ids_running"] is False

    def test_snort_ids_monitor_dto_from_dict(self) -> None:
        """
        Tests the snort_ids_monitor_dto_from_dict function
        """
        d = {
            "monitor_running": False,
            "snort_ids_running": True
        }
        dto = SnortIdsManagerUtil.snort_ids_monitor_dto_from_dict(d)
        assert dto.monitor_running is False
        assert dto.snort_ids_running is True

    def test_snort_ids_log_dto_to_dict(self) -> None:
        """
        Tests the snort_ids_log_dto_to_dict function
        """
        dto = SnortIdsLogDTO()
        dto.timestamp = 123456.0
        dto.ip = "127.0.0.1"
        dto.total_alerts = 10
        
        d = SnortIdsManagerUtil.snort_ids_log_dto_to_dict(dto)
        assert abs(d["timestamp"] - 123456.0) < 1e-3
        assert d["ip"] == "127.0.0.1"
        assert d["total_alerts"] == 10

    def test_snort_ids_log_dto_from_dict(self) -> None:
        """
        Tests the snort_ids_log_dto_from_dict function
        """
        d = {
            "timestamp": 876543.0,
            "ip": "192.168.0.1",
            "total_alerts": 5,
            "attempted_admin_alerts": 0,
            "attempted_user_alerts": 0,
            "inappropriate_content_alerts": 0,
            "policy_violation_alerts": 0,
            "shellcode_detect_alerts": 0,
            "successful_admin_alerts": 0,
            "successful_user_alerts": 0,
            "trojan_activity_alerts": 0,
            "unsuccessful_user_alerts": 0,
            "web_application_attack_alerts": 0,
            "attempted_dos_alerts": 0,
            "attempted_recon_alerts": 0,
            "bad_unknown_alerts": 0,
            "default_login_attempt_alerts": 0,
            "denial_of_service_alerts": 0,
            "misc_attack_alerts": 0,
            "non_standard_protocol_alerts": 0,
            "rpc_portman_decode_alerts": 0,
            "successful_dos_alerts": 0,
            "successful_recon_largescale_alerts": 0,
            "successful_recon_limited_alerts": 0,
            "suspicious_filename_detect_alerts": 0,
            "suspicious_login_alerts": 0,
            "system_call_detect_alerts": 0,
            "unusual_client_port_connection_alerts": 0,
            "web_application_activity_alerts": 0,
            "icmp_event_alerts": 0,
            "misc_activity_alerts": 0,
            "network_scan_alerts": 0,
            "not_suspicious_alerts": 0,
            "protocol_command_decode_alerts": 0,
            "unknown_alerts": 0,
            "tcp_connection_alerts": 0,
            "priority_1_alerts": 0,
            "priority_2_alerts": 0,
            "priority_3_alerts": 0,
            "priority_4_alerts": 0,
            "warning_alerts": 0,
            "severe_alerts": 0,
            "alerts_weighted_by_priority": 0
        }
        dto = SnortIdsManagerUtil.snort_ids_log_dto_from_dict(d)
        assert abs(dto.timestamp - 876543.0) < 1e-3
        assert dto.ip == "192.168.0.1"
        assert dto.total_alerts == 5

    def test_snort_ids_log_dto_empty(self) -> None:
        """
        Tests the snort_ids_log_dto_empty function
        """
        dto = SnortIdsManagerUtil.snort_ids_log_dto_empty()
        assert dto.timestamp == 0
        assert dto.ip == ""

    def test_snort_ids_monitor_dto_empty(self) -> None:
        """
        Tests the snort_ids_monitor_dto_empty function
        """
        dto = SnortIdsManagerUtil.snort_ids_monitor_dto_empty()
        assert dto.monitor_running is False
        assert dto.snort_ids_running is False
