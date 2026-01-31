import pytest
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.sine_arrival_config import SineArrivalConfig
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.dao.eptmp_arrival_config import EPTMPArrivalConfig
from csle_collector.client_manager.dao.piece_wise_constant_arrival_config import PieceWiseConstantArrivalConfig
from csle_collector.client_manager.dao.spiking_arrival_config import SpikingArrivalConfig
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.host_manager.dao.failed_login_attempt import FailedLoginAttempt
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_collector.host_manager.dao.successful_login import SuccessfulLogin
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert import OSSECIDSAlert
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_alert import SnortIdsAlert
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_collector.snort_ids_manager.dao.snort_ids_fast_log_alert import SnortIdsFastLogAlert
from csle_collector.five_g_core_manager.dao.five_g_core_amf_metrics import FiveGCoreAMFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_hss_metrics import FiveGCoreHSSMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_mme_metrics import FiveGCoreMMEMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_pcf_metrics import FiveGCorePCFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_pcrf_metrics import FiveGCorePCRFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_smf_metrics import FiveGCoreSMFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_upf_metrics import FiveGCoreUPFMetrics
from csle_collector.five_g_cu_manager.dao.five_g_cu_cp_metrics import FiveGCUCPMetrics
from csle_collector.five_g_cu_manager.dao.five_g_cu_app_resource_usage_metrics import FiveGCUAppResourceUsageMetrics
from csle_collector.five_g_cu_manager.dao.five_g_cu_buffer_pool_metrics import FiveGCUBufferPoolMetrics
from csle_collector.five_g_du_manager.dao.five_g_du_metrics import FiveGDUMetrics
from csle_collector.five_g_du_manager.dao.five_g_du_cell_metrics import FiveGDUCellMetrics
from csle_collector.five_g_du_manager.dao.five_g_du_app_resource_usage_metrics import FiveGDUAppResourceUsageMetrics
from csle_collector.five_g_du_manager.dao.five_g_du_buffer_pool_metrics import FiveGDUBufferPoolMetrics
from csle_collector.five_g_du_manager.dao.five_g_du_rlc_metrics import FiveGDURLCMetrics
from csle_collector.five_g_du_manager.dao.five_g_du_low_metrics import FiveGDULowMetrics


@pytest.fixture
def example_constant_arrival_config() -> ConstantArrivalConfig:
    """
    Fixture that returns an example ConstantArrivalConfig object

    :return: an example ConstantArrivalConfig object
    """
    return ConstantArrivalConfig(lamb=10)


@pytest.fixture
def example_sine_arrival_config() -> SineArrivalConfig:
    """
    Fixture that returns an example SineArrivalConfig object

    :return: an example SineArrival object
    """
    return SineArrivalConfig(lamb=0.5, time_scaling_factor=1.0, period_scaling_factor=5.0)


@pytest.fixture
def example_client(example_constant_arrival_config: ConstantArrivalConfig) -> Client:
    """
    Fixture that returns an example Client object

    :return: an example Client object
    """
    return Client(id=1, workflow_distribution=[0.8, 0.2], arrival_config=example_constant_arrival_config)


@pytest.fixture
def example_eptmp_arrival_config() -> EPTMPArrivalConfig:
    """
    Fixture that returns an example EPTMPArrivalConfig object

    :return: an example EPTMPArrivalConfig object
    """
    return EPTMPArrivalConfig(thetas=[0.1, 0.4], gammas=[0.3, 0.6], phis=[0.7], omegas=[0.4, 0.2])


@pytest.fixture
def example_piece_wise_constant_arrival_config() -> PieceWiseConstantArrivalConfig:
    """
    Fixture that returns an example PieceWiseConstantArrivalConfig object

    :return: an example PieceWiseConstantArrivalConfig object
    """
    return PieceWiseConstantArrivalConfig(breakvalues=[1.4, 0.2], breakpoints=[2, 5])


@pytest.fixture
def example_spiking_arrival_config() -> SpikingArrivalConfig:
    """
    Fixture that returns an example SpikingArrivalConfig object

    :return: an example SpikingArrivalConfig object
    """
    return SpikingArrivalConfig(exponents=[0.3, 0.2], factors=[0.4, 0.2])


@pytest.fixture
def example_workflow_markov_chain() -> WorkflowMarkovChain:
    """
    Fixture that returns an example WorkflowMarkovChain object

    :return: an example WorkflowMarkovChain object
    """
    return WorkflowMarkovChain(transition_matrix=[[0.1, 0.9], [0.4, 0.6]], initial_state=5, id=2)


