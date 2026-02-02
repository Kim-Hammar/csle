"""
Unit tests for IntrusionResponseGameStateLocal DAO.
"""
import json
import tempfile
from typing import Any, Dict

import numpy as np

from gym_csle_intrusion_response_game.dao.intrusion_response_game_state_local import IntrusionResponseGameStateLocal
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
import gym_csle_intrusion_response_game.constants.constants as env_constants


class TestIntrusionResponseGameStateLocalSuite:
    """
    Test suite for IntrusionResponseGameStateLocal class.
    """

    @staticmethod
    def get_example_state() -> IntrusionResponseGameStateLocal:
        """
        Creates an example IntrusionResponseGameStateLocal for testing.

        :return: the example state
        """
        num_zones = 2
        S = IntrusionResponseGameUtil.local_state_space(number_of_zones=num_zones)
        S_A = IntrusionResponseGameUtil.local_attacker_state_space()
        S_D = IntrusionResponseGameUtil.local_defender_state_space(number_of_zones=num_zones)
        d_b1 = IntrusionResponseGameUtil.local_initial_defender_belief(S_A)
        a_b1 = IntrusionResponseGameUtil.local_initial_attacker_belief(S_D, initial_zone=1)
        s_1_idx = IntrusionResponseGameUtil.local_initial_state_idx(initial_zone=1, S=S)

        return IntrusionResponseGameStateLocal(
            d_b1=d_b1,
            a_b1=a_b1,
            s_1_idx=s_1_idx,
            S=S,
            S_A=S_A,
            S_D=S_D
        )

    def test_initialization(self) -> None:
        """
        Tests initialization of IntrusionResponseGameStateLocal.

        :return: None
        """
        state = self.get_example_state()

        assert state.t == 1
        assert state.s_idx == state.s_1_idx
        assert len(state.d_b) == len(state.d_b1)
        assert len(state.a_b) == len(state.a_b1)
        assert np.allclose(state.d_b, state.d_b1)
        assert np.allclose(state.a_b, state.a_b1)

    def test_reset(self) -> None:
        """
        Tests the reset method.

        :return: None
        """
        state = self.get_example_state()

        # Modify state
        state.t = 10
        state.s_idx = 5
        state.d_b = np.array([0.1, 0.2, 0.7])
        state.a_b = np.array([0.5, 0.5])

        # Reset
        state.reset()

        # Should be back to initial values
        assert state.t == 1
        assert state.s_idx == state.s_1_idx
        assert np.allclose(state.d_b, state.d_b1)
        assert np.allclose(state.a_b, state.a_b1)

    def test_attacker_observation(self) -> None:
        """
        Tests the attacker_observation method.

        :return: None
        """
        state = self.get_example_state()
        obs = state.attacker_observation()

        # Should be attacker state + belief
        expected_length = 1 + len(state.a_b)
        assert len(obs) == expected_length
        assert obs[0] == state.attacker_state()

    def test_defender_observation(self) -> None:
        """
        Tests the defender_observation method.

        :return: None
        """
        state = self.get_example_state()
        obs = state.defender_observation()

        # Should be defender state + belief
        expected_length = 1 + len(state.d_b)
        assert len(obs) == expected_length
        assert obs[0] == state.defender_state()

    def test_state_vector(self) -> None:
        """
        Tests the state_vector method.

        :return: None
        """
        state = self.get_example_state()
        vec = state.state_vector()

        assert len(vec) == 2  # [d_state, a_state]
        assert vec[env_constants.STATES.D_STATE_INDEX] == state.defender_state()
        assert vec[env_constants.STATES.A_STATE_INDEX] == state.attacker_state()

    def test_attacker_state(self) -> None:
        """
        Tests the attacker_state method.

        :return: None
        """
        state = self.get_example_state()
        a_state = state.attacker_state()

        # Initial state should be healthy (0)
        assert a_state == env_constants.ATTACK_STATES.HEALTHY

    def test_defender_state(self) -> None:
        """
        Tests the defender_state method.

        :return: None
        """
        state = self.get_example_state()
        d_state = state.defender_state()

        # Initial zone is 1
        assert d_state == 1

    def test_str(self) -> None:
        """
        Tests the __str__ method.

        :return: None
        """
        state = self.get_example_state()
        s = str(state)

        assert "d_b1" in s
        assert "a_b1" in s
        assert "s_1_idx" in s
        assert "s_idx" in s
        assert "t:" in s

    def test_to_dict(self) -> None:
        """
        Tests the to_dict method.

        :return: None
        """
        state = self.get_example_state()
        d = state.to_dict()

        assert isinstance(d, dict)
        assert "d_b1" in d
        assert "a_b1" in d
        assert "s_1_idx" in d
        assert "s_idx" in d
        assert "S" in d
        assert "S_A" in d
        assert "S_D" in d
        assert "d_b" in d
        assert "a_b" in d
        assert "t" in d

    def test_from_dict(self) -> None:
        """
        Tests the from_dict method.

        :return: None
        """
        state = self.get_example_state()
        d = state.to_dict()
        restored = IntrusionResponseGameStateLocal.from_dict(d)

        assert restored.s_1_idx == state.s_1_idx
        assert len(restored.S) == len(state.S)
        assert len(restored.S_A) == len(state.S_A)
        assert len(restored.S_D) == len(state.S_D)
        assert np.allclose(restored.d_b1, state.d_b1)
        assert np.allclose(restored.a_b1, state.a_b1)

    def test_roundtrip_dict(self) -> None:
        """
        Tests roundtrip conversion through dict.

        :return: None
        """
        state = self.get_example_state()

        # Modify state
        state.t = 5
        state.s_idx = 3
        state.d_b = np.array([0.2, 0.3, 0.5])

        d = state.to_dict()
        restored = IntrusionResponseGameStateLocal.from_dict(d)

        assert restored.s_1_idx == state.s_1_idx

    def test_from_json_file(self) -> None:
        """
        Tests the from_json_file method.

        :return: None
        """
        state = self.get_example_state()
        d = state.to_dict()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(d, f)
            json_path = f.name

        restored = IntrusionResponseGameStateLocal.from_json_file(json_path)

        assert restored.s_1_idx == state.s_1_idx
        assert len(restored.S) == len(state.S)

    def test_json_serializable(self) -> None:
        """
        Tests that the state is properly serializable to JSON.

        :return: None
        """
        state = self.get_example_state()
        d = state.to_dict()

        # Should be able to JSON serialize without errors
        json_str = json.dumps(d)
        assert len(json_str) > 0

        # Should be able to deserialize back
        d2: Dict[str, Any] = json.loads(json_str)
        assert d2["s_1_idx"] == state.s_1_idx

    def test_belief_updates(self) -> None:
        """
        Tests that beliefs can be updated independently of initial beliefs.

        :return: None
        """
        state = self.get_example_state()

        # Store original beliefs
        original_d_b1 = state.d_b1.copy()
        original_a_b1 = state.a_b1.copy()

        # Update current beliefs
        state.d_b = np.array([0.1, 0.2, 0.7])
        state.a_b = np.array([0.6, 0.4])

        # Initial beliefs should not change
        assert np.allclose(state.d_b1, original_d_b1)
        assert np.allclose(state.a_b1, original_a_b1)

        # Current beliefs should be updated
        assert not np.allclose(state.d_b, state.d_b1)
        assert not np.allclose(state.a_b, state.a_b1)

    def test_time_step_increment(self) -> None:
        """
        Tests time step tracking.

        :return: None
        """
        state = self.get_example_state()

        assert state.t == 1
        state.t += 1
        assert state.t == 2
        state.t = 100
        assert state.t == 100

        state.reset()
        assert state.t == 1
