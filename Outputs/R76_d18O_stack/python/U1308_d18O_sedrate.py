#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 16:57:30 2023

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

def shade(fig,axes,left_x,right_x):
    # the following code will shade HEs
    # 1. Get transformation operators for axis and figure
    top_axtr = axes[0].transData # Axis top -> Display
    bottom_axtr = axes[-1].transData # Axis bottom -> Display
    figtr = fig.transFigure.inverted() # Display -> Figure
    # 2. Transform points from axis to figure coordinates
    shade_lower_limit = axes[-1].viewLim.get_points()[0][1] # lower ylim in lowest axis
    shade_upper_limit = axes[0].viewLim.get_points()[1][1] # upper ylim in highest axis
    lower_left = figtr.transform(bottom_axtr.transform((left_x, shade_lower_limit)))
    lower_right = figtr.transform(bottom_axtr.transform((right_x, shade_lower_limit)))
    upper_left = figtr.transform(top_axtr.transform((left_x, shade_upper_limit)))
    upper_right = figtr.transform(top_axtr.transform((right_x, shade_upper_limit)))
    # 4. Create the patch
    rect = matplotlib.patches.Polygon([lower_left,lower_right,upper_right,upper_left], transform=fig.transFigure,color='lightgray')
    fig.patches.append(rect)

sns.set(font='Myriad Pro',palette='husl',style='ticks',context='paper')

plt.rc('text', usetex=True)

# # read pacific data
# stack_path = '../../R75_d18O_stack/results.mat'
# mat = scipy.io.loadmat(stack_path)

# mdata = mat['summary']  # variable in mat file
# mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
# # * SciPy reads in structures as structured NumPy arrays of dtype object
# # * The size of the array is the size of the structure array, not the number
# #   elements in any particular field. The shape defaults to 2-dimensional.
# # * For convenience make a dictionary of the data using the names from dtypes
# # * Since the structure has only one element, but is 2-D, index it at [0, 0]
# ndata = {n: mdata[n] for n in mdtype.names}
# # Reconstruct the columns of the data table from just the time series
# # Use the number of intervals to test if a field is a column or metadata
# columns = [n for n, v in ndata.items()]
# # now make a data frame, setting the time stamps as the index
# df_Pacific = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
#                   columns=columns)

# Pacific_path = '../../R75_d18O_stack/stack.txt'
# Pacific_stack = pd.read_table(Pacific_path, delimiter=' ')
# Pacific_stack = Pacific_stack.groupby('age(kyr)').mean()

# Atlantic data
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
df_Atlantic = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

Atlantic_path = '../stack.txt'
Atlantic_stack = pd.read_table(Atlantic_path, delimiter=' ')
Atlantic_stack = Atlantic_stack.groupby('age(kyr)').mean()

LR04 = LR04_fetching_func.fetch_d18O()

#%% plot
fig, axes = plt.subplots(2,1,sharex=True)

# get data
d18O = ma.fix_invalid(df_Atlantic[df_Atlantic['name']=='U1308']['d18O'].iloc[0]).mean(axis=1)
shift = ma.squeeze(df_Atlantic[df_Atlantic['name']=='U1308']['d18O_shift'])
scale = ma.squeeze(df_Atlantic[df_Atlantic['name']=='U1308']['d18O_scale'])
d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
age = ma.squeeze(df_Atlantic[df_Atlantic['name']=='U1308']['median'])
age = age[~d18O.mask.transpose()]
depth = ma.squeeze(df_Atlantic[df_Atlantic['name']=='U1308']['depth'])
depth = depth[~d18O.mask.transpose()]
# from m to cm
depth *= 100
d18O = d18O[~d18O.mask]
sed_rate = (depth[1:] - depth[:-1]) / (age[1:] - age[:-1])

# plot d18O
axes[0].plot(age, d18O, 'o-', alpha=1, color='C5',markersize=2)
axes[0].set_ylim(2.7, 4.6)
axes[0].invert_yaxis()

# plot sed rate
axes[1].stairs(sed_rate, age, baseline=None, color='C1')

#%% beautification
plt.subplots_adjust(hspace=-0.15)#, right=0.8)
axes[0].set_xlim(1550, 2100)

sns.despine(ax=axes[0], top=True, bottom=True, left=False, right=True)
sns.despine(ax=axes[1], top=True, bottom=False, left=True, right=False)
axes[0].xaxis.set_ticks_position('none')

# shade
shade(fig,axes,1800, 1900)
for ax in axes:
    ax.set_zorder(10)
    ax.set_facecolor('none')
    
axes[0].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[1].set_ylabel('Sedimentation rate (cm/kyr)')
axes[1].yaxis.set_label_position("right")
axes[1].set_xlabel('Age (ka BP)')

# fig.set_size_inches(6,10)

plt.savefig('U1308_d18O_sedrate.png', dpi=700)
# # plt.savefig('Raw_d18O_alignment_18ma_pan.pdf')