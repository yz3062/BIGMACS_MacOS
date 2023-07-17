#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 13:09:39 2023

@author: zhou
"""

import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font='Arial',palette='husl',style='whitegrid',context='talk')

# set up map
ax1 = plt.subplot(1,1,1,projection=ccrs.PlateCarree())
# ax1.set_global()
ax1.set_extent([-100, 10, -30, 60])
ax1.coastlines(resolution='50m')
ax1.gridlines(draw_labels=False)
ax1.add_feature(cfeature.LAND, zorder=2, edgecolor='None')

# plot data
ax1.scatter(-32.2313,
            41.0012,
            c='r',
            label='607')
ax1.scatter(-44.4805,
            5.46267,
            c='y',
            label='927')
ax1.scatter(-78.74,
            12.74333333,
            c='g',
            label='999')

plt.legend()
plt.savefig('map_18ma_Atlantic_heavy_d18O.png', dpi=500)