#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:22:35 2023

@author: zhou
"""

import pandas as pd
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import seaborn as sns
import GEBCO_fetching_fun

sns.set(font='Arial',palette='husl',style='whitegrid',context='paper')

ylim_top = 5500

# read excel. Remove columns without # cycles
df = pd.read_excel('core_info_18ma_cycles.xlsx', sheet_name='18ma_cycles')
df.dropna(subset=['Num cycles'], inplace=True)
df_Atlantic = df[(df['Longitude'] >= -80) & (df['Longitude'] <= 20)]

# set up transect

# Plot bathyemetry
bathymetry, lats = GEBCO_fetching_fun.fetch_WNA_bathymetry()
bathymetry *= -1
plt.fill_between(lats, ylim_top, bathymetry,color='gray', linewidth=0,
                 zorder=-1)
# axis labels
plt.xlabel('Latitude (°N)')
plt.ylabel('Depth (m)')

# plot data
plt.scatter(df_Atlantic['Latitude'], df_Atlantic['Water Depth'])

# beautification
plt.ylim(top=ylim_top)
plt.gca().invert_yaxis()

plt.savefig('Atlantic_transect_core_location_18ma.png', dpi=500)