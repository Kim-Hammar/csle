/**
 * @vitest-environment jsdom
 */
import { test, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import useSession from "./useSession";

/**
 * Tests the useSession() hook
 */
beforeEach(() => {
    // Mock localStorage
    const localStorageMock = {
        getItem: vi.fn(),
        setItem: vi.fn(),
        removeItem: vi.fn(),
        clear: vi.fn()
    };
    vi.stubGlobal('localStorage', localStorageMock);
});

afterEach(() => {
    vi.unstubAllGlobals();
});

test('useSession returns null session data when localStorage is empty', () => {
    localStorage.getItem.mockReturnValue(null);
    const { result } = renderHook(() => useSession());
    expect(result.current.sessionData).toBeNull();
});

test('useSession returns parsed session data from localStorage', () => {
    const mockSession = { username: 'testuser', token: 'abc123' };
    localStorage.getItem.mockReturnValue(JSON.stringify(mockSession));
    const { result } = renderHook(() => useSession());
    expect(result.current.sessionData).toEqual(mockSession);
});

test('useSession saves session data to localStorage', () => {
    localStorage.getItem.mockReturnValue(null);
    const { result } = renderHook(() => useSession());

    const newSession = { username: 'newuser', token: 'xyz789' };
    act(() => {
        result.current.setSessionData(newSession);
    });

    expect(localStorage.setItem).toHaveBeenCalledWith('csleSession', JSON.stringify(newSession));
    expect(result.current.sessionData).toEqual(newSession);
});

test('useSession updates state when saving new session data', () => {
    localStorage.getItem.mockReturnValue(null);
    const { result } = renderHook(() => useSession());

    act(() => {
        result.current.setSessionData({ id: 1 });
    });
    expect(result.current.sessionData).toEqual({ id: 1 });

    act(() => {
        result.current.setSessionData({ id: 2 });
    });
    expect(result.current.sessionData).toEqual({ id: 2 });
});
