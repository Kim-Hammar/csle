import pytest
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_attacker.emulation.attacker_stopping_middleware import AttackerStoppingMiddleware


class TestAttackerStoppingMiddlewareSuite:
    """
    Test suite for attacker_stopping_middleware.py
    """

    def test_stop_intrusion(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the stop_intrusion function
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(
            id=EmulationAttackerActionId.STOP, name="STOP", cmds=[], type=0, descr="", ips=[], index=-1)
        with pytest.raises(NotImplementedError):
            AttackerStoppingMiddleware.stop_intrusion(s=s, a=a)

    def test_continue_intrusion(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the continue_intrusion function
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(
            id=EmulationAttackerActionId.CONTINUE, name="CONTINUE", cmds=[], type=0, descr="", ips=[], index=-1)
        s_prime = AttackerStoppingMiddleware.continue_intrusion(s=s, a=a)
        assert s_prime == s
