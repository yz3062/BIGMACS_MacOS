#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:29:15 2023

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

# read data
stack_path = '../../R38_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_1 = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

stack_path = '../../R39_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_2 = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

stack_path = '../../R40_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_3 = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

stack_path = '../../R41_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_4 = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

stack_path = '../../R42_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_5 = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

df = pd.concat([df_1, df_2, df_3, df_4, df_5])

#%% Concat

output_df_global = pd.DataFrame()
for i in range(len(df['name'])):
    d18O = ma.fix_invalid(df.iloc[i]['d18O']).mean(axis=1)
    shift = ma.squeeze(df.iloc[i]['d18O_shift'])
    scale = ma.squeeze(df.iloc[i]['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(df.iloc[i]['median'])
    age = age[~d18O.mask]
    depth = ma.squeeze(df.iloc[i]['depth'])
    depth = depth[~d18O.mask]
    d18O = d18O[~d18O.mask]
    # set up a temp dataframe
    output_dict = {'core': df.iloc[i]['name'][0],
                   'Depth': depth,
                   'Age': age,
                   'd18O': d18O}
    output_df = pd.DataFrame(data=output_dict)
    output_df_global = pd.concat([output_df_global, output_df])
    
#%% export
output_df_global.to_excel('output_for_untuning_global.xlsx')