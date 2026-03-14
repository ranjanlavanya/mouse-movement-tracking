# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 18:47:02 2025

@author: Lavanya Ranjan
"""
# The code averages frames across an excel to give time in seconds. Basically converts 180000 frames in a csv to 600s, by calculationg one averaged data point for 30 frames.
# Thus, it allows us to visualise velocity as a function of time rather than frames, making it more meaningful.

import os
import pandas as pd
import numpy as np

# Your input folder (contains XLSX files)
input_folder = r"D:\bonsai analysis\codes\time_averaging"

# Output folder (averaged CSV files will be saved here)
output_folder = r"D:\bonsai analysis\codes\time_averaging\OUTPUT"
os.makedirs(output_folder, exist_ok=True)

# Loop through all XLSX files in the input folder
for file in os.listdir(input_folder):
    if file.endswith(".xlsx"):
        file_path = os.path.join(input_folder, file)

        print(f"Processing: {file}")

        # Read Excel file
        df = pd.read_excel(file_path)

        # Make sure file is not empty
        if df.shape[0] == 0:
            print(f"Skipping {file}: empty XLSX.")
            continue

        # Average every 30 rows
        averaged_values = df.groupby(df.index // 30).mean()

        # Output file name (CSV)
        output_file = os.path.join(
            output_folder,
            file.replace(".xlsx", "_time_averaged.csv")
        )

        # Save output as CSV
        averaged_values.to_csv(output_file, index=False)

        print(f"Saved: {output_file}")

print("Finished processing all XLSX files.")
