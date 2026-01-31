import math


def calculate_shannon_limit(bandwidth_hz, snr_db):
    """
    Calculates the Shannon limit (theoretical maximum channel capacity).

    Args:
        bandwidth_hz (float): Bandwidth in Hertz (e.g., 5e6 for 5 MHz).
        snr_db (float): Signal-to-Noise Ratio in decibels (dB).

    Returns:
        float: Maximum theoretical capacity in bits per second (bps).
    """
    # 1. Convert SNR from dB to linear scale
    # Formula: SNR_linear = 10^(SNR_dB / 10)
    snr_linear = 10 ** (snr_db / 10.0)

    # 2. Apply Shannon-Hartley Theorem
    # Formula: C = B * log2(1 + SNR_linear)
    capacity_bps = bandwidth_hz * math.log2(1 + snr_linear)

    return capacity_bps


# --- Example Usage ---
bw = 5_000_000  # 5 MHz
# snr = 10.5
snr = 2.2

limit = calculate_shannon_limit(bw, snr)

print(f"Bandwidth: {bw / 1e6} MHz")
print(f"SNR: {snr} dB")
print(f"Shannon Limit: {limit / 1e6:.2f} Mbps")