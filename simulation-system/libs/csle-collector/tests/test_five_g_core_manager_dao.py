from csle_collector.five_g_core_manager.dao.five_g_core_amf_metrics import FiveGCoreAMFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_hss_metrics import FiveGCoreHSSMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_mme_metrics import FiveGCoreMMEMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_pcf_metrics import FiveGCorePCFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_pcrf_metrics import FiveGCorePCRFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_smf_metrics import FiveGCoreSMFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_upf_metrics import FiveGCoreUPFMetrics


class TestFiveGCoreManagerDaoSuite:
    """
    Test suite for FiveGCoreManager DAOs
    """

    def test_five_g_core_amf_metrics(self, example_five_g_core_amf_metrics: FiveGCoreAMFMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGCoreAMFMetrics DAO

        :param example_five_g_core_amf_metrics: an example FiveGCoreAMFMetrics
        :return: None
        """
        assert isinstance(example_five_g_core_amf_metrics.to_dict(), dict)
        assert isinstance(FiveGCoreAMFMetrics.from_dict(example_five_g_core_amf_metrics.to_dict()), FiveGCoreAMFMetrics)
        assert FiveGCoreAMFMetrics.from_dict(example_five_g_core_amf_metrics.to_dict()).to_dict() == \
               example_five_g_core_amf_metrics.to_dict()

    def test_five_g_core_hss_metrics(self, example_five_g_core_hss_metrics: FiveGCoreHSSMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGCoreHSSMetrics DAO

        :param example_five_g_core_hss_metrics: an example FiveGCoreHSSMetrics
        :return: None
        """
        assert isinstance(example_five_g_core_hss_metrics.to_dict(), dict)
        assert isinstance(FiveGCoreHSSMetrics.from_dict(example_five_g_core_hss_metrics.to_dict()), FiveGCoreHSSMetrics)
        assert FiveGCoreHSSMetrics.from_dict(example_five_g_core_hss_metrics.to_dict()).to_dict() == \
               example_five_g_core_hss_metrics.to_dict()

    def test_five_g_core_mme_metrics(self, example_five_g_core_mme_metrics: FiveGCoreMMEMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGCoreMMEMetrics DAO

        :param example_five_g_core_mme_metrics: an example FiveGCoreMMEMetrics
        :return: None
        """
        assert isinstance(example_five_g_core_mme_metrics.to_dict(), dict)
        assert isinstance(FiveGCoreMMEMetrics.from_dict(example_five_g_core_mme_metrics.to_dict()), FiveGCoreMMEMetrics)
        assert FiveGCoreMMEMetrics.from_dict(example_five_g_core_mme_metrics.to_dict()).to_dict() == \
               example_five_g_core_mme_metrics.to_dict()

    def test_five_g_core_pcf_metrics(self, example_five_g_core_pcf_metrics: FiveGCorePCFMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGCorePCFMetrics DAO

        :param example_five_g_core_pcf_metrics: an example FiveGCorePCFMetrics
        :return: None
        """
        assert isinstance(example_five_g_core_pcf_metrics.to_dict(), dict)
        assert isinstance(FiveGCorePCFMetrics.from_dict(example_five_g_core_pcf_metrics.to_dict()), FiveGCorePCFMetrics)
        assert FiveGCorePCFMetrics.from_dict(example_five_g_core_pcf_metrics.to_dict()).to_dict() == \
               example_five_g_core_pcf_metrics.to_dict()

    def test_five_g_core_pcrf_metrics(self, example_five_g_core_pcrf_metrics: FiveGCorePCRFMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGCorePCRFMetrics DAO

        :param example_five_g_core_pcrf_metrics: an example FiveGCorePCRFMetrics
        :return: None
        """
        assert isinstance(example_five_g_core_pcrf_metrics.to_dict(), dict)
        assert isinstance(FiveGCorePCRFMetrics.from_dict(
            example_five_g_core_pcrf_metrics.to_dict()), FiveGCorePCRFMetrics)
        assert FiveGCorePCRFMetrics.from_dict(example_five_g_core_pcrf_metrics.to_dict()).to_dict() == \
               example_five_g_core_pcrf_metrics.to_dict()

    def test_five_g_core_smf_metrics(self, example_five_g_core_smf_metrics: FiveGCoreSMFMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGCoreSMFMetrics DAO

        :param example_five_g_core_smf_metrics: an example FiveGCoreSMFMetrics
        :return: None
        """
        assert isinstance(example_five_g_core_smf_metrics.to_dict(), dict)
        assert isinstance(FiveGCoreSMFMetrics.from_dict(example_five_g_core_smf_metrics.to_dict()), FiveGCoreSMFMetrics)
        assert FiveGCoreSMFMetrics.from_dict(example_five_g_core_smf_metrics.to_dict()).to_dict() == \
               example_five_g_core_smf_metrics.to_dict()

    def test_five_g_core_upf_metrics(self, example_five_g_core_upf_metrics: FiveGCoreUPFMetrics) -> None:
        """
        Tests creation and dict conversion of the FiveGCoreUPFMetrics DAO

        :param example_five_g_core_upf_metrics: an example FiveGCoreUPFMetrics
        :return: None
        """
        assert isinstance(example_five_g_core_upf_metrics.to_dict(), dict)
        assert isinstance(FiveGCoreUPFMetrics.from_dict(example_five_g_core_upf_metrics.to_dict()), FiveGCoreUPFMetrics)
        assert FiveGCoreUPFMetrics.from_dict(example_five_g_core_upf_metrics.to_dict()).to_dict() == \
               example_five_g_core_upf_metrics.to_dict()
