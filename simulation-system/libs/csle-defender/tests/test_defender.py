import pytest
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_defender.defender import Defender
from csle_defender.emulation.emulated_defender import EmulatedDefender


class TestDefenderSuite:
    """
    Test suite for defender.py and emulated_defender.py
    """

    def test_defender_transition(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the defender_transition function
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        action = EmulationDefenderAction(id=EmulationDefenderActionId.CONTINUE, name="CONTINUE",
                                         type=EmulationDefenderActionType.CONTINUE,
                                         cmds=[], descr="", ips=[], index=0)
        s_prime = Defender.defender_transition(s=s, defender_action=action)
        assert s_prime == s

    def test_emulated_defender_transition_stop(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests emulated_defender transition with STOP action
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        action = EmulationDefenderAction(id=EmulationDefenderActionId.STOP, name="STOP",
                                         type=EmulationDefenderActionType.STOP,
                                         cmds=[], descr="", ips=[], index=0)
        s_prime = EmulatedDefender.defender_transition(s=s, defender_action=action, attacker_action=None)
        if s_prime.defender_obs_state is not None:
            assert s_prime.defender_obs_state.stopped is True

    def test_emulated_defender_transition_invalid_type(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests emulated_defender transition with invalid action type
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        # Using CONTINUE id with an action type that is NOT STOP or CONTINUE
        action = EmulationDefenderAction(id=EmulationDefenderActionId.CONTINUE, name="INVALID",
                                         type=EmulationDefenderActionType.ADD_DEFENSIVE_MECHANISM,
                                         cmds=[], descr="", ips=[], index=0)
        with pytest.raises(ValueError, match="Action type not recognized"):
            EmulatedDefender.defender_transition(s=s, defender_action=action, attacker_action=None)

    def test_emulated_defender_transition_invalid_id(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests emulated_defender transition with invalid action id for a recognized type
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        # Using a valid type but an id that is not STOP or CONTINUE
        # EmulationDefenderActionId doesn't have an obviously invalid one that is common,
        # but we can pass an integer that doesn't match the expected ones if it's not strictly typed in runtime
        action = EmulationDefenderAction(id=100, name="INVALID", type=EmulationDefenderActionType.STOP,
                                         cmds=[], descr="", ips=[], index=0)
        with pytest.raises(ValueError, match="Stopping action id:100,name:INVALID not recognized"):
            EmulatedDefender.defender_transition(s=s, defender_action=action, attacker_action=None)
