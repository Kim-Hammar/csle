from csle_common.util.read_emulation_statistics_util import ReadEmulationStatisticsUtil
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters


class TestReadEmulationStatisticsUtilSuite:
    """
    Test suite for read_emulation_statistics_util
    """

    def test_average_host_metrics_single(self) -> None:
        """
        Test average_host_metrics with a single metric
        """
        metric = HostMetrics()
        metric.num_logged_in_users = 5
        metric.num_failed_login_attempts = 10
        metric.num_open_connections = 15
        metric.num_login_events = 20
        metric.num_processes = 100
        metric.num_users = 3

        result = ReadEmulationStatisticsUtil.average_host_metrics([metric])

        assert result.num_logged_in_users == 5
        assert result.num_failed_login_attempts == 10
        assert result.num_open_connections == 15
        assert result.num_login_events == 20
        assert result.num_processes == 100
        assert result.num_users == 3

    def test_average_host_metrics_multiple(self) -> None:
        """
        Test average_host_metrics with multiple metrics (sums values)
        """
        metric1 = HostMetrics()
        metric1.num_logged_in_users = 5
        metric1.num_failed_login_attempts = 10
        metric1.num_open_connections = 15
        metric1.num_login_events = 20
        metric1.num_processes = 100
        metric1.num_users = 3

        metric2 = HostMetrics()
        metric2.num_logged_in_users = 3
        metric2.num_failed_login_attempts = 5
        metric2.num_open_connections = 10
        metric2.num_login_events = 15
        metric2.num_processes = 50
        metric2.num_users = 2

        result = ReadEmulationStatisticsUtil.average_host_metrics([metric1, metric2])

        assert result.num_logged_in_users == 8
        assert result.num_failed_login_attempts == 15
        assert result.num_open_connections == 25
        assert result.num_login_events == 35
        assert result.num_processes == 150
        assert result.num_users == 5

    def test_average_host_metrics_empty(self) -> None:
        """
        Test average_host_metrics with empty list
        """
        result = ReadEmulationStatisticsUtil.average_host_metrics([])

        assert result.num_logged_in_users == 0
        assert result.num_failed_login_attempts == 0
        assert result.num_open_connections == 0
        assert result.num_login_events == 0
        assert result.num_processes == 0
        assert result.num_users == 0

    def test_average_ossec_metrics_single(self) -> None:
        """
        Test average_ossec_metrics with a single metric
        """
        metric = OSSECIdsAlertCounters()
        metric.severe_alerts = 5
        metric.warning_alerts = 10
        metric.total_alerts = 15
        metric.alerts_weighted_by_level = 50

        result = ReadEmulationStatisticsUtil.average_ossec_metrics([metric])

        assert result.severe_alerts == 5
        assert result.warning_alerts == 10
        assert result.total_alerts == 15
        assert result.alerts_weighted_by_level == 50

    def test_average_ossec_metrics_multiple(self) -> None:
        """
        Test average_ossec_metrics with multiple metrics
        """
        metric1 = OSSECIdsAlertCounters()
        metric1.severe_alerts = 5
        metric1.warning_alerts = 10
        metric1.total_alerts = 15
        metric1.alerts_weighted_by_level = 50

        metric2 = OSSECIdsAlertCounters()
        metric2.severe_alerts = 3
        metric2.warning_alerts = 7
        metric2.total_alerts = 10
        metric2.alerts_weighted_by_level = 30

        result = ReadEmulationStatisticsUtil.average_ossec_metrics([metric1, metric2])

        assert result.severe_alerts == 8
        assert result.warning_alerts == 17
        assert result.total_alerts == 25
        assert result.alerts_weighted_by_level == 80

    def test_average_ossec_metrics_empty(self) -> None:
        """
        Test average_ossec_metrics with empty list
        """
        result = ReadEmulationStatisticsUtil.average_ossec_metrics([])

        assert result.severe_alerts == 0
        assert result.warning_alerts == 0
        assert result.total_alerts == 0

    def test_average_snort_metrics_single(self) -> None:
        """
        Test average_snort_metrics with a single metric
        """
        metric = SnortIdsAlertCounters()
        metric.severe_alerts = 5
        metric.warning_alerts = 10
        metric.total_alerts = 15
        metric.alerts_weighted_by_priority = 50

        result = ReadEmulationStatisticsUtil.average_snort_metrics([metric])

        assert result.severe_alerts == 5
        assert result.warning_alerts == 10
        assert result.total_alerts == 15
        assert result.alerts_weighted_by_priority == 50

    def test_average_snort_metrics_multiple(self) -> None:
        """
        Test average_snort_metrics with multiple metrics
        """
        metric1 = SnortIdsAlertCounters()
        metric1.severe_alerts = 5
        metric1.warning_alerts = 10
        metric1.total_alerts = 15
        metric1.alerts_weighted_by_priority = 50

        metric2 = SnortIdsAlertCounters()
        metric2.severe_alerts = 3
        metric2.warning_alerts = 7
        metric2.total_alerts = 10
        metric2.alerts_weighted_by_priority = 30

        result = ReadEmulationStatisticsUtil.average_snort_metrics([metric1, metric2])

        assert result.severe_alerts == 8
        assert result.warning_alerts == 17
        assert result.total_alerts == 25
        assert result.alerts_weighted_by_priority == 80

    def test_average_snort_metrics_empty(self) -> None:
        """
        Test average_snort_metrics with empty list
        """
        result = ReadEmulationStatisticsUtil.average_snort_metrics([])

        assert result.severe_alerts == 0
        assert result.warning_alerts == 0
        assert result.total_alerts == 0

    def test_average_snort_rule_metrics_single(self) -> None:
        """
        Test average_snort_rule_metrics with a single metric
        """
        metric = SnortIdsRuleCounters()
        metric.rule_alerts = {"rule1": 5, "rule2": 10}

        result = ReadEmulationStatisticsUtil.average_snort_rule_metrics([metric])

        assert result.rule_alerts["rule1"] == 5
        assert result.rule_alerts["rule2"] == 10

    def test_average_snort_rule_metrics_multiple(self) -> None:
        """
        Test average_snort_rule_metrics with multiple metrics
        """
        metric1 = SnortIdsRuleCounters()
        metric1.rule_alerts = {"rule1": 5, "rule2": 10}

        metric2 = SnortIdsRuleCounters()
        metric2.rule_alerts = {"rule1": 3, "rule3": 7}

        result = ReadEmulationStatisticsUtil.average_snort_rule_metrics([metric1, metric2])

        assert result.rule_alerts["rule1"] == 8
        assert result.rule_alerts["rule2"] == 10
        assert result.rule_alerts["rule3"] == 7

    def test_average_snort_rule_metrics_empty(self) -> None:
        """
        Test average_snort_rule_metrics with empty list
        """
        result = ReadEmulationStatisticsUtil.average_snort_rule_metrics([])

        assert result.rule_alerts == {}
