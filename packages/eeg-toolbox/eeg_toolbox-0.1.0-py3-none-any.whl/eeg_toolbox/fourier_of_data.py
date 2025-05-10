import mne
import numpy as np
from numpy.fft import fft, ifft

def data_fourier(data):
    '''
    Calculates the Fourier transform of EEG channels of the data.

    Args:
        data (np.ndarray): The loaded data stored in a numpy array.

    Returns:
        fft_magnitudes (np.ndarray): The Fourier transform of EEG channels of the data separately.
        mean_fft (np.ndarray): The mean of the Fourier transforms.
    '''

    EEG_data = data[:29,:]
    fft_magnitudes = np.abs(fft(EEG_data, axis=1))
    mean_fft = np.mean(fft_magnitudes, axis=0)

    return fft_magnitudes, mean_fft