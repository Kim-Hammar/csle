"""
Unit tests for the constants module.
"""
import numpy as np

import gym_csle_intrusion_response_game.constants.constants as env_constants


class TestConstantsSuite:
    """
    Test suite for the constants module.
    """

    def test_zones_constants(self) -> None:
        """
        Tests the ZONES constants.

        :return: None
        """
        assert env_constants.ZONES.REDIRECTION_ZONE == 1
        assert env_constants.ZONES.SHUTDOWN_ZONE == 0
        # Shutdown should be less than redirection
        assert env_constants.ZONES.SHUTDOWN_ZONE < env_constants.ZONES.REDIRECTION_ZONE

    def test_states_constants(self) -> None:
        """
        Tests the STATES constants.

        :return: None
        """
        assert env_constants.STATES.D_STATE_INDEX == 0
        assert env_constants.STATES.A_STATE_INDEX == 1
        # Terminal state should be [-1, -1]
        assert np.array_equal(env_constants.STATES.TERMINAL_STATE, np.array([-1, -1]))

    def test_attack_states_constants(self) -> None:
        """
        Tests the ATTACK_STATES constants.

        :return: None
        """
        assert env_constants.ATTACK_STATES.HEALTHY == 0
        assert env_constants.ATTACK_STATES.RECON == 1
        assert env_constants.ATTACK_STATES.COMPROMISED == 2
        # States should be ordered by severity
        assert env_constants.ATTACK_STATES.HEALTHY < env_constants.ATTACK_STATES.RECON
        assert env_constants.ATTACK_STATES.RECON < env_constants.ATTACK_STATES.COMPROMISED

    def test_defender_states_constants(self) -> None:
        """
        Tests the DEFENDER_STATES constants.

        :return: None
        """
        assert env_constants.DEFENDER_STATES.SHUTDOWN == 1
        assert env_constants.DEFENDER_STATES.REDIRECT == 2

    def test_attacker_actions_constants(self) -> None:
        """
        Tests the ATTACKER_ACTIONS constants.

        :return: None
        """
        assert env_constants.ATTACKER_ACTIONS.WAIT == 0
        assert env_constants.ATTACKER_ACTIONS.RECON == 1
        assert env_constants.ATTACKER_ACTIONS.BRUTE_FORCE == 2
        assert env_constants.ATTACKER_ACTIONS.EXPLOIT == 3
        # All actions should be unique
        actions = [
            env_constants.ATTACKER_ACTIONS.WAIT,
            env_constants.ATTACKER_ACTIONS.RECON,
            env_constants.ATTACKER_ACTIONS.BRUTE_FORCE,
            env_constants.ATTACKER_ACTIONS.EXPLOIT
        ]
        assert len(actions) == len(set(actions))

    def test_defender_actions_constants(self) -> None:
        """
        Tests the DEFENDER_ACTIONS constants.

        :return: None
        """
        assert env_constants.DEFENDER_ACTIONS.WAIT == 0

    def test_static_defender_strategies_constants(self) -> None:
        """
        Tests the STATIC_DEFENDER_STRATEGIES constants.

        :return: None
        """
        assert env_constants.STATIC_DEFENDER_STRATEGIES.RANDOM == "random"

    def test_static_attacker_strategies_constants(self) -> None:
        """
        Tests the STATIC_ATTACKER_STRATEGIES constants.

        :return: None
        """
        assert env_constants.STATIC_ATTACKER_STRATEGIES.RANDOM == "random"

    def test_env_metrics_constants(self) -> None:
        """
        Tests the ENV_METRICS constants.

        :return: None
        """
        assert env_constants.ENV_METRICS.RETURN == "R"
        assert env_constants.ENV_METRICS.TIME_HORIZON == "T"
        assert env_constants.ENV_METRICS.STATE == "s"
        assert env_constants.ENV_METRICS.DEFENDER_ACTION == "a1"
        assert env_constants.ENV_METRICS.ATTACKER_ACTION == "a2"
        assert env_constants.ENV_METRICS.OBSERVATION == "o"
        assert env_constants.ENV_METRICS.TIME_STEP == "t"
        assert env_constants.ENV_METRICS.INTRUSION_LENGTH == "intrusion_length"
        assert env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN == "average_upper_bound_return"
        assert env_constants.ENV_METRICS.AVERAGE_RANDOM_RETURN == "average_random_return"
        assert env_constants.ENV_METRICS.AVERAGE_HEURISTIC_RETURN == "average_heuristic_return"
        assert env_constants.ENV_METRICS.INTRUSION_START == "intrusion_start"
        assert env_constants.ENV_METRICS.WEIGHTED_INTRUSION_PREDICTION_DISTANCE == \
            "weighted_intrusion_prediction_distance"
        assert env_constants.ENV_METRICS.START_POINT_CORRECT == "start_point_correct"
        assert env_constants.ENV_METRICS.INTRUSION_END == "intrusion_end"

    def test_terminal_state_is_recognizable(self) -> None:
        """
        Tests that terminal state can be recognized.

        :return: None
        """
        terminal = env_constants.STATES.TERMINAL_STATE
        # Both values should be -1
        assert terminal[env_constants.STATES.D_STATE_INDEX] == -1
        assert terminal[env_constants.STATES.A_STATE_INDEX] == -1

    def test_action_indices_match_conventions(self) -> None:
        """
        Tests that action indices follow expected conventions.

        :return: None
        """
        # WAIT should always be 0 for both players
        assert env_constants.ATTACKER_ACTIONS.WAIT == 0
        assert env_constants.DEFENDER_ACTIONS.WAIT == 0

    def test_constants_classes_have_expected_attributes(self) -> None:
        """
        Tests that constant classes have expected attributes.

        :return: None
        """
        # ZONES class
        assert hasattr(env_constants.ZONES, 'REDIRECTION_ZONE')
        assert hasattr(env_constants.ZONES, 'SHUTDOWN_ZONE')

        # STATES class
        assert hasattr(env_constants.STATES, 'TERMINAL_STATE')
        assert hasattr(env_constants.STATES, 'D_STATE_INDEX')
        assert hasattr(env_constants.STATES, 'A_STATE_INDEX')

        # ATTACK_STATES class
        assert hasattr(env_constants.ATTACK_STATES, 'HEALTHY')
        assert hasattr(env_constants.ATTACK_STATES, 'RECON')
        assert hasattr(env_constants.ATTACK_STATES, 'COMPROMISED')

        # ATTACKER_ACTIONS class
        assert hasattr(env_constants.ATTACKER_ACTIONS, 'WAIT')
        assert hasattr(env_constants.ATTACKER_ACTIONS, 'RECON')
        assert hasattr(env_constants.ATTACKER_ACTIONS, 'BRUTE_FORCE')
        assert hasattr(env_constants.ATTACKER_ACTIONS, 'EXPLOIT')
