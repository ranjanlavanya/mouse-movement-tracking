# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 15:32:29 2025

@author: Lavanya Ranjan
"""

# For calculation of all stationary events (freezing bouts) which are greater than 1s in  the dataset. Also, lists bout duration of each event.
# calculates no of all stattionary events for a csv (which are greater than or equal to 30 frames); and lists the duartion (in seconds) for each event as bout duration

import pandas as pd
import os

def count_stationary_events(input_folder, output_folder):
    # Get all CSV files
    csv_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".csv")]

    if len(csv_files) == 0:
        print("No CSV files found.")
        return

    results = []   # store each CSV result here

    for file in csv_files:
        input_csv_path = os.path.join(input_folder, file)
        print(f"Processing: {file}")

        df = pd.read_csv(input_csv_path)

        # Extract 5th column and normalize
        state_col = df.columns[4]
        states = df[state_col].astype(str).str.strip().str.lower().tolist()

        # Count stationary streaks
        stationary_count = 0
        current_streak = 0
        bout_durations = []  # in frames

        for s in states:
            if s == "stationary":
                current_streak += 1
            else:
                if current_streak >= 30:
                    stationary_count += 1
                    bout_durations.append(current_streak)
                current_streak = 0

        # final streak
        if current_streak >= 30:
            stationary_count += 1
            bout_durations.append(current_streak)

        # Convert bout durations to seconds (divide by 30)
        bout_seconds = [round(b / 30, 3) for b in bout_durations]

        # Prepare row dictionary
        row = {
            "input_csv_name": file,
            "stationary_count": stationary_count
        }

        # Add bout durations as separate columns (bout1_sec, bout2_sec...)
        for i, bout in enumerate(bout_seconds, start=1):
            row[f"bout{i}_sec"] = bout

        results.append(row)

    # Create output folder
    os.makedirs(output_folder, exist_ok=True)

    # Convert results to DataFrame
    out_df = pd.DataFrame(results)

    # Save
    output_csv_path = os.path.join(output_folder, "count.csv")
    out_df.to_csv(output_csv_path, index=False)

    print(f"\nSaved results for {len(csv_files)} files to:")
    print(output_csv_path)


# ---- CALL WITH YOUR PATHS ----
count_stationary_events(
    input_folder="E:\\Lavanya\\experiment\\vids\\final_analysis\\stationary_count",
    output_folder="E:\\Lavanya\\experiment\\vids\\final_analysis\\stationary_count"
)
