#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 00:19:57 2022

@author: zhou
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import seaborn as sns

sns.set(font='Arial',palette='husl',style='ticks')

fig = plt.figure()

ax1 = plt.subplot(1,1,1,projection=ccrs.PlateCarree())
ax1.set_global()
ax1.gridlines(draw_labels=False)
ax1.add_feature(cfeature.LAND)
ax1.add_feature(cfeature.OCEAN)

ax1.scatter(-90.82, -3.1, label='ODP846', transform=ccrs.PlateCarree())
ax1.scatter(-15.87, 57.52, label='ODP982', transform=ccrs.PlateCarree())
ax1.scatter(116.27, 19.45, label='ODP1146', transform=ccrs.PlateCarree())
ax1.scatter(113.28, 9.37, label='ODP1143', transform=ccrs.PlateCarree())
ax1.scatter(-42.9, 3.72, label='ODP926', transform=ccrs.PlateCarree())

ax1.legend(loc=4)

# plt.savefig('map.png', dpi=500)