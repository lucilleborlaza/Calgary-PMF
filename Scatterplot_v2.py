# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 09:48:06 2024
This script is prepared to create a scatterplot of PMF source contributions in Calgary
and create a geospatial map for visualization.
@author: lb945465
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataframe from the Excel file
data = pd.read_excel(r"C:\Users\LB945465\OneDrive - University at Albany - SUNY\State University of New York\Extra\Extra work\Calgary PMF\9-factor solution_VOC spatial_Calgary_v2.xlsx", 
                                    )

# Convert the 'Date' column to datetime and then back to string
data['Date'] = pd.to_datetime(data['Date'], format='%d%b%Y %H:%M:%S')

# Sort the data first by 'Season' and then by 'Date' within each season
data = data.sort_values(by=['Season', 'Site'])
#data['Date'] = data['Date'].dt.strftime('%d%b%Y %H:%M:%S')

# Convert the 'Site' column to a string
data['Site'] = data['Site'].astype(str)

# Selecting the last nine columns for the factors
factors = data.columns[-9:]

# Separate the data by season
summer_data = data[data['Season'] == 'Summer']
winter_data = data[data['Season'] == 'Winter']

for factor in factors:
    # Create a 1x2 grid of subplots for the current factor
    fig, axes = plt.subplots(2, 1, figsize=(25,10), dpi=100, sharex=True)  # Adjust figsize as needed

    # Plot Summer data in the first subplot
    sns.scatterplot(ax=axes[0], data=summer_data, x='Site', y=factor, hue='Site type', style='Site type', markers=True)
    axes[0].set_title(f"{factor} - Summer", fontweight="bold", fontsize=18)
    axes[0].set_xlabel('')
    axes[0].set_ylabel("Source contribution", fontweight="bold", fontsize=15)
    # Optional: Customize the x-tick labels, e.g., rotation, fontsize
    
    # Plot Winter data in the second subplot
    sns.scatterplot(ax=axes[1], data=winter_data, x='Site', y=factor, hue='Site type', style='Site type', markers=True)
    axes[1].set_title(f"{factor} - Winter", fontweight="bold", fontsize=18)
    axes[1].set_xlabel('Site')
    axes[1].set_ylabel("Source contribution", fontweight="bold", fontsize=15)
    # Optional: Customize the x-tick labels, e.g., rotation, fontsize
    
    # Synchronize y-axes between the two subplots
    max_y = max(axes[0].get_ylim()[1], axes[1].get_ylim()[1])
    axes[0].set_ylim(0, max_y)
    axes[1].set_ylim(0, max_y)

    # Adjust the margins
    axes[0].margins(x=0.01)  # Set a small margin value
    axes[1].margins(x=0.01)
    
    # Hide the legend for the first subplot if you prefer it only on one plot
    #axes[0].legend().set_visible(False)
    
    # Rotate x-axis labels and set a custom rotation
    plt.setp(axes[1].get_xticklabels(), rotation=45, ha="right")

    # Adjust the layout for readability
    plt.tight_layout()

    # Show the plot
    plt.show()
