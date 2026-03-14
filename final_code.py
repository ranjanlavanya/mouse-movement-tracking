# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 14:40:35 2024

@author: Lavanya Ranjan (with expert advice: Arpan)
"""
# This code takes in a folder which has multiple csv files. It then loops over all the files in the folder to do:
# It takes in a csv file which has x,y coordinates for a point (bonsai analysed). It calculates
# velocity between consecutive x-y coordinates based on Euclidean distance (assuming equal time 
# between two consecutive frames. It compares displacement between frames). Then it plots that velocity against the frames and creates a trajectory plot
# for each file. It also saves all of the plots and the velocities in a csv file. Further, it also creates a csv with
# the total no of frames for staionary and mobile frames. You can thank me later :)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set the directory containing the CSV files
input_folder = "E:/Lavanya/experiment/vids"
output_folder = "E:/Lavanya/experiment/vids/final_analysis"  # Folder to save plots and CSVs

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Initialize a list to store the total number of frames for stationary and moving state for each file
summary_data = []

# Loop over each CSV file in the specified folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        print(f"Processing file: {filename}")

        # Load the data and extract X, Y coordinates
        data = pd.read_csv(file_path).iloc[:, [0, 1]]
        data.columns = ['X', 'Y']

        # Calculate velocity using Euclidean distance between consecutive points
        velocities = np.sqrt(np.diff(data['X'])**2 + np.diff(data['Y'])**2) #np.diff gives a[i+1]-a[i]. Note that it will always be positive, it is the net 'distance' covered in unit time.

        # Set a threshold for classifying stationary vs moving
        threshold = 2.5
        # Adjust based on your data - the freezing clips
        
        states = np.where(velocities < threshold, 'Stationary', 'Moving')

        # Create a DataFrame with all necessary data
        tracking_data = pd.DataFrame({
            'X': data['X'][1:].values,  # Exclude the first point (no velocity for it)
            'Y': data['Y'][1:].values,
            'Velocity': velocities,
            'State': states
        })

        # Plotting the velocity and state over time
        plt.figure(figsize=(10, 5), dpi=600)

        plt.subplot(2, 1, 1)
        plt.plot(tracking_data['Velocity'], label='Velocity')
        plt.axhline(threshold, color='r', linestyle='--', label='Threshold')
        plt.ylabel('Velocity')
        plt.legend()
        plt.savefig(f"{output_folder}/{filename}_velocity_plot.png")  # Save the velocity plot

        plt.subplot(2, 1, 2)
        plt.scatter(tracking_data.index, tracking_data['State'].eq('Moving').astype(int), 
                    label='State (1=Moving, 0=Stationary)', s=0.5)
        plt.ylabel('State')
        plt.xlabel('Time Step')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{output_folder}/{filename}_velocity_state_plot.png")  # Save the state plot
        plt.close()

        # Segregate into two columns: 'Stationary' and 'Moving'
        tracking_data['Stationary'] = tracking_data['State'].eq('Stationary').astype(int)
        tracking_data['Moving'] = tracking_data['State'].eq('Moving').astype(int)

        # Calculate the total number of time steps for each state
        stationary_count = tracking_data['Stationary'].sum()
        moving_count = tracking_data['Moving'].sum()

        print(f'Total Stationary Time Steps: {stationary_count}')
        print(f'Total Moving Time Steps: {moving_count}')
        print(f'Proportion of total time spent stationary: {stationary_count/(stationary_count+moving_count)}')
        
        # Append the counts to the summary data
        summary_data.append({
            'Filename': filename,
            'Total_Number_of_Stationary_Frames': stationary_count,
            'Total_Number_of_Mobile_Frames': moving_count,
            'Proportion of total time spent stationary': stationary_count/(stationary_count+moving_count)
            })

        # Save the velocity and state data with frame index to a CSV
        output_file = f"{output_folder}/{filename}_velocity_with_state.csv"
        tracking_data[['X', 'Y', 'Velocity', 'State']].to_csv(output_file, index_label='Frame')

        print(f"Data saved to {output_file}")

        # Plot the object's trajectory on the 2D plane
        plt.figure(figsize=(10, 8), dpi=600)
        plt.plot(data['X'], data['Y'], color='gray', linestyle='-', linewidth=0.6, label='Trajectory')

        # Mark stationary and moving points with different colors
        plt.scatter(tracking_data[tracking_data['State'] == 'Stationary']['X'],
                    tracking_data[tracking_data['State'] == 'Stationary']['Y'], 
                    color='dodgerblue', label='Stationary', s=15)

        # have disabled this segment by making alpha 0.0; otherwise it also plots small circles for moving state
        plt.scatter(tracking_data[tracking_data['State'] == 'Moving']['X'],
                    tracking_data[tracking_data['State'] == 'Moving']['Y'], 
                    color='red',alpha = 0.0, label='Moving', s=10)

        # Highlight the start and end points
        plt.scatter(data.iloc[0]['X'], data.iloc[0]['Y'], color='tomato', s=100, marker='o', label='Start')
        plt.scatter(data.iloc[-1]['X'], data.iloc[-1]['Y'], color='black', s=100, marker='X', label='End')

        # Set equal scaling for X and Y axes
        plt.axis('equal')  # Ensures 1:1 aspect ratio

        # Configure plot appearance
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Object Trajectory on 2D Plane')
        plt.legend()
        plt.grid(False) #change it to True for the grid

        # Save the trajectory plot
        plt.savefig(f"{output_folder}/{filename}_trajectory_plot.png")
        plt.close()
        
        print(f"Plots saved for {filename}\n")

# Save the summary data to a final CSV file
summary_df = pd.DataFrame(summary_data)
summary_output_file = f"{output_folder}/summary_stationary_moving_times.csv"
summary_df.to_csv(summary_output_file, index=False)
#os.rename(output_folder, c(str(output_file)
print(f"Summary data saved to {summary_output_file}")
print("Processing complete for all files.")

