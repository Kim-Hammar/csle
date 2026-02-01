import { test, expect } from 'vitest';
import getSystemModelTypeStr from "./getSystemModelTypeStr";

/**
 * Tests the getSystemModelTypeStr() function
 */
test('getSystemModelTypeStr returns correct string for each model type', () => {
    expect(getSystemModelTypeStr(0)).toBe("gaussian_mixture");
    expect(getSystemModelTypeStr(1)).toBe("empirical");
    expect(getSystemModelTypeStr(2)).toBe("gp");
    expect(getSystemModelTypeStr(3)).toBe("mcmc");
});

test('getSystemModelTypeStr returns Unknown for invalid model type', () => {
    expect(getSystemModelTypeStr(4)).toBe("Unknown");
    expect(getSystemModelTypeStr(-1)).toBe("Unknown");
    expect(getSystemModelTypeStr(100)).toBe("Unknown");
    expect(getSystemModelTypeStr(null)).toBe("Unknown");
    expect(getSystemModelTypeStr(undefined)).toBe("Unknown");
});
