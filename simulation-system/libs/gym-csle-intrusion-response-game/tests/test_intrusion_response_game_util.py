"""
Unit tests for intrusion_response_game_util.py
"""
from typing import List
import numpy as np
import pytest

from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
import gym_csle_intrusion_response_game.constants.constants as env_constants


class TestIntrusionResponseGameUtilSuite:
    """
    Test suite for IntrusionResponseGameUtil class.
    """

    def test_is_local_state_terminal(self) -> None:
        """
        Tests the is_local_state_terminal function.

        :return: None
        """
        assert IntrusionResponseGameUtil.is_local_state_terminal(np.array([-1, -1]))
        assert not IntrusionResponseGameUtil.is_local_state_terminal(np.array([0, -1]))
        assert not IntrusionResponseGameUtil.is_local_state_terminal(np.array([-1, 0]))
        assert not IntrusionResponseGameUtil.is_local_state_terminal(np.array([0, 0]))
        assert not IntrusionResponseGameUtil.is_local_state_terminal(np.array([1, 2]))

    def test_is_local_state_in_zone(self) -> None:
        """
        Tests the is_local_state_in_zone function.

        :return: None
        """
        state = np.array([1, 0])  # D_STATE_INDEX=0, A_STATE_INDEX=1
        assert IntrusionResponseGameUtil.is_local_state_in_zone(state, zone=1)
        assert not IntrusionResponseGameUtil.is_local_state_in_zone(state, zone=2)
        assert not IntrusionResponseGameUtil.is_local_state_in_zone(state, zone=0)

        state2 = np.array([3, 2])
        assert IntrusionResponseGameUtil.is_local_state_in_zone(state2, zone=3)

    def test_is_local_state_shutdown_or_redirect(self) -> None:
        """
        Tests the is_local_state_shutdown_or_redirect function.

        :return: None
        """
        shutdown_state = np.array([env_constants.DEFENDER_STATES.SHUTDOWN, 0])
        redirect_state = np.array([env_constants.DEFENDER_STATES.REDIRECT, 0])
        normal_state = np.array([3, 0])

        assert IntrusionResponseGameUtil.is_local_state_shutdown_or_redirect(shutdown_state)
        assert IntrusionResponseGameUtil.is_local_state_shutdown_or_redirect(redirect_state)
        assert not IntrusionResponseGameUtil.is_local_state_shutdown_or_redirect(normal_state)

    def test_is_local_state_compromised(self) -> None:
        """
        Tests the is_local_state_compromised function.

        :return: None
        """
        compromised_state = np.array([1, env_constants.ATTACK_STATES.COMPROMISED])
        healthy_state = np.array([1, env_constants.ATTACK_STATES.HEALTHY])
        recon_state = np.array([1, env_constants.ATTACK_STATES.RECON])

        assert IntrusionResponseGameUtil.is_local_state_compromised(compromised_state)
        assert not IntrusionResponseGameUtil.is_local_state_compromised(healthy_state)
        assert not IntrusionResponseGameUtil.is_local_state_compromised(recon_state)

    def test_is_local_state_healthy(self) -> None:
        """
        Tests the is_local_state_healthy function.

        :return: None
        """
        healthy_state = np.array([1, env_constants.ATTACK_STATES.HEALTHY])
        compromised_state = np.array([1, env_constants.ATTACK_STATES.COMPROMISED])
        recon_state = np.array([1, env_constants.ATTACK_STATES.RECON])

        assert IntrusionResponseGameUtil.is_local_state_healthy(healthy_state)
        assert not IntrusionResponseGameUtil.is_local_state_healthy(compromised_state)
        assert not IntrusionResponseGameUtil.is_local_state_healthy(recon_state)

    def test_is_local_state_recon(self) -> None:
        """
        Tests the is_local_state_recon function.

        :return: None
        """
        recon_state = np.array([1, env_constants.ATTACK_STATES.RECON])
        healthy_state = np.array([1, env_constants.ATTACK_STATES.HEALTHY])
        compromised_state = np.array([1, env_constants.ATTACK_STATES.COMPROMISED])

        assert IntrusionResponseGameUtil.is_local_state_recon(recon_state)
        assert not IntrusionResponseGameUtil.is_local_state_recon(healthy_state)
        assert not IntrusionResponseGameUtil.is_local_state_recon(compromised_state)

    def test_are_local_states_equal(self) -> None:
        """
        Tests the are_local_states_equal function.

        :return: None
        """
        s1 = np.array([1, 2])
        s2 = np.array([1, 2])
        s3 = np.array([1, 3])
        s4 = np.array([2, 2])

        assert IntrusionResponseGameUtil.are_local_states_equal(s1, s2)
        assert not IntrusionResponseGameUtil.are_local_states_equal(s1, s3)
        assert not IntrusionResponseGameUtil.are_local_states_equal(s1, s4)

    def test_are_local_defense_states_equal(self) -> None:
        """
        Tests the are_local_defense_states_equal function.

        :return: None
        """
        s1 = np.array([1, 2])
        s2 = np.array([1, 3])  # Same defense state, different attack state
        s3 = np.array([2, 2])  # Different defense state

        assert IntrusionResponseGameUtil.are_local_defense_states_equal(s1, s2)
        assert not IntrusionResponseGameUtil.are_local_defense_states_equal(s1, s3)

    def test_are_local_attack_states_equal(self) -> None:
        """
        Tests the are_local_attack_states_equal function.

        :return: None
        """
        s1 = np.array([1, 2])
        s2 = np.array([3, 2])  # Different defense state, same attack state
        s3 = np.array([1, 3])  # Same defense state, different attack state

        assert IntrusionResponseGameUtil.are_local_attack_states_equal(s1, s2)
        assert not IntrusionResponseGameUtil.are_local_attack_states_equal(s1, s3)

    def test_local_state_space(self) -> None:
        """
        Tests the local_state_space function.

        :return: None
        """
        S = IntrusionResponseGameUtil.local_state_space(number_of_zones=3)

        # Should have 1 terminal state + 3 zones * 3 attack states = 10 states
        assert len(S) == 10
        # First state should be terminal
        assert list(S[0]) == [-1, -1]
        # Check zone 1 states
        assert list(S[1]) == [1, env_constants.ATTACK_STATES.HEALTHY]
        assert list(S[2]) == [1, env_constants.ATTACK_STATES.RECON]
        assert list(S[3]) == [1, env_constants.ATTACK_STATES.COMPROMISED]

    def test_local_defender_state_space(self) -> None:
        """
        Tests the local_defender_state_space function.

        :return: None
        """
        S_D = IntrusionResponseGameUtil.local_defender_state_space(number_of_zones=4)
        assert len(S_D) == 4
        assert list(S_D) == [1, 2, 3, 4]

    def test_local_attacker_state_space(self) -> None:
        """
        Tests the local_attacker_state_space function.

        :return: None
        """
        S_A = IntrusionResponseGameUtil.local_attacker_state_space()
        assert len(S_A) == 3
        assert env_constants.ATTACK_STATES.HEALTHY in S_A
        assert env_constants.ATTACK_STATES.RECON in S_A
        assert env_constants.ATTACK_STATES.COMPROMISED in S_A

    def test_local_defender_actions(self) -> None:
        """
        Tests the local_defender_actions function.

        :return: None
        """
        A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=3)
        assert len(A1) == 4  # 0 (wait) + 3 zones
        assert list(A1) == [0, 1, 2, 3]

    def test_local_attacker_actions(self) -> None:
        """
        Tests the local_attacker_actions function.

        :return: None
        """
        A2 = IntrusionResponseGameUtil.local_attacker_actions()
        assert len(A2) == 4
        assert env_constants.ATTACKER_ACTIONS.WAIT in A2
        assert env_constants.ATTACKER_ACTIONS.RECON in A2
        assert env_constants.ATTACKER_ACTIONS.BRUTE_FORCE in A2
        assert env_constants.ATTACKER_ACTIONS.EXPLOIT in A2

    def test_local_observation_space(self) -> None:
        """
        Tests the local_observation_space function.

        :return: None
        """
        O = IntrusionResponseGameUtil.local_observation_space(X_max=10)
        assert len(O) == 10
        assert list(O) == list(range(10))

    def test_zones(self) -> None:
        """
        Tests the zones function.

        :return: None
        """
        zones = IntrusionResponseGameUtil.zones(num_zones=5)
        assert len(zones) == 5
        assert list(zones) == [1, 2, 3, 4, 5]

    def test_constant_defender_action_costs(self) -> None:
        """
        Tests the constant_defender_action_costs function.

        :return: None
        """
        A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=3)
        costs = IntrusionResponseGameUtil.constant_defender_action_costs(A1, constant_cost=0.5)

        assert len(costs) == 4
        assert costs[env_constants.DEFENDER_ACTIONS.WAIT] == 0.0  # Wait should have 0 cost
        assert costs[1] == 0.5
        assert costs[2] == 0.5
        assert costs[3] == 0.5

    def test_constant_zone_utilities(self) -> None:
        """
        Tests the constant_zone_utilities function.

        :return: None
        """
        zones = IntrusionResponseGameUtil.zones(num_zones=3)
        utilities = IntrusionResponseGameUtil.constant_zone_utilities(zones, constant_utility=1.0)

        assert len(utilities) == 3
        assert all(u == 1.0 for u in utilities)

    def test_constant_zone_detection_probabilities(self) -> None:
        """
        Tests the constant_zone_detection_probabilities function.

        :return: None
        """
        zones = IntrusionResponseGameUtil.zones(num_zones=3)
        probs = IntrusionResponseGameUtil.constant_zone_detection_probabilities(zones, constant_detection_prob=0.1)

        assert len(probs) == 3
        # None should be shutdown zone (0), so all should have the constant probability
        assert all(p == 0.1 for p in probs)

    def test_local_attack_success_probabilities_uniform(self) -> None:
        """
        Tests the local_attack_success_probabilities_uniform function.

        :return: None
        """
        A2 = IntrusionResponseGameUtil.local_attacker_actions()
        probs = IntrusionResponseGameUtil.local_attack_success_probabilities_uniform(p=0.5, A2=A2)

        assert len(probs) == 4
        assert probs[env_constants.ATTACKER_ACTIONS.WAIT] == 1.0
        assert probs[env_constants.ATTACKER_ACTIONS.RECON] == 1.0
        assert probs[env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] == 0.5
        assert probs[env_constants.ATTACKER_ACTIONS.EXPLOIT] == 0.5

    def test_local_attack_success_probabilities_bounds(self) -> None:
        """
        Tests that local_attack_success_probabilities_uniform validates probability bounds.

        :return: None
        """
        A2 = IntrusionResponseGameUtil.local_attacker_actions()

        # Test valid bounds
        probs = IntrusionResponseGameUtil.local_attack_success_probabilities_uniform(p=0.0, A2=A2)
        assert probs[env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] == 0.0

        probs = IntrusionResponseGameUtil.local_attack_success_probabilities_uniform(p=1.0, A2=A2)
        assert probs[env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] == 1.0

        # Test invalid bounds (should raise AssertionError)
        with pytest.raises(AssertionError):
            IntrusionResponseGameUtil.local_attack_success_probabilities_uniform(p=1.5, A2=A2)

        with pytest.raises(AssertionError):
            IntrusionResponseGameUtil.local_attack_success_probabilities_uniform(p=-0.1, A2=A2)

    def test_local_initial_defender_belief(self) -> None:
        """
        Tests the local_initial_defender_belief function.

        :return: None
        """
        S_A = IntrusionResponseGameUtil.local_attacker_state_space()
        belief = IntrusionResponseGameUtil.local_initial_defender_belief(S_A)

        assert len(belief) == 3
        assert belief[env_constants.ATTACK_STATES.HEALTHY] == 1.0
        assert belief[env_constants.ATTACK_STATES.RECON] == 0.0
        assert belief[env_constants.ATTACK_STATES.COMPROMISED] == 0.0
        assert sum(belief) == 1.0

    def test_local_initial_attacker_belief(self) -> None:
        """
        Tests the local_initial_attacker_belief function.

        :return: None
        """
        S_D = IntrusionResponseGameUtil.local_defender_state_space(number_of_zones=3)
        belief = IntrusionResponseGameUtil.local_initial_attacker_belief(S_D, initial_zone=1)

        assert len(belief) == 3
        # Uniform distribution
        assert abs(sum(belief) - 1.0) < 0.001
        for b in belief:
            assert abs(b - 1.0 / 3.0) < 0.001

    def test_local_initial_state_distribution(self) -> None:
        """
        Tests the local_initial_state_distribution function.

        :return: None
        """
        S = IntrusionResponseGameUtil.local_state_space(number_of_zones=3)
        rho = IntrusionResponseGameUtil.local_initial_state_distribution(initial_state_idx=1, S=S)

        assert len(rho) == len(S)
        assert rho[1] == 1.0
        assert sum(rho) == 1.0
        assert rho[0] == 0.0

    def test_local_initial_state(self) -> None:
        """
        Tests the local_initial_state function.

        :return: None
        """
        S = IntrusionResponseGameUtil.local_state_space(number_of_zones=3)
        # Wrap states to match expected format
        S_wrapped = [[s, s] for s in S]
        initial_state = IntrusionResponseGameUtil.local_initial_state(initial_zone=1, S=np.array(S_wrapped))

        # Should return a state in zone 1 that is healthy
        assert initial_state[0][env_constants.STATES.D_STATE_INDEX] == 1
        assert initial_state[1][env_constants.STATES.A_STATE_INDEX] == env_constants.ATTACK_STATES.HEALTHY

    def test_local_initial_state_idx(self) -> None:
        """
        Tests the local_initial_state_idx function.

        :return: None
        """
        S = IntrusionResponseGameUtil.local_state_space(number_of_zones=3)
        idx = IntrusionResponseGameUtil.local_initial_state_idx(initial_zone=1, S=S)

        # Index 1 should be zone 1, healthy
        assert S[idx][env_constants.STATES.D_STATE_INDEX] == 1
        assert S[idx][env_constants.STATES.A_STATE_INDEX] == env_constants.ATTACK_STATES.HEALTHY

    def test_local_initial_state_idx_raises_on_invalid_zone(self) -> None:
        """
        Tests that local_initial_state_idx raises ValueError for invalid zone.

        :return: None
        """
        S = IntrusionResponseGameUtil.local_state_space(number_of_zones=3)
        with pytest.raises(ValueError, match="Initial state not recognized"):
            IntrusionResponseGameUtil.local_initial_state_idx(initial_zone=99, S=S)

    def test_local_defender_utility_function_terminal_state(self) -> None:
        """
        Tests the local_defender_utility_function for terminal state.

        :return: None
        """
        terminal_state = np.array([-1, -1])
        C_D = np.array([0.0, 0.5, 0.5, 0.5])
        Z_U = np.array([1.0, 1.0, 1.0])

        utility = IntrusionResponseGameUtil.local_defender_utility_function(
            s=terminal_state, a1=0, eta=0.5, reachable=True, initial_zone=1, beta=1.0, C_D=C_D, Z_U=Z_U
        )
        assert utility == 0

    def test_local_reward_tensor_shape(self) -> None:
        """
        Tests that local_reward_tensor has correct shape.

        :return: None
        """
        S = IntrusionResponseGameUtil.local_state_space(number_of_zones=2)
        A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=2)
        A2 = IntrusionResponseGameUtil.local_attacker_actions()
        C_D = IntrusionResponseGameUtil.constant_defender_action_costs(A1, constant_cost=0.1)
        zones = IntrusionResponseGameUtil.zones(num_zones=2)
        Z_U = IntrusionResponseGameUtil.constant_zone_utilities(zones, constant_utility=1.0)

        R = IntrusionResponseGameUtil.local_reward_tensor(
            eta=0.5, C_D=C_D, reachable=True, Z_U=Z_U, initial_zone=1, beta=1.0, S=S, A1=A1, A2=A2
        )

        assert R.shape == (len(A1), len(A2), len(S))

    def test_local_transition_probability_terminal_state(self) -> None:
        """
        Tests local_transition_probability from terminal state.

        :return: None
        """
        terminal = np.array([-1, -1])
        non_terminal = np.array([1, 0])
        Z_D_P = np.array([0.1, 0.1])
        A_P = np.array([1.0, 1.0, 0.5, 0.5])

        # From terminal to terminal should be 1
        prob = IntrusionResponseGameUtil.local_transition_probability(
            s=terminal, s_prime=terminal, a1=0, a2=0, Z_D_P=Z_D_P, A_P=A_P
        )
        assert prob == 1.0

        # From terminal to non-terminal should be 0
        prob = IntrusionResponseGameUtil.local_transition_probability(
            s=terminal, s_prime=non_terminal, a1=0, a2=0, Z_D_P=Z_D_P, A_P=A_P
        )
        assert prob == 0.0

    def test_local_transition_tensor_probabilities_sum_to_one(self) -> None:
        """
        Tests that local_transition_tensor probabilities sum to 1 for each state-action pair.

        :return: None
        """
        num_zones = 2
        S = IntrusionResponseGameUtil.local_state_space(number_of_zones=num_zones)
        A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=num_zones)
        A2 = IntrusionResponseGameUtil.local_attacker_actions()
        zones = IntrusionResponseGameUtil.zones(num_zones=num_zones)
        Z_D = IntrusionResponseGameUtil.constant_zone_detection_probabilities(zones, constant_detection_prob=0.1)
        A_P = IntrusionResponseGameUtil.local_attack_success_probabilities_uniform(p=0.5, A2=A2)

        T = IntrusionResponseGameUtil.local_transition_tensor(Z_D=Z_D, A_P=A_P, S=S, A1=A1, A2=A2)

        # Check shape
        assert T.shape == (len(A1), len(A2), len(S), len(S))

        # Check probabilities sum to 1
        for a1 in range(len(A1)):
            for a2 in range(len(A2)):
                for s in range(len(S)):
                    prob_sum = sum(T[a1][a2][s])
                    assert abs(prob_sum - 1.0) < 0.001, f"Probs don't sum to 1 for a1={a1}, a2={a2}, s={s}"

    def test_sample_next_state(self) -> None:
        """
        Tests the sample_next_state function.

        :return: None
        """
        num_zones = 2
        S = IntrusionResponseGameUtil.local_state_space(number_of_zones=num_zones)
        A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=num_zones)
        A2 = IntrusionResponseGameUtil.local_attacker_actions()
        zones = IntrusionResponseGameUtil.zones(num_zones=num_zones)
        Z_D = IntrusionResponseGameUtil.constant_zone_detection_probabilities(zones, constant_detection_prob=0.0)
        A_P = IntrusionResponseGameUtil.local_attack_success_probabilities_uniform(p=0.5, A2=A2)
        T = IntrusionResponseGameUtil.local_transition_tensor(Z_D=Z_D, A_P=A_P, S=S, A1=A1, A2=A2)

        # From terminal state, should always stay in terminal
        terminal_idx = 0
        for _ in range(10):
            next_state = IntrusionResponseGameUtil.sample_next_state(
                T=T, s_idx=terminal_idx, a1=0, a2=0, S=S
            )
            assert next_state == terminal_idx

    def test_sample_attacker_action(self) -> None:
        """
        Tests the sample_attacker_action function.

        :return: None
        """
        # Deterministic policy
        pi2 = np.array([[1.0, 0.0, 0.0, 0.0]])
        for _ in range(10):
            action = IntrusionResponseGameUtil.sample_attacker_action(pi2=pi2, s=0)
            assert action == 0

        # Uniform policy
        pi2_uniform = np.array([[0.25, 0.25, 0.25, 0.25]])
        actions: List[int] = []
        for _ in range(100):
            action = IntrusionResponseGameUtil.sample_attacker_action(pi2=pi2_uniform, s=0)
            actions.append(action)
        # Should have some variety
        assert len(set(actions)) > 1

    def test_sample_defender_action(self) -> None:
        """
        Tests the sample_defender_action function.

        :return: None
        """
        # Deterministic policy
        pi1 = np.array([[1.0, 0.0, 0.0]])
        for _ in range(10):
            action = IntrusionResponseGameUtil.sample_defender_action(pi1=pi1, s=0)
            assert action == 0

    def test_local_observation_tensor_betabinom_shape(self) -> None:
        """
        Tests the local_observation_tensor_betabinom shape and normalization.

        :return: None
        """
        num_zones = 2
        S = IntrusionResponseGameUtil.local_state_space(number_of_zones=num_zones)
        A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=num_zones)
        A2 = IntrusionResponseGameUtil.local_attacker_actions()
        O = IntrusionResponseGameUtil.local_observation_space(X_max=10)

        Z = IntrusionResponseGameUtil.local_observation_tensor_betabinom(S=S, A1=A1, A2=A2, O=O)

        # Check shape
        assert Z.shape == (len(A1), len(A2), len(S), len(O))

        # Check probabilities sum to 1
        for a1 in range(len(A1)):
            for a2 in range(len(A2)):
                for s in range(len(S)):
                    prob_sum = sum(Z[a1][a2][s])
                    assert abs(prob_sum - 1.0) < 0.001

    def test_local_workflow_utility(self) -> None:
        """
        Tests the local_workflow_utility function.

        :return: None
        """
        # Node not reachable - utility should be 0
        state = np.array([1, 0])
        utility = IntrusionResponseGameUtil.local_workflow_utility(
            beta=1.0, reachable=False, s=state, initial_zone=1
        )
        assert utility == 0.0

        # Node compromised - utility should be 0
        compromised_state = np.array([1, env_constants.ATTACK_STATES.COMPROMISED])
        utility = IntrusionResponseGameUtil.local_workflow_utility(
            beta=1.0, reachable=True, s=compromised_state, initial_zone=1
        )
        assert utility == 0.0

        # Shutdown zone - utility should be 0
        shutdown_state = np.array([env_constants.ZONES.SHUTDOWN_ZONE, 0])
        utility = IntrusionResponseGameUtil.local_workflow_utility(
            beta=1.0, reachable=True, s=shutdown_state, initial_zone=1
        )
        assert utility == 0.0

    def test_local_intrusion_cost_unreachable(self) -> None:
        """
        Tests local_intrusion_cost when node is unreachable.

        :return: None
        """
        state = np.array([1, 0])
        C_D = np.array([0.0, 0.1, 0.1])
        Z_U = np.array([1.0, 1.0])

        cost = IntrusionResponseGameUtil.local_intrusion_cost(
            a1=1, D_C=C_D, reachable=False, s=state, Z_U=Z_U
        )
        assert cost == C_D[1]

    def test_local_intrusion_cost_compromised(self) -> None:
        """
        Tests local_intrusion_cost when node is compromised.

        :return: None
        """
        compromised_state = np.array([1, env_constants.ATTACK_STATES.COMPROMISED])
        C_D = np.array([0.0, 0.1, 0.1])
        Z_U = np.array([1.0, 2.0])

        cost = IntrusionResponseGameUtil.local_intrusion_cost(
            a1=0, D_C=C_D, reachable=True, s=compromised_state, Z_U=Z_U
        )
        # Should return zone utility (zone is 1, so index 0)
        assert cost == Z_U[0]
