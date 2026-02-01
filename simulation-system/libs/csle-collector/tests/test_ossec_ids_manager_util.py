from csle_collector.ossec_ids_manager.ossec_ids_manager_util import OSSecManagerUtil
from csle_collector.ossec_ids_manager.ossec_ids_manager_pb2 import OSSECIdsMonitorDTO, OSSECIdsLogDTO


class TestOSSecManagerUtilSuite:
    """
    Test suite for OSSecManagerUtil
    """

    def test_ossec_ids_monitor_dto_to_dict(self) -> None:
        """
        Tests the ossec_ids_monitor_dto_to_dict function
        """
        dto = OSSECIdsMonitorDTO()
        dto.monitor_running = True
        dto.ossec_ids_running = False
        
        d = OSSecManagerUtil.ossec_ids_monitor_dto_to_dict(dto)
        assert d["monitor_running"] is True
        assert d["ossec_ids_running"] is False

    def test_ossec_ids_monitor_dto_from_dict(self) -> None:
        """
        Tests the ossec_ids_monitor_dto_from_dict function
        """
        d = {
            "monitor_running": False,
            "ossec_ids_running": True
        }
        dto = OSSecManagerUtil.ossec_ids_monitor_dto_from_dict(d)
        assert dto.monitor_running is False
        assert dto.ossec_ids_running is True

    def test_ossec_ids_log_dto_to_dict(self) -> None:
        """
        Tests the ossec_ids_log_dto_to_dict function
        """
        dto = OSSECIdsLogDTO()
        dto.timestamp = 123456.0
        dto.ip = "127.0.0.1"
        dto.total_alerts = 10
        
        d = OSSecManagerUtil.ossec_ids_log_dto_to_dict(dto)
        assert abs(d["timestamp"] - 123456.0) < 1e-3
        assert d["ip"] == "127.0.0.1"
        assert d["total_alerts"] == 10

    def test_ossec_ids_log_dto_from_dict(self) -> None:
        """
        Tests the ossec_ids_log_dto_from_dict function
        """
        d = {
            "timestamp": 876543.0,
            "ip": "192.168.0.1",
            "total_alerts": 5,
            "attempted_admin_alerts": 0,
            "warning_alerts": 0,
            "severe_alerts": 0,
            "alerts_weighted_by_level": 0,
            "level_0_alerts": 0,
            "level_1_alerts": 0,
            "level_2_alerts": 0,
            "level_3_alerts": 0,
            "level_4_alerts": 0,
            "level_5_alerts": 0,
            "level_6_alerts": 0,
            "level_7_alerts": 0,
            "level_8_alerts": 0,
            "level_9_alerts": 0,
            "level_10_alerts": 0,
            "level_11_alerts": 0,
            "level_12_alerts": 0,
            "level_13_alerts": 0,
            "level_14_alerts": 0,
            "level_15_alerts": 0,
            "invalid_login_alerts": 0,
            "authentication_success_alerts": 0,
            "authentication_failed_alerts": 0,
            "connection_attempt_alerts": 0,
            "attacks_alerts": 0,
            "adduser_alerts": 0,
            "sshd_alerts": 0,
            "ids_alerts": 0,
            "firewall_alerts": 0,
            "squid_alerts": 0,
            "apache_alerts": 0,
            "syslog_alerts": 0
        }
        dto = OSSecManagerUtil.ossec_ids_log_dto_from_dict(d)
        assert abs(dto.timestamp - 876543.0) < 1e-3
        assert dto.ip == "192.168.0.1"
        assert dto.total_alerts == 5

    def test_ossec_ids_log_dto_empty(self) -> None:
        """
        Tests the ossec_ids_log_dto_empty function
        """
        dto = OSSecManagerUtil.ossec_ids_log_dto_empty()
        assert dto.timestamp == 0
        assert dto.ip == ""

    def test_ossec_ids_monitor_dto_empty(self) -> None:
        """
        Tests the ossec_ids_monitor_dto_empty function
        """
        dto = OSSecManagerUtil.ossec_ids_monitor_dto_empty()
        assert dto.monitor_running is False
        assert dto.ossec_ids_running is False
