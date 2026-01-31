import pytest
from csle_ryu.dao.agg_flow_statistic import AggFlowStatistic
from csle_ryu.dao.avg_flow_statistic import AvgFlowStatistic
from csle_ryu.dao.avg_port_statistic import AvgPortStatistic
from csle_ryu.dao.flow_statistic import FlowStatistic
from csle_ryu.dao.port_statistic import PortStatistic


@pytest.fixture
def example_agg_flow_statistic() -> AggFlowStatistic:
    """
    :return: an example AggFlowStatistic object
    """
    return AggFlowStatistic(timestamp=1234567.8, datapath_id="1", total_num_packets=100, total_num_bytes=1000,
                            total_num_flows=5)


@pytest.fixture
def example_avg_flow_statistic() -> AvgFlowStatistic:
    """
    :return: an example AvgFlowStatistic object
    """
    return AvgFlowStatistic(timestamp=1234567.8, datapath_id="1", total_num_packets=100, total_num_bytes=1000,
                            avg_duration_nanoseconds=100, avg_duration_seconds=1, avg_hard_timeout=0,
                            avg_idle_timeout=0, avg_priority=100, avg_cookie=1)


@pytest.fixture
def example_avg_port_statistic() -> AvgPortStatistic:
    """
    :return: an example AvgPortStatistic object
    """
    return AvgPortStatistic(timestamp=1234567.8, datapath_id="1", total_num_received_packets=100,
                            total_num_received_bytes=1000, total_num_received_errors=0,
                            total_num_transmitted_packets=100, total_num_transmitted_bytes=1000,
                            total_num_transmitted_errors=0, total_num_received_dropped=0,
                            total_num_transmitted_dropped=0, total_num_received_frame_errors=0,
                            total_num_received_overrun_errors=0, total_num_received_crc_errors=0,
                            total_num_collisions=0, avg_duration_nanoseconds=100, avg_duration_seconds=1)


@pytest.fixture
def example_flow_statistic() -> FlowStatistic:
    """
    :return: an example FlowStatistic object
    """
    return FlowStatistic(timestamp=1234567.8, datapath_id="1", in_port="1", out_port="2",
                         dst_mac_address="00:00:00:00:00:01", num_packets=10, num_bytes=100,
                         duration_nanoseconds=100, duration_seconds=1, hard_timeout=0,
                         idle_timeout=0, priority=100, cookie=1)


@pytest.fixture
def example_port_statistic() -> PortStatistic:
    """
    :return: an example PortStatistic object
    """
    return PortStatistic(timestamp=1234567.8, datapath_id="1", port=1, num_received_packets=10,
                         num_received_bytes=100, num_received_errors=0, num_transmitted_packets=10,
                         num_transmitted_bytes=100, num_transmitted_errors=0, num_received_dropped=0,
                         num_transmitted_dropped=0, num_received_frame_errors=0, num_received_overrun_errors=0,
                         num_received_crc_errors=0, num_collisions=0, duration_nanoseconds=100,
                         duration_seconds=1)
