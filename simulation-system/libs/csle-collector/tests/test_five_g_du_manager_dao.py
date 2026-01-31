from csle_collector.five_g_du_manager.dao.five_g_du_metrics import FiveGDUMetrics
from csle_collector.five_g_du_manager.dao.five_g_du_cell_metrics import FiveGDUCellMetrics
from csle_collector.five_g_du_manager.dao.five_g_du_app_resource_usage_metrics import FiveGDUAppResourceUsageMetrics
from csle_collector.five_g_du_manager.dao.five_g_du_buffer_pool_metrics import FiveGDUBufferPoolMetrics
from csle_collector.five_g_du_manager.dao.five_g_du_rlc_metrics import FiveGDURLCMetrics
from csle_collector.five_g_du_manager.dao.five_g_du_low_metrics import FiveGDULowMetrics


class TestFiveGDuManagerDaoSuite:
    """
    Test suite for FiveGDuManager DAOs
    """

    def test_five_g_du_metrics(self, example_five_g_du_metrics: FiveGDUMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGDUMetrics DAO

        :param example_five_g_du_metrics: an example FiveGDUMetrics
        :return: None
        """
        assert isinstance(example_five_g_du_metrics.to_dict(), dict)
        assert isinstance(FiveGDUMetrics.from_dict(example_five_g_du_metrics.to_dict()), FiveGDUMetrics)
        assert FiveGDUMetrics.from_dict(example_five_g_du_metrics.to_dict()).to_dict() == \
               example_five_g_du_metrics.to_dict()

    def test_five_g_du_cell_metrics(self, example_five_g_du_cell_metrics: FiveGDUCellMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGDUCellMetrics DAO

        :param example_five_g_du_cell_metrics: an example FiveGDUCellMetrics
        :return: None
        """
        assert isinstance(example_five_g_du_cell_metrics.to_dict(), dict)
        assert isinstance(FiveGDUCellMetrics.from_dict(example_five_g_du_cell_metrics.to_dict()), FiveGDUCellMetrics)
        assert FiveGDUCellMetrics.from_dict(example_five_g_du_cell_metrics.to_dict()).to_dict() == \
               example_five_g_du_cell_metrics.to_dict()

    def test_five_g_du_app_resource_usage_metrics(
            self, example_five_g_du_app_resource_usage_metrics: FiveGDUAppResourceUsageMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGDUAppResourceUsageMetrics DAO

        :param example_five_g_du_app_resource_usage_metrics: an example FiveGDUAppResourceUsageMetrics
        :return: None
        """
        assert isinstance(example_five_g_du_app_resource_usage_metrics.to_dict(), dict)
        assert isinstance(FiveGDUAppResourceUsageMetrics.from_dict(
            example_five_g_du_app_resource_usage_metrics.to_dict()), FiveGDUAppResourceUsageMetrics)
        assert FiveGDUAppResourceUsageMetrics.from_dict(
            example_five_g_du_app_resource_usage_metrics.to_dict()).to_dict() == \
            example_five_g_du_app_resource_usage_metrics.to_dict()

    def test_five_g_du_buffer_pool_metrics(
            self, example_five_g_du_buffer_pool_metrics: FiveGDUBufferPoolMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGDUBufferPoolMetrics DAO

        :param example_five_g_du_buffer_pool_metrics: an example FiveGDUBufferPoolMetrics
        :return: None
        """
        assert isinstance(example_five_g_du_buffer_pool_metrics.to_dict(), dict)
        assert isinstance(FiveGDUBufferPoolMetrics.from_dict(
            example_five_g_du_buffer_pool_metrics.to_dict()), FiveGDUBufferPoolMetrics)
        assert FiveGDUBufferPoolMetrics.from_dict(
            example_five_g_du_buffer_pool_metrics.to_dict()).to_dict() == \
            example_five_g_du_buffer_pool_metrics.to_dict()

    def test_five_g_du_rlc_metrics(self, example_five_g_du_rlc_metrics: FiveGDURLCMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGDURLCMetrics DAO

        :param example_five_g_du_rlc_metrics: an example FiveGDURLCMetrics
        :return: None
        """
        assert isinstance(example_five_g_du_rlc_metrics.to_dict(), dict)
        assert isinstance(FiveGDURLCMetrics.from_dict(example_five_g_du_rlc_metrics.to_dict()), FiveGDURLCMetrics)
        assert FiveGDURLCMetrics.from_dict(example_five_g_du_rlc_metrics.to_dict()).to_dict() == \
               example_five_g_du_rlc_metrics.to_dict()

    def test_five_g_du_low_metrics(self, example_five_g_du_low_metrics: FiveGDULowMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGDULowMetrics DAO

        :param example_five_g_du_low_metrics: an example FiveGDULowMetrics
        :return: None
        """
        assert isinstance(example_five_g_du_low_metrics.to_dict(), dict)
        assert isinstance(FiveGDULowMetrics.from_dict(example_five_g_du_low_metrics.to_dict()), FiveGDULowMetrics)
        assert FiveGDULowMetrics.from_dict(example_five_g_du_low_metrics.to_dict()).to_dict() == \
               example_five_g_du_low_metrics.to_dict()
