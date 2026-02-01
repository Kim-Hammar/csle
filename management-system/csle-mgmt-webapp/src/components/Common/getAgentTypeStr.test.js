import { test, expect } from 'vitest';
import getAgentTypeStr from "./getAgentTypeStr";

/**
 * Tests the getAgentTypeStr() function
 */
test('getAgentTypeStr returns correct string for each agent type', () => {
    expect(getAgentTypeStr(0)).toBe("T-SPSA");
    expect(getAgentTypeStr(1)).toBe("PPO");
    expect(getAgentTypeStr(2)).toBe("T-FP");
    expect(getAgentTypeStr(3)).toBe("DQN");
    expect(getAgentTypeStr(4)).toBe("REINFORCE");
    expect(getAgentTypeStr(5)).toBe("NFSP");
    expect(getAgentTypeStr(6)).toBe("RANDOM");
    expect(getAgentTypeStr(7)).toBe("NONE");
    expect(getAgentTypeStr(8)).toBe("VALUE ITERATION");
    expect(getAgentTypeStr(9)).toBe("HSVI");
    expect(getAgentTypeStr(10)).toBe("SONDIK's VALUE ITERATION");
    expect(getAgentTypeStr(11)).toBe("RANDOM SEARCH");
    expect(getAgentTypeStr(12)).toBe("DIFFERENTIAL EVOLUTION");
    expect(getAgentTypeStr(13)).toBe("CROSS ENTROPY METHOD");
    expect(getAgentTypeStr(14)).toBe("KIEFER WOLFOWITZ");
    expect(getAgentTypeStr(15)).toBe("Q_LEARNING");
    expect(getAgentTypeStr(16)).toBe("SARSA");
    expect(getAgentTypeStr(17)).toBe("POLICY ITERATION");
    expect(getAgentTypeStr(18)).toBe("SHAPLEY ITERATION");
    expect(getAgentTypeStr(19)).toBe("HSVI for OS-POSGs");
    expect(getAgentTypeStr(20)).toBe("FICTITIOUS PLAY");
    expect(getAgentTypeStr(21)).toBe("LINEAR PROGRAMMING FOR NORMAL-FORM GAMES");
    expect(getAgentTypeStr(22)).toBe("DynaSec");
    expect(getAgentTypeStr(23)).toBe("BAYESIAN OPTIMIZATION");
    expect(getAgentTypeStr(24)).toBe("DFSP LOCAL");
    expect(getAgentTypeStr(25)).toBe("LINEAR PROGRAMMING CMDP");
    expect(getAgentTypeStr(26)).toBe("BAYESIAN OPTIMIZATION EMUKIT");
    expect(getAgentTypeStr(27)).toBe("SIMULATED ANNEALING");
    expect(getAgentTypeStr(28)).toBe("CMA-ES");
    expect(getAgentTypeStr(29)).toBe("NELDER-MEAD");
    expect(getAgentTypeStr(30)).toBe("PARTICLE SWARM");
    expect(getAgentTypeStr(31)).toBe("PPO CLEAN");
    expect(getAgentTypeStr(32)).toBe("POMCP");
    expect(getAgentTypeStr(33)).toBe("DQN CLEAN");
    expect(getAgentTypeStr(34)).toBe("C51 CLEAN");
    expect(getAgentTypeStr(35)).toBe("PPG CLEAN");
    expect(getAgentTypeStr(36)).toBe("MCS");
});

test('getAgentTypeStr returns Unknown for invalid agent type', () => {
    expect(getAgentTypeStr(37)).toBe("Unknown");
    expect(getAgentTypeStr(-1)).toBe("Unknown");
    expect(getAgentTypeStr(100)).toBe("Unknown");
    expect(getAgentTypeStr(null)).toBe("Unknown");
    expect(getAgentTypeStr(undefined)).toBe("Unknown");
});
