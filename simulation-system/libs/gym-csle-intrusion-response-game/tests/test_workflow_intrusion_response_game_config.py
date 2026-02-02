"""
Unit tests for WorkflowIntrusionResponseGameConfig DAO.
"""
import json
import tempfile
from typing import Any, Dict

import numpy as np

from gym_csle_intrusion_response_game.dao.workflow_intrusion_response_game_config import (
    WorkflowIntrusionResponseGameConfig
)
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil


class TestWorkflowIntrusionResponseGameConfigSuite:
    """
    Test suite for WorkflowIntrusionResponseGameConfig class.
    """

    @staticmethod
    def get_example_config() -> WorkflowIntrusionResponseGameConfig:
        """
        Creates an example WorkflowIntrusionResponseGameConfig for testing.

        :return: the example config
        """
        num_zones = 3
        zones = IntrusionResponseGameUtil.zones(num_zones=num_zones)
        A2 = IntrusionResponseGameUtil.local_attacker_actions()

        # Create adjacency matrix for 2 nodes (simple linear topology)
        adjacency_matrix = np.array([[0, 1], [1, 0]])
        nodes = np.array([0, 1])
        initial_zones = np.array([1, 2])
        gw_reachable = np.array([1, 0])

        C_D = IntrusionResponseGameUtil.constant_defender_action_costs(
            IntrusionResponseGameUtil.local_defender_actions(number_of_zones=num_zones),
            constant_cost=0.1
        )
        Z_D_P = IntrusionResponseGameUtil.constant_zone_detection_probabilities(zones, constant_detection_prob=0.1)
        A_P = IntrusionResponseGameUtil.local_attack_success_probabilities_uniform(p=0.5, A2=A2)
        Z_U = IntrusionResponseGameUtil.constant_zone_utilities(zones, constant_utility=1.0)

        return WorkflowIntrusionResponseGameConfig(
            env_name="test-workflow-env",
            adjacency_matrix=adjacency_matrix,
            nodes=nodes,
            initial_zones=initial_zones,
            X_max=10,
            beta=1.0,
            gamma=0.99,
            zones=zones,
            Z_D_P=Z_D_P,
            C_D=C_D,
            A_P=A_P,
            Z_U=Z_U,
            eta=0.5,
            gw_reachable=gw_reachable
        )

    def test_initialization(self) -> None:
        """
        Tests initialization of WorkflowIntrusionResponseGameConfig.

        :return: None
        """
        config = self.get_example_config()

        assert config.env_name == "test-workflow-env"
        assert config.X_max == 10
        assert config.beta == 1.0
        assert config.gamma == 0.99
        assert config.eta == 0.5
        assert len(config.nodes) == 2
        assert len(config.initial_zones) == 2
        assert len(config.zones) == 3
        assert config.adjacency_matrix.shape == (2, 2)
        assert len(config.gw_reachable) == 2

    def test_attacker_observation_space(self) -> None:
        """
        Tests the attacker_observation_space method.

        :return: None
        """
        config = self.get_example_config()
        obs_space = config.attacker_observation_space()

        # Shape should be (len(zones) + 1) * len(nodes)
        expected_shape = ((len(config.zones) + 1) * len(config.nodes),)
        assert obs_space.shape == expected_shape

    def test_defender_observation_space(self) -> None:
        """
        Tests the defender_observation_space method.

        :return: None
        """
        config = self.get_example_config()
        obs_space = config.defender_observation_space()

        # Shape should be 4 * len(nodes)
        expected_shape = (4 * len(config.nodes),)
        assert obs_space.shape == expected_shape

    def test_attacker_action_space(self) -> None:
        """
        Tests the attacker_action_space method.

        :return: None
        """
        config = self.get_example_config()
        action_space = config.attacker_action_space()

        # MultiDiscrete with 4 actions per node
        assert action_space.shape == (len(config.nodes),)
        assert all(n == 4 for n in action_space.nvec)

    def test_defender_action_space(self) -> None:
        """
        Tests the defender_action_space method.

        :return: None
        """
        config = self.get_example_config()
        action_space = config.defender_action_space()

        # MultiDiscrete with (1 + len(zones)) actions per node
        assert action_space.shape == (len(config.nodes),)
        assert all(n == 1 + len(config.zones) for n in action_space.nvec)

    def test_to_dict(self) -> None:
        """
        Tests the to_dict method.

        :return: None
        """
        config = self.get_example_config()
        d = config.to_dict()

        assert isinstance(d, dict)
        assert d["env_name"] == "test-workflow-env"
        assert d["X_max"] == 10
        assert d["beta"] == 1.0
        assert d["gamma"] == 0.99
        assert d["eta"] == 0.5
        assert "nodes" in d
        assert "initial_zones" in d
        assert "zones" in d
        assert "adjacency_matrix" in d
        assert "Z_D_P" in d
        assert "C_D" in d
        assert "A_P" in d
        assert "Z_U" in d
        assert "gw_reachable" in d

    def test_from_dict(self) -> None:
        """
        Tests the from_dict method.

        :return: None
        """
        config = self.get_example_config()
        d = config.to_dict()
        restored = WorkflowIntrusionResponseGameConfig.from_dict(d)

        assert restored.env_name == config.env_name
        assert restored.X_max == config.X_max
        assert restored.beta == config.beta
        assert restored.gamma == config.gamma
        assert restored.eta == config.eta
        assert len(restored.nodes) == len(config.nodes)
        assert len(restored.zones) == len(config.zones)
        assert np.allclose(restored.adjacency_matrix, config.adjacency_matrix)
        assert np.allclose(restored.gw_reachable, config.gw_reachable)

    def test_roundtrip_dict(self) -> None:
        """
        Tests roundtrip conversion through dict.

        :return: None
        """
        config = self.get_example_config()
        d = config.to_dict()
        restored = WorkflowIntrusionResponseGameConfig.from_dict(d)
        d2 = restored.to_dict()

        # Check all keys match
        assert set(d.keys()) == set(d2.keys())

        # Check scalar values match
        assert d["env_name"] == d2["env_name"]
        assert d["X_max"] == d2["X_max"]
        assert d["beta"] == d2["beta"]
        assert d["gamma"] == d2["gamma"]
        assert d["eta"] == d2["eta"]

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

        restored = WorkflowIntrusionResponseGameConfig.from_json_file(json_path)

        assert restored.env_name == config.env_name
        assert restored.X_max == config.X_max
        assert len(restored.nodes) == len(config.nodes)

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
        assert d2["env_name"] == "test-workflow-env"

    def test_different_network_topologies(self) -> None:
        """
        Tests config with different network topologies.

        :return: None
        """
        # Star topology (3 nodes, one central)
        adjacency_matrix = np.array([
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 0]
        ])
        config = WorkflowIntrusionResponseGameConfig(
            env_name="star-topology",
            adjacency_matrix=adjacency_matrix,
            nodes=np.array([0, 1, 2]),
            initial_zones=np.array([1, 2, 3]),
            X_max=5,
            beta=0.5,
            gamma=0.95,
            zones=np.array([1, 2, 3]),
            Z_D_P=np.array([0.1, 0.1, 0.1]),
            C_D=np.array([0.0, 0.1, 0.1, 0.1]),
            A_P=np.array([1.0, 1.0, 0.5, 0.5]),
            Z_U=np.array([1.0, 1.0, 1.0]),
            eta=0.5,
            gw_reachable=np.array([1, 0, 0])
        )

        assert config.adjacency_matrix.shape == (3, 3)
        assert len(config.nodes) == 3
        assert config.defender_action_space().shape == (3,)
        assert config.attacker_action_space().shape == (3,)
