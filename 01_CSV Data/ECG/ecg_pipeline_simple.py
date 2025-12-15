"""
ecg_teaching_script.py  (Simplified Version)

- Loads 3 ECG CSV files:
      ecg_sample_1.csv, ecg_sample_2.csv, ecg_sample_3.csv
- Preprocessing:
      1) Bandpass filter only (0.5–40 Hz)
      2) Z-score normalization
- Visualization:
      - Raw vs processed (2x1 plot)
      - QRS detection + marked peaks
- Heart rate estimation

Run:
    python ecg_teaching_script.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

# ----------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------
FS = 400.0  # sampling frequency in Hz
FILE_PATHS = [
    "data/ecg_sample_1.csv",
    "data/ecg_sample_2.csv",
    "data/ecg_sample_3.csv",
]
LEAD_NAME = "lead_1"
RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def load_ecg_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype="band")
    return b, a


def bandpass_filter(signal, fs, low=0.5, high=40.0, order=4):
    b, a = butter_bandpass(low, high, fs, order)
    return filtfilt(b, a, signal)


def normalize_signal(signal):
    mean = np.mean(signal)
    std = np.std(signal)
    if std == 0:
        return signal - mean
    return (signal - mean) / std


def preprocess_ecg(df, lead_name="lead_1", fs=FS):
    """
    Simplified preprocessing:
        1) Bandpass 0.5–40 Hz
        2) Z-score normalization
    """
    time = df["time_s"].values
    raw = df[lead_name].values

    bandpassed = bandpass_filter(raw, fs, low=0.5, high=40.0)
    normalized = normalize_signal(bandpassed)

    return time, raw, normalized


def detect_qrs(time, ecg, fs=FS):
    """
    Simple R-peak detection using scipy.find_peaks.
    Teaching-focused, not clinical-grade.
    """
    min_rr_sec = 0.3
    distance = int(min_rr_sec * fs)

    height = 0.5 * np.max(ecg)

    peaks, props = find_peaks(ecg, distance=distance, height=height)
    return peaks, time[peaks], props


def plot_raw_vs_processed(time, raw, processed, title):
    fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

    axes[0].plot(time, raw)
    axes[0].set_title(title + " - Raw")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True)

    axes[1].plot(time, processed)
    axes[1].set_title(title + " - Processed (Bandpass 0.5–40 Hz)")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Normalized amplitude")
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


def plot_with_qrs(time, ecg, peaks, title):
    plt.figure(figsize=(12, 4))
    plt.plot(time, ecg)
    plt.plot(time[peaks], ecg[peaks], "o")
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()


def estimate_heart_rate(peak_times):
    if len(peak_times) < 2:
        return np.nan
    rr_intervals = np.diff(peak_times)
    return 60.0 / np.mean(rr_intervals)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    for idx, path in enumerate(FILE_PATHS, start=1):
        print("=" * 60)
        print(f"Loading: {path}")

        df = load_ecg_csv(path)

        # --- preprocess ---
        time, raw, processed = preprocess_ecg(df, lead_name=LEAD_NAME, fs=FS)

        # --- QRS detection ---
        peaks, peak_times, props = detect_qrs(time, processed, fs=FS)

        # --- visualization (optional, can be commented out) ---
        plot_raw_vs_processed(time, raw, processed, f"ECG Sample {idx}")
        plot_with_qrs(time, processed, peaks, f"ECG Sample {idx} - QRS Detection")

        # --- save processed signal ---
        processed_path = os.path.join(RESULTS_DIR, f"ecg_sample_{idx}_processed.csv")
        processed_df = pd.DataFrame({
            "time_s": time,
            "ecg_processed": processed
        })
        processed_df.to_csv(processed_path, index=False)
        print(f"Saved processed signal to: {processed_path}")

        # --- save QRS locations ---
        qrs_path = os.path.join(RESULTS_DIR, f"ecg_sample_{idx}_qrs.csv")
        qrs_df = pd.DataFrame({
            "peak_index": peaks,
            "peak_time_s": peak_times
        })
        qrs_df.to_csv(qrs_path, index=False)
        print(f"Saved QRS peaks to: {qrs_path}")

        # --- heart rate estimate ---
        hr = estimate_heart_rate(peak_times)
        print(f"Estimated HR: {hr:.1f} bpm")

    print("=" * 60)
    print("Processing + saving done.")



if __name__ == "__main__":
    main()
