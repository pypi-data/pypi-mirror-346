from scipy.signal import resample
from scipy.signal import iirnotch, filtfilt, butter
import numpy as np



def resample_data(data, old_sfreq, new_sfreq):
    """
    Resample EEG data to a new sampling frequency.

    Args:
        data (np.ndarray): EEG data, shape (n_channels, n_times)
        old_sfreq (float): Original sampling rate.
        new_sfreq (float): Target sampling rate.

    Returns:
        data_resampled (np.ndarray): Resampled EEG data.
    """
    n_channels, n_times = data.shape
    n_times_new = int(n_times * new_sfreq / old_sfreq)
    data_resampled = resample(data, n_times_new, axis=1)
    return data_resampled



def notch_filter(data, fs, filter_freq=50.0, Q=200):
    """
    Apply a notch filter at `freq` Hz to remove power line noise.

    Args:
        data (np.ndarray): EEG data (n_channels, n_times)
        fs (float): Sampling frequency
        filter_freq (float): Line noise frequency to remove (50 or 60 Hz)
        Q (float): Quality factor (higher = narrower notch)

    Returns:
        filtered_data (np.ndarray): EEG data with line noise removed
    """
    w0 = filter_freq / (fs / 2)  # Normalized frequency
    b, a = iirnotch(w0, Q)
    filtered_data = filtfilt(b, a, data, axis=1)
    return filtered_data


def bandpass_filter(data, freq, lowcut = None, highcut = None, order=5):
    """
    Apply bandpass Butterworth filter.

    Args:
        data (np.ndarray): EEG data, shape (n_channels, n_times)
        lowcut (float): Low cutoff frequency.
        highcut (float): High cutoff frequency.
        freq (float): Sampling frequency.
        order (int): Filter order.

    Returns:
        data_filtered (np.ndarray): Filtered EEG data.
    """
    nyq = 0.5 * freq  # Nyquist frequency
    low = lowcut / nyq if lowcut else 0
    high = highcut / nyq if highcut else 1

    if lowcut and highcut:
        btype = 'band'
    elif lowcut:
        btype = 'high'
    elif highcut:
        btype = 'low'
    else:
        raise ValueError("Must specify lowcut or highcut or both")

    b, a = butter(order, [low, high] if btype == 'band' else (low or high), btype=btype)
    data_filtered = filtfilt(b, a, data, axis=1)
    return data_filtered

def zscore_normalization(data):
    """
    Apply z-score normalization per channel.
    (doesn't work with fourier transform, only the dc component (0hz) remains in ft)

    Args:
        data (np.ndarray): EEG data, shape (n_channels, n_times)

    Returns:
        data_normalized (np.ndarray): Normalized EEG data.
    """
    mean = np.mean(data, axis=1, keepdims=True)
    std = np.std(data, axis=1, keepdims=True)
    std_safe = np.where(std == 0, 1, std)  # avoid divide by zero
    data_normalized = (data - mean) / std

    return data_normalized

def minmax_normalization(data):
    """
    Apply min-max normalization per channel.

    Args:
        data (np.ndarray): EEG data, shape (n_channels, n_times)

    Returns:
        normalized (np.ndarray)
    """
    min_val = np.min(data, axis=1, keepdims=True)
    max_val = np.max(data, axis=1, keepdims=True)
    range_val = max_val - min_val
    range_safe = np.where(range_val == 0, 1, range_val)  # avoid divide by zero
    normalized = (data - min_val) / range_safe
    return normalized

def mean_centering(data):
    """
    Subtract mean per channel.

    Args:
        data (np.ndarray): EEG data, shape (n_channels, n_times)

    Returns:
        centered (np.ndarray)
    """
    mean = np.mean(data, axis=1, keepdims=True)
    centered = data - mean
    return centered