/**
 * @vitest-environment jsdom
 */
import { test, expect, vi, beforeEach, afterEach } from 'vitest';
import getWindowDimensions from "./getDimensions";

/**
 * Tests the getWindowDimensions() function
 */
beforeEach(() => {
    // Store original window properties
    vi.stubGlobal('window', {
        innerWidth: 1920,
        innerHeight: 1080
    });
});

afterEach(() => {
    vi.unstubAllGlobals();
});

test('getWindowDimensions returns width and height from window object', () => {
    const result = getWindowDimensions();
    expect(result).toEqual({ width: 1920, height: 1080 });
});

test('getWindowDimensions returns correct dimensions for different window sizes', () => {
    vi.stubGlobal('window', {
        innerWidth: 800,
        innerHeight: 600
    });
    const result = getWindowDimensions();
    expect(result).toEqual({ width: 800, height: 600 });
});
