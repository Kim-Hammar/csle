from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
import csle_system_identification.constants.constants as system_identification_constants
from csle_common.dao.training.hparam import HParam
from csle_system_identification.empirical.empirical_algorithm import EmpiricalAlgorithm
import unittest.mock as mock


class TestEmpiricalAlgorithmSuite:
    """
    Test suite for empirical_algorithm.py
    """

    def test_init(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests initialization of the EmpiricalAlgorithm

        :return: None
        """
        sys_id_config = SystemIdentificationConfig(
            output_dir="test_dir", title="test init", model_type=SystemModelType.EMPIRICAL_DISTRIBUTION,
            log_every=1, hparams={
                system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS: HParam(
                    value=["no_intrusion", "intrusion"],
                    name=system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS,
                    descr="the conditional distributions to estimate"),
                system_identification_constants.SYSTEM_IDENTIFICATION.METRICS: HParam(
                    value=["alerts_weighted_by_priority"],
                    name=system_identification_constants.SYSTEM_IDENTIFICATION.METRICS,
                    descr="the metrics to estimate")
            }
        )
        stats = EmulationStatistics(emulation_name="test_em", descr="test")
        emp_alg = EmpiricalAlgorithm(emulation_env_config=get_ex_em_env, emulation_statistics=stats,
                                     system_identification_config=sys_id_config, system_identification_job=None)
        assert emp_alg.system_identification_job is None
        assert emp_alg.emulation_env_config is not None
        assert emp_alg.emulation_statistics is not None
        assert emp_alg.system_identification_config is not None

        # Clean up
        import shutil
        import os
        if os.path.exists(emp_alg.system_identification_config.output_dir):
            shutil.rmtree(emp_alg.system_identification_config.output_dir)

    @mock.patch("csle_common.metastore.metastore_facade.MetastoreFacade.save_system_identification_job")
    @mock.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_system_identification_job")
    def test_fit(self, mock_update, mock_save, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the fit method of the EmpiricalAlgorithm
        """
        sys_id_config = SystemIdentificationConfig(
            output_dir="test_dir_fit", title="test fit", model_type=SystemModelType.EMPIRICAL_DISTRIBUTION,
            log_every=1, hparams={
                system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS: HParam(
                    value=["no_intrusion"],
                    name=system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS,
                    descr="test"),
                system_identification_constants.SYSTEM_IDENTIFICATION.METRICS: HParam(
                    value=["alerts"],
                    name=system_identification_constants.SYSTEM_IDENTIFICATION.METRICS,
                    descr="test")
            }
        )
        stats = mock.MagicMock(spec=EmulationStatistics)
        stats.id = 1
        stats.conditionals_counts = {"no_intrusion": {"alerts": {1: 10, 2: 20}}}
        stats.conditionals_probs = {"no_intrusion": {"alerts": {1: 0.33, 2: 0.67}}}

        mock_save.return_value = 1

        emp_alg = EmpiricalAlgorithm(emulation_env_config=get_ex_em_env, emulation_statistics=stats,
                                     system_identification_config=sys_id_config, system_identification_job=None)
        model = emp_alg.fit()

        assert model is not None
        assert model.emulation_env_name == get_ex_em_env.name
        assert mock_save.called
        assert mock_update.called

        # Clean up
        import shutil
        import os
        if os.path.exists(emp_alg.system_identification_config.output_dir):
            shutil.rmtree(emp_alg.system_identification_config.output_dir)
