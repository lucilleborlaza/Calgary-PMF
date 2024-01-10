# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:46:45 2023
This script is prepared for Marco Eugene. The raw file contains source contributions (7F and 9F).
The objective is to do a site comparison. UPDATED: 1/10/2024
@author: lb945465
"""

import pandas as pd
import geopandas as gpd
import folium
import folium.plugins
from sklearn.preprocessing import MinMaxScaler

# Read Excel file and import necessary libraries
excel_path = r'C:\Users\LB945465\OneDrive - University at Albany - SUNY\State University of New York\Extra\Extra work\Calgary PMF\9-factor solution_VOC spatial_Calgary_v2.xlsx'

def create_heatmap(excel_path, worksheet):
    df = pd.read_excel(excel_path, sheet_name=worksheet)
    factor_columns = df.columns[-9:]

    for factor in factor_columns:
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))
        map_center = [51.0447, -114.0719]
        m = folium.Map(location=map_center, zoom_start=10)
        
        heat_data = [[row['Latitude'], row['Longitude']] for idx, row in gdf.iterrows() if row[factor] > 0]
        folium.plugins.HeatMap(heat_data, name=f'{factor} Heatmap').add_to(m)
        
        file_name = f'heatmap_{worksheet}_{factor}.html'
        m.save(file_name)
        #print(f"Heatmap for {factor} in {worksheet} saved as {file_name}")

create_heatmap(excel_path, worksheet='Sheet1')

def create_circle_marker_map(excel_path, worksheet):
    df = pd.read_excel(excel_path, sheet_name=worksheet)
    factor_columns = df.columns[-9:]

    for factor in factor_columns:
        df_factor = df[df[factor] != 0]
        scaler = MinMaxScaler(feature_range=(2, 20))
        df_factor['Marker_size'] = scaler.fit_transform(df_factor[[factor]].values)

        gdf = gpd.GeoDataFrame(df_factor, geometry=gpd.points_from_xy(df_factor['Longitude'], df_factor['Latitude']))
        map_center = [51.0447, -114.0719]
        m = folium.Map(location=map_center, zoom_start=10)

        for idx, row in gdf.iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=row['Marker_size'],
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                popup=f"{factor}: {row[factor]:.1f} (Site: {row['Site_ID']})",
            ).add_to(m)

        file_name = f'circle_marker_map_{worksheet}_{factor}.html'
        m.save(file_name)
        #print(f"Circle marker map for {factor} in {worksheet} saved as {file_name}")

create_circle_marker_map(excel_path, worksheet='Sheet1')
