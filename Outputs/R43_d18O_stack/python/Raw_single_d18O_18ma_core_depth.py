#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:32:22 2023

@author: zhou
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.io
import numpy as np
import numpy.ma as ma

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

# read pacific data
stack_path = '../results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_Pacific = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

# Atlantic data
stack_path = '../../R37_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_Atlantic = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

# Indian data
stack_path = '../../R14_d18O_stack/results.mat'
mat = scipy.io.loadmat(stack_path)

mdata = mat['summary']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
ndata = {n: mdata[n] for n in mdtype.names}
columns = [n for n, v in ndata.items()]
# now make a data frame, setting the time stamps as the index
df_Indian = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  columns=columns)

# import core_info.xlsx
xls = pd.ExcelFile('../../../../../Work/Lorraine/Stacking/Stack/Merged/core_info.xlsx')
LR04_df = pd.read_excel(xls, 'LR04 cores')
ProbStack_df = pd.read_excel(xls, 'ProbStack')
thisStudy_df = pd.read_excel(xls, 'This study')
# combine all three sheets
core_info_df = pd.concat([LR04_df, ProbStack_df, thisStudy_df])
core_info_df.set_index('File Name', inplace=True)

#%% plot

for i in range(len(df_Pacific['name'])):
    d18O = ma.fix_invalid(df_Pacific.iloc[i]['d18O']).mean(axis=1)
    shift = ma.squeeze(df_Pacific.iloc[i]['d18O_shift'])
    scale = ma.squeeze(df_Pacific.iloc[i]['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(df_Pacific.iloc[i]['median'])
    age = age[~d18O.mask]
    d18O = d18O[~d18O.mask]
    fig = plt.figure()
    if d18O[(age>1800) & (age<1900)].size != 0: 
        plt.plot(age, d18O, color='C4')
        water_depth = core_info_df.loc[df_Pacific.iloc[i]['name'][0]+'.txt']['Water Depth']
        plt.title(df_Pacific.iloc[i]['name'][0]+', '+str(water_depth)+' m')
        plt.xlim(1500, 2000)
        plt.ylim(2.5, 4.5)
        plt.gca().invert_yaxis()
        plt.xlabel('Age (ka BP)')
        plt.ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
        plt.savefig('single record figures/'+df_Pacific.iloc[i]['name'][0], dpi=500)
for i in range(len(df_Atlantic['name'])):
    d18O = ma.fix_invalid(df_Atlantic.iloc[i]['d18O']).mean(axis=1)
    shift = ma.squeeze(df_Atlantic.iloc[i]['d18O_shift'])
    scale = ma.squeeze(df_Atlantic.iloc[i]['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(df_Atlantic.iloc[i]['median'])
    age = age[~d18O.mask]
    d18O = d18O[~d18O.mask]
    fig = plt.figure()
    if d18O[(age>1800) & (age<1900)].size != 0: 
        plt.plot(age, d18O, color='C5')
        water_depth = core_info_df.loc[df_Atlantic.iloc[i]['name'][0]+'.txt']['Water Depth']
        plt.title(df_Atlantic.iloc[i]['name'][0]+', '+str(water_depth)+' m')
        plt.xlim(1500, 2000)
        plt.ylim(2.5, 4.5)
        plt.gca().invert_yaxis()
        plt.xlabel('Age (ka BP)')
        plt.ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
        plt.savefig('single record figures/'+df_Atlantic.iloc[i]['name'][0], dpi=500)
for i in range(len(df_Indian['name'])):
    d18O = ma.fix_invalid(df_Indian.iloc[i]['d18O']).mean(axis=1)
    shift = ma.squeeze(df_Indian.iloc[i]['d18O_shift'])
    scale = ma.squeeze(df_Indian.iloc[i]['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(df_Indian.iloc[i]['median'])
    age = age[~d18O.mask]
    d18O = d18O[~d18O.mask]
    fig = plt.figure()
    if d18O[(age>1800) & (age<1900)].size != 0: 
        plt.plot(age, d18O, color='C6')
        water_depth = core_info_df.loc[df_Indian.iloc[i]['name'][0]+'.txt']['Water Depth']
        plt.title(df_Indian.iloc[i]['name'][0]+', '+str(water_depth)+' m')
        plt.xlim(1500, 2000)
        plt.ylim(2.5, 4.5)
        plt.gca().invert_yaxis()
        plt.xlabel('Age (ka BP)')
        plt.ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
        plt.savefig('single record figures/'+df_Indian.iloc[i]['name'][0], dpi=500)

# fig.set_size_inches(6,4)
# plt.savefig('Raw_d18O_18ma_zoom.png', dpi=700)