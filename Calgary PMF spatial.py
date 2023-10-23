# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:46:45 2023
This script is prepared for Marco Eugene. The raw file contains source contributions (7F and 9F).
The objective is to do a site comparison.
@author: lb945465
"""

import pandas as pd
import geopandas as gpd
import folium
import folium.plugins
from sklearn.preprocessing import MinMaxScaler

# Read Excel file and import necessary libraries
excel_path = r'C:\Users\LB945465\OneDrive - University at Albany - SUNY\State University of New York\Extra\Marco Eugene\9F VOC spatial.xlsx'

def create_heatmap(excel_path, worksheet, factor_prefix):
    # Read the Excel file into a DataFrame for the specified worksheet
    df = pd.read_excel(excel_path, sheet_name=worksheet)

    # Calculate Factor_total by summing columns that start with the specified prefix
    factor_columns = [col for col in df.columns if col.startswith(factor_prefix)]
    df['Factor_total'] = df[factor_columns].sum(axis=1)

    # Create a GeoDataFrame using Longitude and Latitude
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))

    # Create a map centered at Calgary (or your desired location)
    map_center = [51.0447, -114.0719]  # Latitude and Longitude of Calgary, AB, Canada (or your desired location)
    m = folium.Map(location=map_center, zoom_start=10)

    # Create HeatMap from the GeoDataFrame
    heat_data = [[row['Latitude'], row['Longitude']] for idx, row in gdf.iterrows()]
    
    # Add HeatMap layer to the map
    folium.plugins.HeatMap(heat_data, name=f'{worksheet} Heatmap').add_to(m)
    
    # Save the map as an HTML file
    file_name = f'heatmap_{worksheet}_{factor_prefix}.html'
    m.save(file_name)
    
    print(f"Heatmap for {worksheet} worksheet with Factor {factor_prefix} saved as {file_name}")

# Example usage:
# Create a heatmap for '7F' worksheet with all columns that start with 'Factor 1'
create_heatmap(excel_path, worksheet='9F', factor_prefix='Factor')

def create_circle_marker_map(excel_path, worksheet, factor_prefix):
    # Read the Excel file into a DataFrame for the specified worksheet
    df = pd.read_excel(excel_path, sheet_name=worksheet)

    # Calculate Factor_total by summing columns that start with the specified prefix
    factor_columns = [col for col in df.columns if col.startswith(factor_prefix)]
    df['Factor_total'] = df[factor_columns].sum(axis=1)

    # Filter rows with non-zero 'Factor_total' values
    df = df[df['Factor_total'] != 0]

    # Normalize 'Factor_total' values to a desired range for marker sizes
    scaler = MinMaxScaler(feature_range=(2, 20))  # Adjust the range as needed
    df['Marker_size'] = scaler.fit_transform(df[['Factor_total']].values)

    # Create a GeoDataFrame using Longitude and Latitude
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))

    # Create a map centered at Calgary (or your desired location)
    map_center = [51.0447, -114.0719]  # Latitude and Longitude of Calgary, AB, Canada (or your desired location)
    m = folium.Map(location=map_center, zoom_start=10)

    # Add circle markers for each site with variable size and 'Site_ID' in the popup
    for idx, row in gdf.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=row['Marker_size'],  # Use 'Marker_size' for marker size
            color='blue',  # Circle marker color
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            popup=f"Factor Total: {row['Factor_total']:.1f} (Site: {row['Site_ID']})",
        ).add_to(m)

    # Save the map as an HTML file
    file_name = f'circle_marker_map_{worksheet}_{factor_prefix}.html'
    m.save(file_name)
    
    print(f"Circle marker map for {worksheet} worksheet with Factor {factor_prefix} saved as {file_name}")

# Example usage:
# Create a circle marker map for '7F' worksheet with all columns that start with 'Factor 1'
create_circle_marker_map(excel_path, worksheet='9F', factor_prefix='Factor')
