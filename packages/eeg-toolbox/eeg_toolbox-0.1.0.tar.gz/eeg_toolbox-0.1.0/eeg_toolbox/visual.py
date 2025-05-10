import mne
import matplotlib.pyplot as plt
import numpy as np

def plot_eeg_overview(data, ch_names, sfreq, n_channels=5, offset=100):
    """
    Plots the first n EEG channels with an offset on the time axis.

    Args:
        data: The EEG data in a numpy array format.
        ch_names: List containing the names of the EEG channels.
        sfreq: Sampling frequency of the EEG data.
        n_channels: The first n channels of the EEG data that appears on the plots. (Default: 5)
        offset: Customize the offset of the data on the plot. (Default: 100)

    """
    times = np.arange(data.shape[1]) / sfreq
    data_scaled = data * 1e6
    plt.figure(figsize=(14, 6))
    for i in range(min(n_channels, data.shape[0])):
        plt.plot(times, data_scaled[i] + i * offset, label = ch_names[i])
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude + Offset (µV)")
    plt.title("EEG Channels Overview")
    plt.legend(loc = "upper right")
    plt.tight_layout()
    plt.show()

def plot_fft_spectrum(mean_fft, sfreq, n_samples):
    """
    Displays the average frequency spectrum of the EEG data (Fourier transform).
    Requires the returned data from data_fourier() function.

    Args:
        mean_fft: The fourier transformed EEG data (returned from data_fourier() function).
        sfreq: Sampling frequency of the EEG data.
        n_samples: The number of data points in the EEG data.

    """
    freqs = np.fft.fftfreq(n_samples, 1 / sfreq)
    plt.figure(figsize=(10, 4))
    plt.plot(freqs[:len(freqs)//2], mean_fft[:len(freqs)//2])
    plt.title("Mean FFT Magnitude Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_graph_segments(data, sfreq, events, ch_names, window_sec=1.5, n_show=5):
    """
        Plots the EEG bands detected in the data with a custom size window around the detected events. Requires the returned data from detect_graphoelements() function.

        Args:
            data: A two dimensional array with the shape (n_channels, n_samples). n_channels: how many EEG channels; n_samples: how many samples are on each channel (length in time)
            sfreq: Sampling frequency of the EEG data.
            events: Events returned by the detect_graphoelements function. All elements have this structure:
                {"channel_index": The index of the channel on which the event is occuring.
                "time_sec": The time of the event expressed in secundum.
                "energy_3_8Hz": The energy of the detected event between 3 and 8 Hz.
                "dominant_rhythm": What kind of wave is the detected event e.g. theta, delta etc.
                energy of all the other bands}
            ch_names: A list containing the names of the EEG channels. Returned from load_edf_data().
            window_sec: The plot visualizes a +- window_sec second window around the detected events. Default: 1.5
            n_show: How many detected events to draw from the events list.


    """
    window_samples = int(window_sec * sfreq)
    plt.figure(figsize=(14, n_show * 3))
    for i, event in enumerate(events[:n_show]):
        ch_id = event["channel_index"]
        t0 = int(event["time_sec"] * sfreq)
        start = max(0, t0 - window_samples)
        stop = min(t0 + window_samples, data.shape[1])
        segment = data[ch_id, start:stop]
        seg_times = np.linspace(-window_sec, window_sec, segment.shape[0])
        plt.subplot(n_show, 1, i + 1)
        plt.plot(seg_times, segment * 1e6, label=f"{ch_names[ch_id]} @ {event['time_sec']:.2f}s")
        plt.axvline(0, color='red', linestyle='--', label='Detected Event')
        plt.title(f"{ch_names[ch_id]} | Detected: {event['dominant_rhythm'].upper()} rythm")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude (µV)")
        plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()