@pytest.fixture
def example_workflow_service() -> WorkflowService:
    """
    Fixture that returns an example WorkflowService object

    :return: an example WorkflowService object
    """
    return WorkflowService(ips_and_commands=[("1.2.2.1", ["command1", "command2"])], id=2)


@pytest.fixture
def example_workflow_config(example_workflow_markov_chain: WorkflowMarkovChain,
                            example_workflow_service: WorkflowService) -> WorkflowsConfig:
    """
    Fixture that returns an example WorkflowsConfig object

    :return: an example WorkflowsConfig object
    """
    return WorkflowsConfig(workflow_markov_chains=[example_workflow_markov_chain],
                           workflow_services=[example_workflow_service])


@pytest.fixture
def example_docker_stats() -> DockerStats:
    """
    Fixture that returns an example DockerStats object

    :return: an example DockerStats object
    """
    return DockerStats(pids=1.2, timestamp="1234567", cpu_percent=1.4, mem_current=56.3, mem_total=100.0,
                       mem_percent=84.0, blk_read=13.2, blk_write=2.0, net_rx=21.0, net_tx=0.2,
                       container_name="example_container1", ip="1.2.3.4", ts=2.3)


@pytest.fixture
def example_failed_login_attempt() -> FailedLoginAttempt:
    """
    Fixture that returns an example FailedLoginAttempt object

    :return: an example FailedLoginAttempt object
    """
    return FailedLoginAttempt()


@pytest.fixture
def example_host_metrics() -> HostMetrics:
    """
    Fixture that returns an example HostMetrics object

    :return: an example HostMetrics object
    """
    return HostMetrics(num_logged_in_users=1, num_failed_login_attempts=10, num_open_connections=1, num_login_events=2,
                       num_processes=5, num_users=1, ip="1.1.1.1", ts=0.5)


@pytest.fixture
def example_successful_login() -> SuccessfulLogin:
    """
    Fixture that returns an example SuccessfulLogin object

    :return: an example SuccessfulLogin object
    """
    return SuccessfulLogin()


@pytest.fixture
def example_ossec_ids_alert() -> OSSECIDSAlert:
    """
    Fixture that returns an example OSSECIDSAlert object

    :return: an example OSSECIDSAlert object
    """
    return OSSECIDSAlert(timestamp=12345.2, groups=["group1", "group2"], host="host1", ip="1.2.3.4",
                         rule_id="admin", level=1, descr="231", src="292", user="user1")


@pytest.fixture
def example_ossec_ids_alert_counters() -> OSSECIdsAlertCounters:
    """
    Fixture that returns an example OSSECIdsAlertCounters object

    :return: an example OSSECIdsAlertCounters object
    """
    return OSSECIdsAlertCounters()


@pytest.fixture
def example_snort_ids_alert() -> SnortIdsAlert:
    """
    Fixture that returns an example SnortIdsAlert object

    :return: an example SnortIdsAlert object
    """
    return SnortIdsAlert()


@pytest.fixture
def example_snort_ids_alert_counters() -> SnortIdsAlertCounters:
    """
    Fixture that returns an example SnortIdsAlertCounters object

    :return: an example SnortIdsAlertCounters object
    """
    return SnortIdsAlertCounters()


@pytest.fixture
def example_snort_ids_ip_alert_counters() -> SnortIdsIPAlertCounters:
    """
    Fixture that returns an example SnortIdsIPAlertCounters object

    :return: an example SnortIdsIPAlertCounters object
    """
    return SnortIdsIPAlertCounters()


@pytest.fixture
def example_snort_ids_rule_counters() -> SnortIdsRuleCounters:
    """
    Fixture that returns an example SnortIdsRuleCounters object

    :return: an example SnortIdsRuleCounters object
    """
    return SnortIdsRuleCounters()


@pytest.fixture
def example_snort_ids_fast_alert() -> SnortIdsFastLogAlert:
    """
    Fixture that returns an example SnortIdsFastLogAlert object

    :return: an example SnortIdsFastLogAlert object
    """
    return SnortIdsFastLogAlert(timestamp=1234.4, priority=1, class_id=1, source_ip="1.2.3.4", target_ip="2.3.4.1",
                                rule_id="1")


@pytest.fixture
def example_five_g_core_amf_metrics() -> FiveGCoreAMFMetrics:
    """
    Fixture that returns an example FiveGCoreAMFMetrics object

    :return: an example FiveGCoreAMFMetrics object
    """
    return FiveGCoreAMFMetrics()


