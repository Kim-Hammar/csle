import { test, expect } from 'vitest';
import getDateStr from "./getDateStr";

/**
 * Tests the getDateStr() function
 */
test('getDateStr converts Unix timestamp to formatted date string', () => {
    // Test with a known timestamp: 1609459200 = 2021-01-01 00:00:00 UTC
    const result = getDateStr(1609459200);
    // The function uses local timezone, so we verify the format pattern
    expect(result).toMatch(/^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{2}:\d{2}$/);
});

test('getDateStr handles zero timestamp', () => {
    const result = getDateStr(0);
    // Unix epoch: 1970-01-01
    expect(result).toMatch(/^1970-/);
});

test('getDateStr formats minutes and seconds with leading zeros', () => {
    // Timestamp where minutes and seconds need padding
    const result = getDateStr(1609459205); // 5 seconds after midnight
    expect(result).toMatch(/:\d{2}:\d{2}$/);
});
