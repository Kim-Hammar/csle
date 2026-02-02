import { test, expect } from 'vitest';
import parseLogs from "./parseLogs";

/**
 * Tests the parseLogs() function
 */
test('parseLogs converts log lines to indexed objects', () => {
    const lines = ["Error: connection failed", "Warning: timeout", "Info: connected"];
    const result = parseLogs(lines);
    expect(result).toEqual([
        { index: 0, content: "Error: connection failed" },
        { index: 1, content: "Warning: timeout" },
        { index: 2, content: "Info: connected" }
    ]);
});

test('parseLogs returns empty array for empty input', () => {
    expect(parseLogs([])).toEqual([]);
});

test('parseLogs handles single log line', () => {
    const lines = ["Single log entry"];
    const result = parseLogs(lines);
    expect(result).toEqual([{ index: 0, content: "Single log entry" }]);
});

test('parseLogs preserves empty string content', () => {
    const lines = ["", "non-empty", ""];
    const result = parseLogs(lines);
    expect(result).toEqual([
        { index: 0, content: "" },
        { index: 1, content: "non-empty" },
        { index: 2, content: "" }
    ]);
});
