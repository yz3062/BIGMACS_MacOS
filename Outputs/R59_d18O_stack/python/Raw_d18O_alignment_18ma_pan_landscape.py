#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 16:10:02 2023

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../../Work/Lorraine/LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.io
import numpy as np
import numpy.ma as ma
import matplotlib

from scipy import interpolate

def age_model_interp(dated_depths, dated_ages, all_depths):
    f = interpolate.interp1d(dated_depths, dated_ages, fill_value='extrapolate')
    all_ages = f(all_depths)
    return all_ages

def shade(fig,axes,upper_y,lower_y):
    # the following code will shade HEs
    # 1. Get transformation operators for axis and figure
    top_axtr = axes[0].transData # Axis top -> Display
    bottom_axtr = axes[-1].transData # Axis bottom -> Display
    figtr = fig.transFigure.inverted() # Display -> Figure
    # 2. Transform points from axis to figure coordinates
    shade_left_limit = axes[0].viewLim.get_points()[0][0] # upper ylim in highest axis
    shade_right_limit = axes[-1].viewLim.get_points()[1][0] # lower ylim in lowest axis
    upper_right = figtr.transform(bottom_axtr.transform((shade_right_limit, upper_y)))
    lower_right = figtr.transform(bottom_axtr.transform((shade_right_limit, lower_y)))
    upper_left = figtr.transform(top_axtr.transform((shade_left_limit, upper_y)))
    lower_left = figtr.transform(top_axtr.transform((shade_left_limit, lower_y)))
    # 4. Create the patch
    rect = matplotlib.patches.Polygon([upper_right, lower_right, lower_left, upper_left], transform=fig.transFigure,color='lightgray')
    fig.patches.append(rect)

sns.set(font='Myriad Pro',palette='husl',style='ticks',context='paper')

plt.rc('text', usetex=True)

