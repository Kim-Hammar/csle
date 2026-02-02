"""
Unit tests for LocalIntrusionResponseGameConfig DAO.
"""
import json
import tempfile
from typing import Any, Dict

import numpy as np

from gym_csle_intrusion_response_game.dao.local_intrusion_response_game_config import LocalIntrusionResponseGameConfig
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil


class TestLocalIntrusionResponseGameConfigSuite:
    """
    Test suite for LocalIntrusionResponseGameConfig class.
    """

    @staticmethod
    def get_example_config() -> LocalIntrusionResponseGameConfig:
        """
        Creates an example LocalIntrusionResponseGameConfig for testing.

        :return: the example config
        """
        num_zones = 2
        S = IntrusionResponseGameUtil.local_state_space(number_of_zones=num_zones)
        S_A = IntrusionResponseGameUtil.local_attacker_state_space()
        S_D = IntrusionResponseGameUtil.local_defender_state_space(number_of_zones=num_zones)
        A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=num_zones)
        A2 = IntrusionResponseGameUtil.local_attacker_actions()
        O = IntrusionResponseGameUtil.local_observation_space(X_max=10)
        zones = IntrusionResponseGameUtil.zones(num_zones=num_zones)
        d_b1 = IntrusionResponseGameUtil.local_initial_defender_belief(S_A)
        a_b1 = IntrusionResponseGameUtil.local_initial_attacker_belief(S_D, initial_zone=1)
        C_D = IntrusionResponseGameUtil.constant_defender_action_costs(A1, constant_cost=0.1)
        Z_D_P = IntrusionResponseGameUtil.constant_zone_detection_probabilities(zones, constant_detection_prob=0.1)
        A_P = IntrusionResponseGameUtil.local_attack_success_probabilities_uniform(p=0.5, A2=A2)
        Z_U = IntrusionResponseGameUtil.constant_zone_utilities(zones, constant_utility=1.0)

        T = IntrusionResponseGameUtil.local_transition_tensor(Z_D=Z_D_P, A_P=A_P, S=S, A1=A1, A2=A2)
        Z = IntrusionResponseGameUtil.local_observation_tensor_betabinom(S=S, A1=A1, A2=A2, O=O)
        R = IntrusionResponseGameUtil.local_reward_tensor(
            eta=0.5, C_D=C_D, reachable=True, Z_U=Z_U, initial_zone=1, beta=1.0, S=S, A1=A1, A2=A2
        )

        return LocalIntrusionResponseGameConfig(
            env_name="test-env",
            T=np.array([T]),  # Wrap in extra dimension as expected by the class
            O=O,
            Z=Z,
            R=np.array([R]),
            S=S,
            S_A=S_A,
            S_D=S_D,
            s_1_idx=1,
            zones=zones,
            A1=A1,
            A2=A2,
            d_b1=d_b1,
            a_b1=a_b1,
            gamma=0.99,
            beta=1.0,
            C_D=C_D,
            eta=0.5,
            A_P=A_P,
            Z_D_P=Z_D_P,
            Z_U=Z_U
        )

    def test_initialization(self) -> None:
        """
        Tests initialization of LocalIntrusionResponseGameConfig.

        :return: None
        """
        config = self.get_example_config()

        assert config.env_name == "test-env"
        assert config.gamma == 0.99
        assert config.beta == 1.0
        assert config.eta == 0.5
        assert config.s_1_idx == 1
        assert len(config.A1) == 3  # wait + 2 zones
        assert len(config.A2) == 4
        assert len(config.S) == 7  # 1 terminal + 2 zones * 3 attack states
        assert len(config.S_A) == 3
        assert len(config.S_D) == 2
        assert len(config.zones) == 2
        assert len(config.O) == 10

    def test_states_to_idx_mapping(self) -> None:
        """
        Tests that states_to_idx mapping is correctly created.

        :return: None
        """
        config = self.get_example_config()

        # Terminal state should be in the mapping
        assert (-1, -1) in config.states_to_idx
        # Zone 1, healthy should be in the mapping
        assert (1, 0) in config.states_to_idx
        # Zone 2, compromised should be in the mapping
        assert (2, 2) in config.states_to_idx

    def test_attacker_observation_space(self) -> None:
        """
        Tests the attacker_observation_space method.

        :return: None
        """
        config = self.get_example_config()
        obs_space = config.attacker_observation_space()

        # Shape should be len(S_D) + 1
        assert obs_space.shape == (len(config.S_D) + 1,)

    def test_defender_observation_space(self) -> None:
        """
        Tests the defender_observation_space method.

        :return: None
        """
        config = self.get_example_config()
        obs_space = config.defender_observation_space()

        # Shape should be len(S_A) + 1
        assert obs_space.shape == (len(config.S_A) + 1,)

    def test_defender_observation_space_stopping(self) -> None:
        """
        Tests the defender_observation_space_stopping method.

        :return: None
        """
        config = self.get_example_config()
        obs_space = config.defender_observation_space_stopping()

        # Shape should be len(S_A)
        assert obs_space.shape == (len(config.S_A),)

    def test_attacker_action_space(self) -> None:
        """
        Tests the attacker_action_space method.

        :return: None
        """
        config = self.get_example_config()
        action_space = config.attacker_action_space()

        assert action_space.n == len(config.A2)

    def test_defender_action_space(self) -> None:
        """
        Tests the defender_action_space method.

        :return: None
        """
        config = self.get_example_config()
        action_space = config.defender_action_space()

        assert action_space.n == len(config.A1)

    def test_defender_action_space_stopping(self) -> None:
        """
        Tests the defender_action_space_stopping method.

        :return: None
        """
        config = self.get_example_config()
        action_space = config.defender_action_space_stopping()

        assert action_space.n == 2

    def test_to_dict(self) -> None:
        """
        Tests the to_dict method.

        :return: None
        """
        config = self.get_example_config()
        d = config.to_dict()

        assert isinstance(d, dict)
        assert d["env_name"] == "test-env"
        assert d["gamma"] == 0.99
        assert d["beta"] == 1.0
        assert d["eta"] == 0.5
        assert d["s_1_idx"] == 1
        assert "T" in d
        assert "O" in d
        assert "Z" in d
        assert "R" in d
        assert "S" in d
        assert "S_A" in d
        assert "S_D" in d
        assert "A1" in d
        assert "A2" in d
        assert "d_b1" in d
        assert "a_b1" in d
        assert "C_D" in d
        assert "A_P" in d
        assert "Z_D_P" in d
        assert "Z_U" in d
        assert "zones" in d

    def test_from_dict(self) -> None:
        """
        Tests the from_dict method.

        :return: None
        """
        config = self.get_example_config()
        d = config.to_dict()
        restored = LocalIntrusionResponseGameConfig.from_dict(d)

        assert restored.env_name == config.env_name
        assert restored.gamma == config.gamma
        assert restored.beta == config.beta
        assert restored.eta == config.eta
        assert restored.s_1_idx == config.s_1_idx
        assert len(restored.A1) == len(config.A1)
        assert len(restored.A2) == len(config.A2)
        assert len(restored.S) == len(config.S)
        assert np.allclose(restored.d_b1, config.d_b1)
        assert np.allclose(restored.a_b1, config.a_b1)

    def test_roundtrip_dict(self) -> None:
        """
        Tests roundtrip conversion through dict.

        :return: None
        """
        config = self.get_example_config()
        d = config.to_dict()
        restored = LocalIntrusionResponseGameConfig.from_dict(d)
        d2 = restored.to_dict()

        # Check all keys match
        assert set(d.keys()) == set(d2.keys())

        # Check scalar values match
        assert d["env_name"] == d2["env_name"]
        assert d["gamma"] == d2["gamma"]
        assert d["beta"] == d2["beta"]
        assert d["eta"] == d2["eta"]
        assert d["s_1_idx"] == d2["s_1_idx"]

    def test_from_json_file(self) -> None:
        """
        Tests the from_json_file method.

        :return: None
        """
        config = self.get_example_config()
        d = config.to_dict()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(d, f)
            json_path = f.name

        restored = LocalIntrusionResponseGameConfig.from_json_file(json_path)

        assert restored.env_name == config.env_name
        assert restored.gamma == config.gamma
        assert len(restored.S) == len(config.S)

    def test_json_serializable_arrays(self) -> None:
        """
        Tests that all numpy arrays are properly serialized to JSON.

        :return: None
        """
        config = self.get_example_config()
        d = config.to_dict()

        # Should be able to JSON serialize without errors
        json_str = json.dumps(d)
        assert len(json_str) > 0

        # Should be able to deserialize back
        d2: Dict[str, Any] = json.loads(json_str)
        assert d2["env_name"] == "test-env"
