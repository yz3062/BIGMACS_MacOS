#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 19:20:02 2023

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

from scipy import interpolate

def age_model_interp(dated_depths, dated_ages, all_depths):
    f = interpolate.interp1d(dated_depths, dated_ages, fill_value='extrapolate')
    all_ages = f(all_depths)
    return all_ages

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

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

Atlantic_path = '../../R58_d18O_stack/stack.txt'
Atlantic_stack = pd.read_table(Atlantic_path, delimiter=' ')
Atlantic_stack = Atlantic_stack.groupby('age(kyr)').mean()

LR04 = LR04_fetching_func.fetch_d18O()

#%% plot
fig, axes = plt.subplots(2,1, sharex=True)

for i in range(len(df_Pacific['name'])):
    d18O = ma.fix_invalid(df_Pacific.iloc[i]['d18O']).mean(axis=1)
    shift = ma.squeeze(df_Pacific.iloc[i]['d18O_shift'])
    scale = ma.squeeze(df_Pacific.iloc[i]['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(df_Pacific.iloc[i]['median'])
    age = age[~d18O.mask]
    d18O = d18O[~d18O.mask]
    # if '849' in df_Pacific.iloc[i]['name'][0]:
    #     axes[0].plot(age, d18O, linestyle='--', alpha=1)
    # elif '677' in df_Pacific.iloc[i]['name'][0]:
    #     axes[0].plot(age, d18O, linestyle='--', alpha=1)
    # elif '1123' in df_Pacific.iloc[i]['name'][0]:
    #     axes[0].plot(age, d18O, linestyle='--', alpha=1)
    # else:
    axes[0].plot(age, d18O, alpha=0.3)
    # print(df_Pacific.iloc[i]['name'][0] + ': ' + np.array2string(d18O[(age>1800) & (age<1825)]))
for i in range(len(df_Atlantic['name'])):
    d18O = ma.fix_invalid(df_Atlantic.iloc[i]['d18O']).mean(axis=1)
    shift = ma.squeeze(df_Atlantic.iloc[i]['d18O_shift'])
    scale = ma.squeeze(df_Atlantic.iloc[i]['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(df_Atlantic.iloc[i]['median'])
    age = age[~d18O.mask]
    d18O = d18O[~d18O.mask]
    axes[1].plot(age, d18O, alpha=0.3)
axes[0].plot(Pacific_stack.index, Pacific_stack['mean(permil)'], color='C4')
axes[1].plot(Atlantic_stack.index, Atlantic_stack['mean(permil)'], color='C5')
axes[0].plot(LR04.index/1000, LR04, color='k', alpha=0.5)
axes[1].plot(LR04.index/1000, LR04, color='k', alpha=0.5)
axes[0].set_xlim(1750, 1950)
axes[0].set_ylim(2.5, 4.5)
axes[1].set_ylim(2.5, 4.5)
axes[0].invert_yaxis()
axes[1].invert_yaxis()

# axes.legend()

axes[0].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[1].set_xlabel('Age (ka BP)')

fig.set_size_inches(6,4)

plt.savefig('Raw_d18O_18ma_zoom.png', dpi=700)