@pytest.fixture
def example_five_g_core_hss_metrics() -> FiveGCoreHSSMetrics:
    """
    Fixture that returns an example FiveGCoreHSSMetrics object

    :return: an example FiveGCoreHSSMetrics object
    """
    return FiveGCoreHSSMetrics()


@pytest.fixture
def example_five_g_core_mme_metrics() -> FiveGCoreMMEMetrics:
    """
    Fixture that returns an example FiveGCoreMMEMetrics object

    :return: an example FiveGCoreMMEMetrics object
    """
    return FiveGCoreMMEMetrics()


@pytest.fixture
def example_five_g_core_pcf_metrics() -> FiveGCorePCFMetrics:
    """
    Fixture that returns an example FiveGCorePCFMetrics object

    :return: an example FiveGCorePCFMetrics object
    """
    return FiveGCorePCFMetrics()


@pytest.fixture
def example_five_g_core_pcrf_metrics() -> FiveGCorePCRFMetrics:
    """
    Fixture that returns an example FiveGCorePCRFMetrics object

    :return: an example FiveGCorePCRFMetrics object
    """
    return FiveGCorePCRFMetrics()


@pytest.fixture
def example_five_g_core_smf_metrics() -> FiveGCoreSMFMetrics:
    """
    Fixture that returns an example FiveGCoreSMFMetrics object

    :return: an example FiveGCoreSMFMetrics object
    """
    return FiveGCoreSMFMetrics()


@pytest.fixture
def example_five_g_core_upf_metrics() -> FiveGCoreUPFMetrics:
    """
    Fixture that returns an example FiveGCoreUPFMetrics object

    :return: an example FiveGCoreUPFMetrics object
    """
    return FiveGCoreUPFMetrics()


@pytest.fixture
def example_five_g_cu_cp_metrics() -> FiveGCUCPMetrics:
    """
    Fixture that returns an example FiveGCUCPMetrics object

    :return: an example FiveGCUCPMetrics object
    """
    return FiveGCUCPMetrics()


@pytest.fixture
def example_five_g_cu_app_resource_usage_metrics() -> FiveGCUAppResourceUsageMetrics:
    """
    Fixture that returns an example FiveGCUAppResourceUsageMetrics object

    :return: an example FiveGCUAppResourceUsageMetrics object
    """
    return FiveGCUAppResourceUsageMetrics()


@pytest.fixture
def example_five_g_cu_buffer_pool_metrics() -> FiveGCUBufferPoolMetrics:
    """
    Fixture that returns an example FiveGCUBufferPoolMetrics object

    :return: an example FiveGCUBufferPoolMetrics object
    """
    return FiveGCUBufferPoolMetrics()


@pytest.fixture
def example_five_g_du_metrics() -> FiveGDUMetrics:
    """
    Fixture that returns an example FiveGDUMetrics object

    :return: an example FiveGDUMetrics object
    """
    return FiveGDUMetrics()


@pytest.fixture
def example_five_g_du_cell_metrics() -> FiveGDUCellMetrics:
    """
    Fixture that returns an example FiveGDUCellMetrics object

    :return: an example FiveGDUCellMetrics object
    """
    return FiveGDUCellMetrics()


@pytest.fixture
def example_five_g_du_app_resource_usage_metrics() -> FiveGDUAppResourceUsageMetrics:
    """
    Fixture that returns an example FiveGDUAppResourceUsageMetrics object

    :return: an example FiveGDUAppResourceUsageMetrics object
    """
    return FiveGDUAppResourceUsageMetrics()


@pytest.fixture
def example_five_g_du_buffer_pool_metrics() -> FiveGDUBufferPoolMetrics:
    """
    Fixture that returns an example FiveGDUBufferPoolMetrics object

    :return: an example FiveGDUBufferPoolMetrics object
    """
    return FiveGDUBufferPoolMetrics()


@pytest.fixture
def example_five_g_du_rlc_metrics() -> FiveGDURLCMetrics:
    """
    Fixture that returns an example FiveGDURLCMetrics object

    :return: an example FiveGDURLCMetrics object
    """
    return FiveGDURLCMetrics()


@pytest.fixture
def example_five_g_du_low_metrics() -> FiveGDULowMetrics:
    """
    Fixture that returns an example FiveGDULowMetrics object

    :return: an example FiveGDULowMetrics object
    """
    return FiveGDULowMetrics()
