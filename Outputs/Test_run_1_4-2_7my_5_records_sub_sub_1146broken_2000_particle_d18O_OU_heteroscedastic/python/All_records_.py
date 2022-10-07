#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 01:57:43 2022

@author: zhou
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import seaborn as sns
import sys
sys.path.append("../../../../LR04/python")
import LR04_fetching_func
import matplotlib.ticker as ticker

from scipy import interpolate

def age_model_interp(dated_depths, dated_ages, all_depths):
    f = interpolate.interp1d(dated_depths, dated_ages, fill_value='extrapolate')
    all_ages = f(all_depths)
    return all_ages

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

#%% data input
# 846
ODP846_aligned_file_path = '../ages/ODP846.txt'
ODP846_aligned = pd.read_table(ODP846_aligned_file_path, delimiter=' ',)
ODP846_aligned.set_index('depth(m)',inplace=True)

ODP846_original_file_path = '../../../../Stacking/Stack/LR04/846_LR04age.txt'
ODP846_original = pd.read_table(ODP846_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

LR04 = LR04_fetching_func.fetch_d18O()

ODP846_aligned_d18O = age_model_interp(ODP846_original['Depth (mcd)'], ODP846_original['d18O'], ODP846_aligned.index)

# 1146b
ODP1146b_aligned_file_path = '../ages/ODP1146b.txt'
ODP1146b_aligned = pd.read_table(ODP1146b_aligned_file_path, delimiter='\t')
ODP1146b_aligned.set_index('depth(m)',inplace=True)

ODP1146b_original_file_path = '../../../../Stacking/Stack/NewRecords/ODP1146.txt'
ODP1146b_original = pd.read_table(ODP1146b_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

ODP1146b_aligned_d18O = age_model_interp(ODP1146b_original['Depth (mcd)'], ODP1146b_original['d18O'], ODP1146b_aligned.index)

# 926
ODP926_aligned_file_path = '../ages/ODP926.txt'
ODP926_aligned = pd.read_table(ODP926_aligned_file_path, delimiter=' ',)
ODP926_aligned.set_index('depth(m)',inplace=True)

ODP926_original_file_path = '../../../../Stacking/Stack/NewRecords/ODP926.txt'
ODP926_original = pd.read_table(ODP926_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

ODP926_aligned_d18O = age_model_interp(ODP926_original['Depth (mcd)'], ODP926_original['d18O'], ODP926_aligned.index)

# 1143
ODP1143_aligned_file_path = '../ages/ODP1143.txt'
ODP1143_aligned = pd.read_table(ODP1143_aligned_file_path, delimiter='\t',)
ODP1143_aligned.set_index('depth(m)',inplace=True)

ODP1143_original_file_path = '../../../../Stacking/Stack/LR04/1143_LR04age.txt'
ODP1143_original = pd.read_table(ODP1143_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

ODP1143_aligned_d18O = age_model_interp(ODP1143_original['Depth (mcd)'], ODP1143_original['d18O'], ODP1143_aligned.index)

#982
ODP982_aligned_file_path = '../ages/ODP982.txt'
ODP982_aligned = pd.read_table(ODP982_aligned_file_path, delimiter='\t',)
ODP982_aligned.set_index('depth(m)',inplace=True)

ODP982_original_file_path = '../../../../Stacking/Stack/LR04/982_LR04age.txt'
ODP982_original = pd.read_table(ODP982_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

ODP982_aligned_d18O = age_model_interp(ODP982_original['Depth (mcd)'], ODP982_original['d18O'], ODP982_aligned.index)

# 1146a
ODP1146a_aligned_file_path = '../ages/ODP1146a.txt'
ODP1146a_aligned = pd.read_table(ODP1146a_aligned_file_path, delimiter='\t',)
ODP1146a_aligned.set_index('depth(m)',inplace=True)

ODP1146a_original_file_path = '../../../../Stacking/Stack/NewRecords/ODP1146.txt'
ODP1146a_original = pd.read_table(ODP1146a_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

ODP1146a_aligned_d18O = age_model_interp(ODP1146a_original['Depth (mcd)'], ODP1146a_original['d18O'], ODP1146a_aligned.index)

#%% plot
fig, axes = plt.subplots(5, 1, sharex=True)
plt.subplots_adjust(left=0.15, right=0.8, hspace=-0.2)
axes[0].plot(ODP846_aligned['median(kyr)'], ODP846_aligned_d18O,label='ODP846')
axes[0].plot(LR04.index/1000, LR04, color='k', label='LR04')
axes[0].legend(loc=1)

axes[1].plot(ODP1146a_aligned['median(kyr)'], ODP1146a_aligned_d18O,label='ODP1146')
axes[1].plot(ODP1146b_aligned['median(kyr)'], ODP1146b_aligned_d18O)
axes[1].plot(LR04.index/1000, LR04, color='k')
axes[1].legend(loc=1)

axes[2].plot(ODP1143_aligned['median(kyr)'], ODP1143_aligned_d18O,label='ODP1143')
axes[2].plot(LR04.index/1000, LR04, color='k')
axes[2].legend(loc=1)

axes[3].plot(ODP982_aligned['median(kyr)'], ODP982_aligned_d18O,label='ODP982')
axes[3].plot(LR04.index/1000, LR04, color='k')
axes[3].legend(loc=1)

axes[4].plot(ODP926_aligned['median(kyr)'], ODP926_aligned_d18O,label='ODP926')
axes[4].plot(LR04.index/1000, LR04, color='k')
axes[4].legend(loc=1)

axes[0].set_xlim((ODP846_aligned['median(kyr)'].min(),ODP846_aligned['median(kyr)'].max()))

for i in range(5):
    axes[i].invert_yaxis()
    axes[i].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}\mathrm{O}_\mathrm{benthic}$ (‰)')
    axes[i].set_ylim(bottom=4.5)
for i in range(4):
    axes[i].xaxis.set_ticks_position('none')

for i in [0, 2, 4]:
    axes[i].yaxis.set_label_position("right")

axes[4].set_xlabel('Age (Ma BP)')

#%% beautify
sns.despine(ax=axes[0], top=True, bottom=True, left=True, right=False)
sns.despine(ax=axes[1], top=True, bottom=True, left=False, right=True)
sns.despine(ax=axes[2], top=True, bottom=True, left=True, right=False)
sns.despine(ax=axes[3], top=True, bottom=True, left=False, right=True)
sns.despine(ax=axes[4], top=True, bottom=False, left=True, right=False)

axes[0].axvspan(1700, 1900, color='gray', zorder=-1, alpha=0.3)
axes[1].axvspan(1900, 2100, color='gray', zorder=-1, alpha=0.3)
axes[3].axvspan(1400, 1900, color='gray', zorder=-1, alpha=0.3)
axes[3].axvspan(2000, 2600, color='gray', zorder=-1, alpha=0.3)
axes[4].axvspan(1600, 1900, color='gray', zorder=-1, alpha=0.3)

scale_x = 1e3
ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
axes[4].xaxis.set_major_formatter(ticks_x)

for ax in axes:
    ax.set_zorder(10)
    ax.set_facecolor('none')
    
fig.set_size_inches(8, 9)
plt.savefig('All_records.png', dpi=1000)