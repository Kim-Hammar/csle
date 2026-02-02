import { test, expect } from 'vitest';
import getPlayerTypeStr from "./getPlayerTypeStr";

/**
 * Tests the getPlayerTypeStr() function
 */
test('getPlayerTypeStr returns correct string for each player type', () => {
    expect(getPlayerTypeStr(1)).toBe("Defender");
    expect(getPlayerTypeStr(2)).toBe("Attacker");
    expect(getPlayerTypeStr(3)).toBe("Self Play");
});

test('getPlayerTypeStr returns Unknown for invalid player type', () => {
    expect(getPlayerTypeStr(0)).toBe("Unknown");
    expect(getPlayerTypeStr(4)).toBe("Unknown");
    expect(getPlayerTypeStr(-1)).toBe("Unknown");
    expect(getPlayerTypeStr(null)).toBe("Unknown");
    expect(getPlayerTypeStr(undefined)).toBe("Unknown");
});
