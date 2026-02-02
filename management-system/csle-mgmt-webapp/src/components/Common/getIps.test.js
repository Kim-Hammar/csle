import { test, expect } from 'vitest';
import getIps from "./getIps";

/**
 * Tests the getIps() function
 */
test('getIps extracts IPs from array of IP/network tuples', () => {
    const ipsAndNetworks = [
        ["192.168.1.1", "192.168.1.0/24"],
        ["10.0.0.1", "10.0.0.0/8"],
        ["172.16.0.1", "172.16.0.0/16"]
    ];
    expect(getIps(ipsAndNetworks)).toEqual(["192.168.1.1", "10.0.0.1", "172.16.0.1"]);
});

test('getIps returns empty array for empty input', () => {
    expect(getIps([])).toEqual([]);
});

test('getIps handles single element array', () => {
    const ipsAndNetworks = [["127.0.0.1", "127.0.0.0/8"]];
    expect(getIps(ipsAndNetworks)).toEqual(["127.0.0.1"]);
});
