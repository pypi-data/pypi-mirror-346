import numpy as np
from scipy.signal import stft, find_peaks

def detect_graphoelements(data, sfreq, bands, duration_sec = 60):
    """
    Using Short-time Fourier transfrom, it examines the 3–8 Hz energy on all channels. If this is abnormal, the event is recorded.

    Args:
        data: EEG signal matrix [channel, time].
        sfreq: Sampling frequency of the EEG data.
        bands:  Describes the frequency bands. Eg.: bands={"delta" : [0, 4], "theta": [4, 8]})
        duration_sec: The number of seconds to process the the signals.

    Returns:
            results: Events returned by the detect_graphoelements function. All elements have this structure:
                {"channel_index": The index of the channel on which the event is occuring.
                "time_sec": The time of the event expressed in secundum.
                "energy_3_8Hz": The energy of the detected event between 3 and 8 Hz.
                "dominant_rhythm": What kind of wave is the detected event e.g. theta, delta etc.
                energy of all the other bands}
    """
    stop_sample = int(duration_sec * sfreq)
    nperseg = int(1.0 * sfreq)
    noverlap = int(0.9 * sfreq)
    results = []
    
    for c_index in range(data.shape[0]):
        eeg = data[c_index, :stop_sample]
        f, t_stft, Zxx = stft(eeg, fs=sfreq, nperseg=nperseg, noverlap=noverlap)
        power = np.abs(Zxx)
        low_band_energy = np.sum(power[(f >= 3) & (f <= 8), :], axis = 0)
        threshold = np.percentile(low_band_energy, 95)
        peaks, _ = find_peaks(low_band_energy, height=threshold)
        
        for peak_id in peaks:
            window_power = power[:, peak_id]
            band_energies = {
                band: np.sum(window_power[(f >= fmin) & (f < fmax)])
                for band, (fmin, fmax) in bands.items()
            }
            dominant = max(band_energies, key=band_energies.get)
            results.append({
                "channel_index": c_index,
                "time_sec": t_stft[peak_id],
                "energy_3_8Hz": low_band_energy[peak_id],
                "dominant_rhythm": dominant,
                **band_energies
                })
    return results