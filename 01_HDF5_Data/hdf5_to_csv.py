import os
import h5py
import numpy as np
import pandas as pd

# Path to your downloaded HDF5 file
HDF5_PATH = "ecg_tracings.hdf5"
RESULTS_PATH = "results"
os.makedirs(RESULTS_PATH, exist_ok=True)

# Load the HDF5 file
with h5py.File(HDF5_PATH, "r") as f:
    x = np.array(f['tracings'])
    print(f"Loaded data shape: {x.shape}")  # shape (827, 4096, 12)

# Choose the desired N_SAMPLES
# Number of samples to extract (e.g., first 10 ECGs)
N_SAMPLES = 10
samples = x[:N_SAMPLES]  # shape (N_SAMPLES, 4096, 12)

# For each sample, save as CSV
for i in range(N_SAMPLES):
    sample = samples[i]  # shape (4096,12)
    # create a DataFrame: columns lead0, lead1, … lead11
    df = pd.DataFrame(sample, columns=[f"lead_{j + 1}" for j in range(sample.shape[1])])
    # optionally add a time column assuming sampling rate 400Hz
    fs = 400.0
    t = np.arange(sample.shape[0]) / fs
    df.insert(0, "time_s", t)
    # save
    output_file_path = os.path.join(RESULTS_PATH, f"ecg_sample_{i + 1}.csv")
    df.to_csv(output_file_path, index=False)
    print(f"Saved sample {i + 1} to {output_file_path}")
