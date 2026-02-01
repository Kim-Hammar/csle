import pytest
import unittest.mock as mock
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_attacker.attacker import Attacker
from csle_attacker.emulation.emulated_attacker import EmulatedAttacker


class TestAttackerSuite:
    """
    Test suite for attacker.py and emulated_attacker.py
    """

    def test_attacker_transition(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the attacker_transition method
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(id=EmulationAttackerActionId.CONTINUE, name="CONTINUE", cmds=[],
                                    type=EmulationAttackerActionType.CONTINUE, descr="", ips=[], index=-1)
        s_prime = Attacker.attacker_transition(s=s, attacker_action=a)
        assert s_prime == s

    @mock.patch("csle_attacker.emulation.recon_middleware.ReconMiddleware.execute_tcp_syn_stealth_scan")
    @mock.patch("csle_common.util.env_dynamics_util.EnvDynamicsUtil.cache_attacker_action")
    def test_emulated_attacker_recon(self, mock_cache, mock_recon, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the emulated_attacker reconnaissance transition
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST, name="SCAN", cmds=[],
                                    type=EmulationAttackerActionType.RECON, descr="", ips=[], index=-1)
        mock_recon.return_value = s
        s_prime = EmulatedAttacker.attacker_transition(s=s, attacker_action=a)
        assert s_prime == s
        assert mock_cache.called
        assert mock_recon.called

    @mock.patch("csle_attacker.emulation.exploit_middleware.ExploitMiddleware.execute_ssh_same_user_dictionary")
    @mock.patch("csle_common.util.env_dynamics_util.EnvDynamicsUtil.cache_attacker_action")
    def test_emulated_attacker_exploit(self, mock_cache, mock_exploit, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the emulated_attacker exploit transition
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(id=EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST,
                                    name="SSH", cmds=[], type=EmulationAttackerActionType.EXPLOIT,
                                    descr="", ips=[], index=-1)
        mock_exploit.return_value = s
        s_prime = EmulatedAttacker.attacker_transition(s=s, attacker_action=a)
        assert s_prime == s
        assert mock_cache.called
        assert mock_exploit.called

    @mock.patch("csle_attacker.emulation.post_exploit_middleware.PostExploitMiddleware.execute_bash_find_flag")
    def test_emulated_attacker_post_exploit(self, mock_post_exploit, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the emulated_attacker post-exploit transition
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(id=EmulationAttackerActionId.FIND_FLAG, name="FLAG", cmds=[],
                                    type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=-1)
        mock_post_exploit.return_value = s
        s_prime = EmulatedAttacker.attacker_transition(s=s, attacker_action=a)
        assert s_prime == s
        assert mock_post_exploit.called

    def test_emulated_attacker_stopping(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the emulated_attacker stopping transition
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(id=EmulationAttackerActionId.CONTINUE, name="CONTINUE", cmds=[],
                                    type=EmulationAttackerActionType.CONTINUE, descr="", ips=[], index=-1)
        s_prime = EmulatedAttacker.attacker_transition(s=s, attacker_action=a)
        assert s_prime == s

    def test_emulated_attacker_invalid_type(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the emulated_attacker with invalid action type
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(id=EmulationAttackerActionId.CONTINUE, name="INVALID", cmds=[],
                                    type=99, descr="", ips=[], index=-1)
        with pytest.raises(ValueError):
            EmulatedAttacker.attacker_transition(s=s, attacker_action=a)

    def test_emulated_attacker_invalid_recon_id(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the emulated_attacker with invalid recon action id
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(id=999, name="INVALID", cmds=[],
                                    type=EmulationAttackerActionType.RECON, descr="", ips=[], index=-1)
        with pytest.raises(ValueError):
            EmulatedAttacker.attacker_transition(s=s, attacker_action=a)

    def test_emulated_attacker_invalid_exploit_id(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the emulated_attacker with invalid exploit action id
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(id=999, name="INVALID", cmds=[],
                                    type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=-1)
        with pytest.raises(ValueError):
            EmulatedAttacker.attacker_transition(s=s, attacker_action=a)

    def test_emulated_attacker_invalid_post_exploit_id(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the emulated_attacker with invalid post-exploit action id
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(id=999, name="INVALID", cmds=[],
                                    type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=-1)
        with pytest.raises(ValueError):
            EmulatedAttacker.attacker_transition(s=s, attacker_action=a)

    def test_emulated_attacker_invalid_stopping_id(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the emulated_attacker with invalid stopping action id
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        a = EmulationAttackerAction(id=999, name="INVALID", cmds=[],
                                    type=EmulationAttackerActionType.CONTINUE, descr="", ips=[], index=-1)
        with pytest.raises(ValueError):
            EmulatedAttacker.attacker_transition(s=s, attacker_action=a)
