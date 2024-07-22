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

sns.set(font='Arial',palette='husl',style='ticks',context='talk')

xlim_left = 1750
xlim_right = 1950

# read pacific data
stack_path = '../../R86_d18O_stack/results.mat'
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

# Atlantic data
stack_path = '../../R87_d18O_stack/results.mat'
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

#%% set up file to save
with pd.ExcelWriter('Raw_depth_age_d18O.xlsx') as writer:
    # export
    for i in range(len(df_Pacific['name'])):
        d18O = ma.fix_invalid(df_Pacific.iloc[i]['d18O']).mean(axis=1)
        shift = ma.squeeze(df_Pacific.iloc[i]['d18O_shift'])
        scale = ma.squeeze(df_Pacific.iloc[i]['d18O_scale'])
        # [()]: https://stackoverflow.com/questions/51149865/zero-dimensional-numpy-ndarray-only-element-is-a-2d-array-how-to-access-it
        d18O_shifted_scaled = (d18O - shift[()]) / scale[()] # from BIGMACS saveFigures.m
        age_median = ma.squeeze(df_Pacific.iloc[i]['median'])
        age_median = age_median[~d18O.mask]
        age_mean = ma.squeeze(df_Pacific.iloc[i]['mean'])
        age_mean = age_mean[~d18O.mask]
        age_lower95 = ma.squeeze(df_Pacific.iloc[i]['lower_95'])
        age_lower95 = age_lower95[~d18O.mask]
        age_lower68 = ma.squeeze(df_Pacific.iloc[i]['lower_68'])
        age_lower68 = age_lower68[~d18O.mask]
        age_upper95 = ma.squeeze(df_Pacific.iloc[i]['upper_95'])
        age_upper95 = age_upper95[~d18O.mask]
        age_upper68 = ma.squeeze(df_Pacific.iloc[i]['upper_68'])
        age_upper68 = age_upper68[~d18O.mask]
        depth = ma.squeeze(df_Pacific.iloc[i]['depth'])
        depth = depth[~d18O.mask]
        d18O = d18O[~d18O.mask]
        d18O_shifted_scaled = d18O_shifted_scaled[~d18O_shifted_scaled.mask]
        # if d18O[(age>1800) & (age<1900)].size != 0: 
        if df_Pacific.iloc[i]['name'][0] == 'MV0502_3': # for some reason, this core's data is in rows, not columns like the others
            output_dict = {'Depth (mcd)': depth[0],
                            'Age (median; ka)': age_median[0],
                            'Age (mean; ka)': age_mean[0],
                            'Age (lower 95%; ka)': age_lower95[0],
                            'Age (lower 68%; ka)': age_lower68[0],
                            'Age (upper 95%; ka)': age_upper95[0],
                            'Age (upper 68%; ka)': age_upper68[0],
                            'd18O original (‰)': d18O[0],
                            'd18O shifted and scaled (‰)': d18O_shifted_scaled[0],
                            }
        else:
            output_dict = {'Depth (mcd)': depth,
                            'Age (median; ka)': age_median,
                            'Age (mean; ka)': age_mean,
                            'Age (lower 95%; ka)': age_lower95,
                            'Age (lower 68%; ka)': age_lower68,
                            'Age (upper 95%; ka)': age_upper95,
                            'Age (upper 68%; ka)': age_upper68,
                            'd18O original (‰)': d18O,
                            'd18O shifted and scaled (‰)': d18O_shifted_scaled,}
        output_df = pd.DataFrame(data=output_dict)
        output_df.to_excel(writer, sheet_name=df_Pacific.iloc[i]['name'][0])
    for i in range(len(df_Atlantic['name'])):
        d18O = ma.fix_invalid(df_Atlantic.iloc[i]['d18O']).mean(axis=1)
        shift = ma.squeeze(df_Atlantic.iloc[i]['d18O_shift'])
        scale = ma.squeeze(df_Atlantic.iloc[i]['d18O_scale'])
        d18O_shifted_scaled = (d18O - shift[()]) / scale[()] # from BIGMACS saveFigures.m
        age_median = ma.squeeze(df_Atlantic.iloc[i]['median'])
        age_mean = ma.squeeze(df_Atlantic.iloc[i]['mean'])
        age_lower95 = ma.squeeze(df_Atlantic.iloc[i]['lower_95'])
        age_lower68 = ma.squeeze(df_Atlantic.iloc[i]['lower_68'])
        age_upper95 = ma.squeeze(df_Atlantic.iloc[i]['upper_95'])
        age_upper68 = ma.squeeze(df_Atlantic.iloc[i]['upper_68'])
        depth = ma.squeeze(df_Atlantic.iloc[i]['depth'])
        if d18O.mask.any() == True: # if no mask -> all data is unmasked, then skip masking
            print(df_Atlantic.iloc[i]['name'][0])
            age_median = age_median[~d18O.mask]
            age_mean = age_mean[~d18O.mask]
            age_lower95 = age_lower95[~d18O.mask]
            age_lower68 = age_lower68[~d18O.mask]
            age_upper95 = age_upper95[~d18O.mask]
            age_upper68 = age_upper68[~d18O.mask]
            depth = depth[~d18O.mask]
            d18O = d18O[~d18O.mask]
            d18O_shifted_scaled = d18O_shifted_scaled[~d18O_shifted_scaled.mask]
        # if d18O[(age>1800) & (age<1900)].size != 0: 
        output_dict = {'Depth (mcd)': depth,
                        'Age (median; ka)': age_median,
                        'Age (mean; ka)': age_mean,
                        'Age (lower 95%; ka)': age_lower95,
                        'Age (lower 68%; ka)': age_lower68,
                        'Age (upper 95%; ka)': age_upper95,
                        'Age (upper 68%; ka)': age_upper68,
                        'd18O original (‰)': d18O,
                        'd18O shifted and scaled (‰)': d18O_shifted_scaled,}
        output_df = pd.DataFrame(data=output_dict)
        output_df.to_excel(writer, sheet_name=df_Atlantic.iloc[i]['name'][0])
# for i in range(len(df_Atlantic['name'])):
#     d18O = ma.fix_invalid(df_Atlantic.iloc[i]['d18O']).mean(axis=1)
#     shift = ma.squeeze(df_Atlantic.iloc[i]['d18O_shift'])
#     scale = ma.squeeze(df_Atlantic.iloc[i]['d18O_scale'])
#     d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
#     age = ma.squeeze(df_Atlantic.iloc[i]['median'])
#     age = age[~d18O.mask]
#     depth = ma.squeeze(df_Atlantic.iloc[i]['depth'])
#     depth = depth[~d18O.mask]
#     d18O = d18O[~d18O.mask]
#     if d18O[(age>1800) & (age<1900)].size != 0: 
#         output_dict = {'Depth': depth, 'Age': age, 'd18O': d18O}
#         output_df = pd.DataFrame(data=output_dict)
#         output_df.to_excel('single record spreadsheets/'+df_Atlantic.iloc[i]['name'][0]+'.xlsx')