# read pacific data
stack_path = '../results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
# * SciPy reads in structures as structured NumPy arrays of dtype object
# * The size of the array is the size of the structure array, not the number
#   elements in any particular field. The shape defaults to 2-dimensional.
# * For convenience make a dictionary of the data using the names from dtypes
# * Since the structure has only one element, but is 2-D, index it at [0, 0]
ndata = {n: mdata[n] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
# Use the number of intervals to test if a field is a column or metadata
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_Pacific = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

Pacific_path = '../stack.txt'
Pacific_stack = pd.read_table(Pacific_path, delimiter=' ')
Pacific_stack = Pacific_stack.groupby('age(kyr)').mean()

# Atlantic data
stack_path = '../../R58_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
# * SciPy reads in structures as structured NumPy arrays of dtype object
# * The size of the array is the size of the structure array, not the number
#   elements in any particular field. The shape defaults to 2-dimensional.
# * For convenience make a dictionary of the data using the names from dtypes
# * Since the structure has only one element, but is 2-D, index it at [0, 0]
ndata = {n: mdata[n] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
# Use the number of intervals to test if a field is a column or metadata
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_Atlantic = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

Atlantic_path = '../../R37_d18O_stack/stack.txt'
Atlantic_stack = pd.read_table(Atlantic_path, delimiter=' ')
Atlantic_stack = Atlantic_stack.groupby('age(kyr)').mean()

LR04 = LR04_fetching_func.fetch_d18O()

#%% plot
fig, axes = plt.subplots(1,14, sharey=True)

# list of cores to plot from the Pacific
pacific_core_names = ['ODP1241', '677_LR04age_1', '846_LR04age',
                 '1143_LR04age', '849_LR04age_1',
                 '1123_LR04age']

pacific_core_display_names = ['ODP 1241', r'$\mathrm{\underline{ODP 677}}$', r'$\textbf{ODP 846}$',
                              r'$\textbf{ODP 1143}$', r'$\mathrm{\underline{ODP 849}}$', r'$\textbf{ODP 1123}$']

# axes index iterates through the axis to plot each core
axes_index = 0

for core_name in pacific_core_names:
    d18O = ma.fix_invalid(df_Pacific[df_Pacific['name']==core_name]['d18O'].iloc[0]).mean(axis=1)
    shift = ma.squeeze(df_Pacific[df_Pacific['name']==core_name]['d18O_shift'])
    scale = ma.squeeze(df_Pacific[df_Pacific['name']==core_name]['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(df_Pacific[df_Pacific['name']==core_name]['median'])
    age = age[~d18O.mask.transpose()]
    d18O = d18O[~d18O.mask]
    axes[axes_index].plot(d18O, age, 'o-', alpha=1, color='C4',markersize=2)
    axes[axes_index].plot(LR04, LR04.index/1000, color='k', alpha=0.5)
    axes[axes_index].set_xlim(2.7, 4.6)
    axes[0].set_ylim(1550, 2100)
    axes[axes_index].invert_yaxis()
    axes[axes_index].text(3, 2180,
                          pacific_core_display_names[axes_index],
                          color='C4', rotation=45)
    axes_index += 1
    
# list of cores to plot from the Atlantic
atlantic_core_names = ['U1308', '982_LR04age', 'ODP926',
                       'ODP928', '929_LR04age', '607_LR04age',
                       '659_LR04age', 'ODP1267']

atlantic_core_display_names = ['U1308', r'$\textbf{ODP 982}$', 'ODP 926',
                               r'$\textbf{ODP 928}$', r'$\textbf{ODP 929}$', r'$\textbf{DSDP 607}$',
                               r'$\textbf{ODP 659}$', 'ODP 1267']

for core_name in atlantic_core_names:
    d18O = ma.fix_invalid(df_Atlantic[df_Atlantic['name']==core_name]['d18O'].iloc[0]).mean(axis=1)
    shift = ma.squeeze(df_Atlantic[df_Atlantic['name']==core_name]['d18O_shift'])
    scale = ma.squeeze(df_Atlantic[df_Atlantic['name']==core_name]['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(df_Atlantic[df_Atlantic['name']==core_name]['median'])
    age = age[~d18O.mask.transpose()]
    d18O = d18O[~d18O.mask]
    axes[axes_index].plot(d18O, age, 'o-', alpha=1, color='C5',markersize=2)
    axes[axes_index].plot(LR04, LR04.index/1000, color='k', alpha=0.5)
    axes[axes_index].set_xlim(2.7, 4.6)
    axes[0].set_ylim(1550, 2100)
    axes[axes_index].invert_yaxis()
    axes[axes_index].text(3, 2180,
                          atlantic_core_display_names[axes_index-6],
                          color='C5', rotation=45)
    axes_index += 1

#%% beautification
plt.subplots_adjust(wspace=-0.35)
sns.despine(ax=axes[13], top=False, bottom=True, left=True, right=False)
for i in [0, 2, 4, 6, 8, 10, 12]:
    sns.despine(ax=axes[i], top=True, bottom=False, left=True, right=True)
#    axes[i].yaxis.right()
for i in [1, 3, 5, 7, 9, 11]:
    sns.despine(ax=axes[i], top=False, right=True, bottom=True, left=True)
for i in range(13):
    axes[i].yaxis.set_ticks_position('none')
axes[0].tick_params(labelleft=False)
# axes[0].plot(Pacific_stack.index, Pacific_stack['mean(permil)'], color='C4')
# axes[1].plot(Atlantic_stack.index, Atlantic_stack['mean(permil)'], color='C5')

# shade
shade(fig,axes,1800, 1900)
for ax in axes:
    ax.set_zorder(10)
    ax.set_facecolor('none')
    
# # vertical dashed lines
# for ax in axes:
#     ax.axvline(1719, linestyle='dashed', color='gray', zorder=0)
#     ax.axvline(1736, linestyle='dashed', color='gray', zorder=0)
#     ax.axvline(2025, linestyle='dashed', color='gray', zorder=0)
#     ax.axvline(2055, linestyle='dashed', color='gray', zorder=0)

# axes[0].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
# axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
# axes[13].set_ylabel('Age (ka BP)')

fig.set_size_inches(12,6)

# plt.savefig('Raw_d18O_alignment_18ma_pan.png', dpi=700)
plt.savefig('Raw_d18O_alignment_18ma_pan_landscape.pdf')