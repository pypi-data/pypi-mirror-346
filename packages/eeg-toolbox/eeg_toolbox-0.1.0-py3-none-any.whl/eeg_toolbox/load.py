import mne
import numpy as np


def load_edf_data(filepath):
    '''
    Load the raw EDF data from a file path into a Numpy array.

    Args:
        filepath (str): Path to the EDF file.

    Returns:
        data (np.ndarray): The loaded data stored in a numpy array.
        ch_names: List of channel names.
        sfreq: Sampling frequency.
    '''
    raw = mne.io.read_raw_edf(filepath, preload=True, verbose=False)

    data = raw.get_data()
    ch_names = raw.ch_names
    sfreq = raw.info['sfreq']

    return data, ch_names, sfreq

