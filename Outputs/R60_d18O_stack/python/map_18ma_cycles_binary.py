#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 10:45:33 2023

@author: zhou
"""

import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font='Arial',palette='husl',style='whitegrid',context='paper')

# read excel. Remove columns without # cycles
df = pd.read_excel('core_info_18ma_cycles.xlsx', sheet_name='18ma_cycles')
df.dropna(subset=['Num cycles'], inplace=True)
df_1_cycle = df[df['Num cycles'] == 1]
df_2_or_3_cycles = df[df['Num cycles'] > 1]

# set up map
ax1 = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=200))
ax1.set_global()
ax1.coastlines(resolution='50m')
ax1.gridlines(draw_labels=False)
ax1.add_feature(cfeature.LAND, zorder=2, edgecolor='None')

# plot data
ax1.scatter(df_1_cycle['Longitude'],
            df_1_cycle['Latitude'],
            c='C5',
            label='2 cycles',
            transform=ccrs.PlateCarree())
ax1.scatter(df_2_or_3_cycles['Longitude'],
            df_2_or_3_cycles['Latitude'],
            c='C4',
            label='3 or more cycles',
            transform=ccrs.PlateCarree())

# plt.legend()
# plt.savefig('map_18ma_cycles_binary.png', dpi=500)
plt.savefig('map_18ma_cycles_binary.pdf')