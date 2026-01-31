from csle_ryu.dao.agg_flow_statistic import AggFlowStatistic
from csle_ryu.dao.avg_flow_statistic import AvgFlowStatistic
from csle_ryu.dao.avg_port_statistic import AvgPortStatistic
from csle_ryu.dao.flow_statistic import FlowStatistic
from csle_ryu.dao.port_statistic import PortStatistic


class TestRyuDaoSuite:
    """
    Test suite for Ryu data access objects (DAOs)
    """

    def test_agg_flow_statistic(self, example_agg_flow_statistic: AggFlowStatistic) -> None:
        """
        Tests creation and dict conversion of the AggFlowStatistic DAO

        :param example_agg_flow_statistic: an example AggFlowStatistic
        :return: None
        """
        assert isinstance(example_agg_flow_statistic.to_dict(), dict)
        assert isinstance(AggFlowStatistic.from_dict(example_agg_flow_statistic.to_dict()), AggFlowStatistic)
        assert (AggFlowStatistic.from_dict(example_agg_flow_statistic.to_dict()).to_dict() ==
                example_agg_flow_statistic.to_dict())

    def test_avg_flow_statistic(self, example_avg_flow_statistic: AvgFlowStatistic) -> None:
        """
        Tests creation and dict conversion of the AvgFlowStatistic DAO

        :param example_avg_flow_statistic: an example AvgFlowStatistic
        :return: None
        """
        assert isinstance(example_avg_flow_statistic.to_dict(), dict)
        assert isinstance(AvgFlowStatistic.from_dict(example_avg_flow_statistic.to_dict()), AvgFlowStatistic)
        assert (AvgFlowStatistic.from_dict(example_avg_flow_statistic.to_dict()).to_dict() ==
                example_avg_flow_statistic.to_dict())

    def test_avg_port_statistic(self, example_avg_port_statistic: AvgPortStatistic) -> None:
        """
        Tests creation and dict conversion of the AvgPortStatistic DAO

        :param example_avg_port_statistic: an example AvgPortStatistic
        :return: None
        """
        assert isinstance(example_avg_port_statistic.to_dict(), dict)
        assert isinstance(AvgPortStatistic.from_dict(example_avg_port_statistic.to_dict()), AvgPortStatistic)
        assert (AvgPortStatistic.from_dict(example_avg_port_statistic.to_dict()).to_dict() ==
                example_avg_port_statistic.to_dict())

    def test_flow_statistic(self, example_flow_statistic: FlowStatistic) -> None:
        """
        Tests creation and dict conversion of the FlowStatistic DAO

        :param example_flow_statistic: an example FlowStatistic
        :return: None
        """
        assert isinstance(example_flow_statistic.to_dict(), dict)
        assert isinstance(FlowStatistic.from_dict(example_flow_statistic.to_dict()), FlowStatistic)
        assert (FlowStatistic.from_dict(example_flow_statistic.to_dict()).to_dict() ==
                example_flow_statistic.to_dict())

    def test_port_statistic(self, example_port_statistic: PortStatistic) -> None:
        """
        Tests creation and dict conversion of the PortStatistic DAO

        :param example_port_statistic: an example PortStatistic
        :return: None
        """
        assert isinstance(example_port_statistic.to_dict(), dict)
        assert isinstance(PortStatistic.from_dict(example_port_statistic.to_dict()), PortStatistic)
        assert (PortStatistic.from_dict(example_port_statistic.to_dict()).to_dict() ==
                example_port_statistic.to_dict())
