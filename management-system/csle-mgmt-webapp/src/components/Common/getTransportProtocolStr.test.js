import { test, expect } from 'vitest';
import getTransportProtocolStr from "./getTransportProtocolStr";

/**
 * Tests the getTransportProtocolStr() function
 */
test('getTransportProtocolStr returns correct string for each protocol type', () => {
    expect(getTransportProtocolStr(0)).toBe("TCP");
    expect(getTransportProtocolStr(1)).toBe("UDP");
});

test('getTransportProtocolStr returns Unknown for invalid protocol type', () => {
    expect(getTransportProtocolStr(2)).toBe("Unknown");
    expect(getTransportProtocolStr(-1)).toBe("Unknown");
    expect(getTransportProtocolStr(100)).toBe("Unknown");
    expect(getTransportProtocolStr(null)).toBe("Unknown");
    expect(getTransportProtocolStr(undefined)).toBe("Unknown");
});
