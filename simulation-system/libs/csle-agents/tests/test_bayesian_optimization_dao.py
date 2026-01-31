from csle_agents.agents.bayesian_optimization_emukit.bo.kernel.rbf_kernel_config import RBFKernelConfig
from csle_agents.agents.bayesian_optimization_emukit.bo.gp.gp_config import GPConfig
from csle_agents.agents.bayesian_optimization_emukit.bo.bo_config import BOConfig
from csle_agents.agents.bayesian_optimization_emukit.bo.bo_results import BOResults


class TestBayesianOptimizationDaoSuite:
    """
    Test suite for Bayesian Optimization data access objects (DAOs)
    """

    def test_rbf_kernel_config(self, example_rbf_kernel_config: RBFKernelConfig) -> None:
        """
        Tests creation and dict conversion of the RBFKernelConfig DAO

        :param example_rbf_kernel_config: an example RBFKernelConfig
        :return: None
        """
        assert isinstance(example_rbf_kernel_config.to_dict(), dict)
        assert isinstance(RBFKernelConfig.from_dict(example_rbf_kernel_config.to_dict()), RBFKernelConfig)
        assert RBFKernelConfig.from_dict(example_rbf_kernel_config.to_dict()).to_dict() == \
               example_rbf_kernel_config.to_dict()
        assert RBFKernelConfig.from_dict(example_rbf_kernel_config.to_dict()) == example_rbf_kernel_config

    def test_gp_config(self, example_gp_config: GPConfig) -> None:
        """
        Tests creation and dict conversion of the GPConfig DAO

        :param example_gp_config: an example GPConfig
        :return: None
        """
        assert isinstance(example_gp_config.to_dict(), dict)
        assert isinstance(GPConfig.from_dict(example_gp_config.to_dict()), GPConfig)
        assert GPConfig.from_dict(example_gp_config.to_dict()).to_dict() == example_gp_config.to_dict()

    def test_bo_config(self, example_bo_config: BOConfig) -> None:
        """
        Tests creation and dict conversion of the BOConfig DAO

        :param example_bo_config: an example BOConfig
        :return: None
        """
        assert isinstance(example_bo_config.to_dict(), dict)
        assert isinstance(BOConfig.from_dict(example_bo_config.to_dict()), BOConfig)
        assert BOConfig.from_dict(example_bo_config.to_dict()).to_dict() == example_bo_config.to_dict()

    def test_bo_results(self, example_bo_results: BOResults) -> None:
        """
        Tests creation and dict conversion of the BOResults DAO

        :param example_bo_results: an example BOResults
        :return: None
        """
        assert isinstance(example_bo_results.to_dict(), dict)
        assert isinstance(BOResults.from_dict(example_bo_results.to_dict()), BOResults)
        assert BOResults.from_dict(example_bo_results.to_dict()).to_dict() == example_bo_results.to_dict()
