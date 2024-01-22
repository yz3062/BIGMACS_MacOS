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

# read pacific data
stack_path = '../../R59_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_Pacific_1 = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

stack_path = '../../R44_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_Pacific_2 = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

df_Pacific = pd.concat([df_Pacific_1, df_Pacific_2])

# Atlantic data
stack_path = '../../R60_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_Atlantic_1 = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

stack_path = '../../R45_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_Atlantic_2 = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

df_Atlantic = pd.concat([df_Atlantic_1, df_Atlantic_2])

#%% Concat

output_df_Pacific = pd.DataFrame()
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
    # set up a temp dataframe
    output_dict = {'core': df_Pacific.iloc[i]['name'][0],
                   'Depth': depth,
                   'Age': age,
                   'd18O': d18O}
    output_df = pd.DataFrame(data=output_dict)
    output_df_Pacific = pd.concat([output_df_Pacific, output_df])

output_df_Atlantic = pd.DataFrame()
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
    # set up a temp dataframe
    output_dict = {'core': df_Atlantic.iloc[i]['name'][0],
                   'Depth': depth,
                   'Age': age,
                   'd18O': d18O}
    output_df = pd.DataFrame(data=output_dict)
    output_df_Atlantic = pd.concat([output_df_Atlantic, output_df])
    
#%% export
output_df_Pacific.to_excel('output_for_untuning_Pacific.xlsx')
output_df_Atlantic.to_excel('output_for_untuning_Atlantic.xlsx')