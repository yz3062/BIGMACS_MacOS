#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 14:32:58 2023

@author: zhou
"""

import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

# read excel. Remove columns without # cycles
df = pd.read_excel('core_info_18ma_cycles.xlsx', sheet_name='18ma_cycles')
df.dropna(subset=['Num cycles'], inplace=True)

# set up map
ax1 = plt.subplot(1,1,1,projection=ccrs.PlateCarree())
ax1.set_global()
ax1.coastlines(resolution='50m')
ax1.gridlines(draw_labels=False)
ax1.add_feature(cfeature.LAND, zorder=2, edgecolor='None')

# plot data
ax1.scatter(df['Longitude'], df['Latitude'], c=df['Num cycles'], alpha=0.5)

plt.savefig('map_18ma_cycles.png', dpi=500)