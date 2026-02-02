import { test, expect } from 'vitest';
import getBoolStr from "./getBoolStr";

/**
 * Tests the getBoolStr() function
 */
test('getBoolStr returns "true" for truthy values', () => {
    expect(getBoolStr(true)).toBe("true");
    expect(getBoolStr(1)).toBe("true");
    expect(getBoolStr("non-empty")).toBe("true");
});

test('getBoolStr returns "false" for falsy values', () => {
    expect(getBoolStr(false)).toBe("false");
    expect(getBoolStr(0)).toBe("false");
    expect(getBoolStr(null)).toBe("false");
    expect(getBoolStr(undefined)).toBe("false");
    expect(getBoolStr("")).toBe("false");
});
