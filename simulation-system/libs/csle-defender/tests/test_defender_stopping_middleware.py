from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_defender.emulation.defender_stopping_middleware import DefenderStoppingMiddleware


class TestDefenderStoppingMiddlewareSuite:
    """
    Test suite for defender_update_state_middleware.py
    """

    def test_stop_monitor(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the stop_monitor function
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        s_prime = DefenderStoppingMiddleware.stop_monitor(s=s)
        if s_prime.defender_obs_state is not None:
            assert s_prime.defender_obs_state.stopped is True

    def test_continue_monitor(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the continue_monitor function
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        s_prime = DefenderStoppingMiddleware.continue_monitor(s=s)
        assert s_prime == s
