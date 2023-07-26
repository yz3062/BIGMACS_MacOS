#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:47:21 2023

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

# def age_model_interp(dated_depths, dated_ages, all_depths):
#     f = interpolate.interp1d(dated_depths, dated_ages, fill_value='extrapolate')
#     all_ages = f(all_depths)
#     return all_ages

# def autocorr(x):
#     result = np.correlate(x, x, mode='full')
#     return result[int(result.size/2):]

sns.set(font='Arial',palette='husl',style='ticks',context='talk')

xlim_left = 1750
xlim_right = 1950

# read pacific data
stack_path = '../../R59_d18O_stack/results.mat'
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

# Pacific_path = '../stack.txt'
# Pacific_stack = pd.read_table(Pacific_path, delimiter=' ')
# Pacific_stack = Pacific_stack.groupby('age(kyr)').mean()

# Atlantic data
stack_path = '../../R60_d18O_stack/results.mat'
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

# # Indian data
# stack_path = '../../R14_d18O_stack/results.mat'
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
# df_Indian = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
#                   columns=columns)

# Atlantic_path = '../../R37_d18O_stack/stack.txt'
# Atlantic_stack = pd.read_table(Atlantic_path, delimiter=' ')
# Atlantic_stack = Atlantic_stack.groupby('age(kyr)').mean()

LR04 = LR04_fetching_func.fetch_d18O()

#%% plot
# fig, axes = plt.subplots(2,1, sharex=True)

for i in range(len(df_Pacific['name'])):
    d18O = ma.fix_invalid(df_Pacific.iloc[i]['d18O']).mean(axis=1)
    shift = ma.squeeze(df_Pacific.iloc[i]['d18O_shift'])
    scale = ma.squeeze(df_Pacific.iloc[i]['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(df_Pacific.iloc[i]['median'])
    age = age[~d18O.mask]
    depth = ma.squeeze(df_Pacific.iloc[i]['depth'])
    depth = depth[~d18O.mask]
    d18O = d18O[~d18O.mask]
    if d18O[(age>1800) & (age<1900)].size != 0: 
        output_dict = {'Depth': depth, 'Age': age, 'd18O': d18O}
        output_df = pd.DataFrame(data=output_dict)
        output_df.to_excel('single record spreadsheets/'+df_Pacific.iloc[i]['name'][0]+'.xlsx')
for i in range(len(df_Atlantic['name'])):
    d18O = ma.fix_invalid(df_Atlantic.iloc[i]['d18O']).mean(axis=1)
    shift = ma.squeeze(df_Atlantic.iloc[i]['d18O_shift'])
    scale = ma.squeeze(df_Atlantic.iloc[i]['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(df_Atlantic.iloc[i]['median'])
    age = age[~d18O.mask]
    depth = ma.squeeze(df_Atlantic.iloc[i]['depth'])
    depth = depth[~d18O.mask]
    d18O = d18O[~d18O.mask]
    if d18O[(age>1800) & (age<1900)].size != 0: 
        output_dict = {'Depth': depth, 'Age': age, 'd18O': d18O}
        output_df = pd.DataFrame(data=output_dict)
        output_df.to_excel('single record spreadsheets/'+df_Atlantic.iloc[i]['name'][0]+'.xlsx')
# for i in range(len(df_Indian['name'])):
#     d18O = ma.fix_invalid(df_Indian.iloc[i]['d18O']).mean(axis=1)
#     shift = ma.squeeze(df_Indian.iloc[i]['d18O_shift'])
#     scale = ma.squeeze(df_Indian.iloc[i]['d18O_scale'])
#     d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
#     age = ma.squeeze(df_Indian.iloc[i]['median'])
#     age = age[~d18O.mask]
#     d18O = d18O[~d18O.mask]
#     fig = plt.figure()
#     if d18O[(age>1800) & (age<1900)].size != 0: 
#         plt.plot(age, d18O, '-o', color='C6')
#         plt.plot(LR04.index/1000, LR04, color='k', alpha=0.5)
#         # plt.title(df_Indian.iloc[i]['name'][0])
#         plt.xlim(xlim_left, xlim_right)
#         plt.ylim(d18O[(age>1750) & (age<1950)].min()-0.5,
#                  d18O[(age>1750) & (age<1950)].max()+0.5)
#         plt.gca().invert_yaxis()
#         plt.xlabel('Age (ka BP)')
#         plt.ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
#         plt.gca().axvspan(1800, 1900, alpha=0.5, color='lightgray')
#         # plt.savefig('single record figures/'+df_Indian.iloc[i]['name'][0], dpi=500)
#         plt.tight_layout()
#         plt.savefig('single record figures/'+df_Indian.iloc[i]['name'][0]+'.pdf')
# axes[0].plot(Pacific_stack.index, Pacific_stack['mean(permil)'], color='C4')
# axes[1].plot(Atlantic_stack.index, Atlantic_stack['mean(permil)'], color='C5')
# axes[0].plot(LR04.index/1000, LR04, color='k', alpha=0.5)
# axes[1].plot(LR04.index/1000, LR04, color='k', alpha=0.5)

# fig.set_size_inches(6,4)

# plt.savefig('Raw_d18O_18ma_zoom.png', dpi=700)