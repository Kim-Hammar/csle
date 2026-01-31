from csle_collector.five_g_cu_manager.dao.five_g_cu_cp_metrics import FiveGCUCPMetrics
from csle_collector.five_g_cu_manager.dao.five_g_cu_app_resource_usage_metrics import FiveGCUAppResourceUsageMetrics
from csle_collector.five_g_cu_manager.dao.five_g_cu_buffer_pool_metrics import FiveGCUBufferPoolMetrics


class TestFiveGCuManagerDaoSuite:
    """
    Test suite for FiveGCuManager DAOs
    """

    def test_five_g_cu_cp_metrics(self, example_five_g_cu_cp_metrics: FiveGCUCPMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGCUCPMetrics DAO

        :param example_five_g_cu_cp_metrics: an example FiveGCUCPMetrics
        :return: None
        """
        assert isinstance(example_five_g_cu_cp_metrics.to_dict(), dict)
        assert isinstance(FiveGCUCPMetrics.from_dict(example_five_g_cu_cp_metrics.to_dict()), FiveGCUCPMetrics)
        assert FiveGCUCPMetrics.from_dict(example_five_g_cu_cp_metrics.to_dict()).to_dict() == \
               example_five_g_cu_cp_metrics.to_dict()

    def test_five_g_cu_app_resource_usage_metrics(
            self, example_five_g_cu_app_resource_usage_metrics: FiveGCUAppResourceUsageMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGCUAppResourceUsageMetrics DAO

        :param example_five_g_cu_app_resource_usage_metrics: an example FiveGCUAppResourceUsageMetrics
        :return: None
        """
        assert isinstance(example_five_g_cu_app_resource_usage_metrics.to_dict(), dict)
        assert isinstance(FiveGCUAppResourceUsageMetrics.from_dict(
            example_five_g_cu_app_resource_usage_metrics.to_dict()), FiveGCUAppResourceUsageMetrics)
        assert FiveGCUAppResourceUsageMetrics.from_dict(
            example_five_g_cu_app_resource_usage_metrics.to_dict()).to_dict() == \
            example_five_g_cu_app_resource_usage_metrics.to_dict()

    def test_five_g_cu_buffer_pool_metrics(
            self, example_five_g_cu_buffer_pool_metrics: FiveGCUBufferPoolMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGCUBufferPoolMetrics DAO

        :param example_five_g_cu_buffer_pool_metrics: an example FiveGCUBufferPoolMetrics
        :return: None
        """
        assert isinstance(example_five_g_cu_buffer_pool_metrics.to_dict(), dict)
        assert isinstance(FiveGCUBufferPoolMetrics.from_dict(
            example_five_g_cu_buffer_pool_metrics.to_dict()), FiveGCUBufferPoolMetrics)
        assert FiveGCUBufferPoolMetrics.from_dict(
            example_five_g_cu_buffer_pool_metrics.to_dict()).to_dict() == \
            example_five_g_cu_buffer_pool_metrics.to_dict()
