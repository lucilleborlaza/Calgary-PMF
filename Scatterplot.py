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
data = pd.read_excel(r"C:\Users\LB945465\OneDrive - University at Albany - SUNY\State University of New York\Extra\Extra work\Calgary PMF\Copy of 9-factor solution_VOC spatial_Calgary.xlsx", 
                                    )

# Convert the 'Date' column to datetime and then back to string
data['Date'] = pd.to_datetime(data['Date'], format='%d%b%Y %H:%M:%S')

# Sort the data by the 'Date' column
data = data.sort_values(by='Date')
data['Date'] = data['Date'].dt.strftime('%d%b%Y %H:%M:%S')

# Convert the 'Site' column to a string
data['Site'] = data['Site'].astype(str)

# Selecting the last nine columns for the factors
factors = data.columns[-9:]

# Creating a 5x2 subplot
fig, axes = plt.subplots(5, 2, figsize=(30, 20), dpi=200)
axes = axes.flatten()

# Plot each factor in a subplot with 'Site' on the x-axis and markers only, except for the last subplot
for i, factor in enumerate(factors):
    sns.scatterplot(ax=axes[i], data=data, x='Site', y=factor, hue='Site type', style='Site type', markers=True)
    axes[i].set_title(factor)
    axes[i].set_xlabel('')
    if i < len(factors) - 2:  # Hide x-tick labels for all but the bottom row
        axes[i].set_xticklabels([])
    else:  # Only the bottom row subplots will show the x-tick labels
        plt.setp(axes[i].get_xticklabels(), rotation=45, fontsize='x-small')

# Leave the last subplot (10th subplot) empty
axes[-1].axis('off')

# Adjust layout for readability
plt.tight_layout()

# Show the plot
plt.show()

