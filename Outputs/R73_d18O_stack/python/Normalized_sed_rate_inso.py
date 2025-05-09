#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 15:30:43 2023

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../../Work/Lorraine/LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import seaborn as sns
# import pyleoclim as pyleo
import matplotlib
import scipy.io
import numpy as np
import numpy.ma as ma

from scipy import interpolate

def age_model_interp(dated_depths, dated_ages, all_depths):
    f = interpolate.interp1d(dated_depths, dated_ages, fill_value='extrapolate')
    all_ages = f(all_depths)
    return all_ages

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

def shade(fig,axes,left_x,right_x, color='lightgray'):
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
    rect = matplotlib.patches.Polygon([lower_left,lower_right,upper_right,upper_left], transform=fig.transFigure,color=color)
    fig.patches.append(rect)

# read pacific data
stack_path = '../../R73_d18O_stack/results.mat'
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

Pacific_path = '../../R73_d18O_stack/stack.txt'
Pacific_stack = pd.read_table(Pacific_path, delimiter=' ')
Pacific_stack = Pacific_stack.groupby('age(kyr)').mean()

# Atlantic data
stack_path = '../../R72_d18O_stack/results.mat'
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

Atlantic_path = '../../R72_d18O_stack/stack.txt'
Atlantic_stack = pd.read_table(Atlantic_path, delimiter=' ')
Atlantic_stack = Atlantic_stack.groupby('age(kyr)').mean()


LR04 = LR04_fetching_func.fetch_d18O()

#%% figure set up
fig, axes = plt.subplots(5,1, sharex=True)
plt.subplots_adjust(hspace=-0.2)

#%% NH inso
inso_summer_65N = pd.read_table('../../../../../Work/McManus/Milankovitch/python/inso_summer_65N.txt',
                                delimiter=' ',
                                names=['age', 'NH inso.'])
inso_summer_65N.set_index('age', inplace=True)

inso_summer_65N.plot(label='65° N insolation', ax=axes[1], color='C5')
axes[1].set_ylabel(r'Insolation $W/{m^2}$')
axes[1].yaxis.set_label_position("right")
axes[1].yaxis.label.set_color('C5')
axes[1].spines['right'].set_color('C5')
axes[1].tick_params(axis='y', colors='C5')
axes[1].legend(loc='upper right', bbox_to_anchor=(1, 1.2))

#%% SH inso
inso_summer_65S = pd.read_table('../../../../../Work/McManus/Milankovitch/python/inso_summer_65S.txt',
                                delimiter=' ',
                                names=['age', 'SH inso.'])
inso_summer_65S.set_index('age', inplace=True)

inso_summer_65S.plot(label='SH inso.', ax=axes[3], color='C4')
axes[3].set_ylabel(r'Insolation $W/{m^2}$')
axes[3].yaxis.set_label_position("right")
axes[3].yaxis.label.set_color('C4')
axes[3].spines['right'].set_color('C4')
axes[3].tick_params(axis='y', colors='C4')
axes[3].legend(loc='lower right', bbox_to_anchor=(1, -0.2))

# #%% NH prec
# inso_summer_65N = pd.read_table('../../../../../Work/McManus/Milankovitch/python/inso_summer_65N.txt',
#                                 delimiter=' ',
#                                 names=['age', 'inso'])
# inso_summer_65N.set_index('age', inplace=True)
# inso_ts = pyleo.Series(time=inso_summer_65N.index, value=inso_summer_65N['inso'],
#                        time_name='Age',
#                        time_unit='kyr BP',
#                        value_name='65° N insolation',
#                        value_unit=r'$W/{m^2}$')

# ts_band = inso_ts.filter(method='butterworth',cutoff_scale=[17,25])
# ts_band.plot(label='NH precession bandpass', ax=axes[1], color='C5')
# axes[1].yaxis.set_label_position("right")
# axes[1].yaxis.label.set_color('C5')
# axes[1].spines['right'].set_color('C5')
# axes[1].tick_params(axis='y', colors='C5')
# axes[1].legend(loc='upper right', bbox_to_anchor=(1, 1.2))

# #%% SH prec
# inso_summer_65S = pd.read_table('../../../../../Work/McManus/Milankovitch/python/inso_summer_65S.txt',
#                                 delimiter=' ',
#                                 names=['age', 'inso'])
# inso_summer_65S.set_index('age', inplace=True)
# inso_ts = pyleo.Series(time=inso_summer_65S.index, value=inso_summer_65S['inso'],
#                        time_name='Age',
#                        time_unit='kyr BP',
#                        value_name='65° S insolation',
#                        value_unit=r'$W/{m^2}$')

# ts_band = inso_ts.filter(method='butterworth',cutoff_scale=[17,25])
# ts_band.plot(label='SH precession bandpass', ax=axes[3], color='C4')
# axes[3].yaxis.set_label_position("right")
# axes[3].yaxis.label.set_color('C4')
# axes[3].spines['right'].set_color('C4')
# axes[3].tick_params(axis='y', colors='C4')
# axes[3].legend(loc='lower right', bbox_to_anchor=(1, -0.2))

#%% obliquity
obl = pd.read_excel('../../../../../Work/McManus/Milankovitch/Insolation calculation_LR04.xlsx',
                    sheet_name='Sheet1')
obl.set_index('time', inplace=True)
axes[0].plot(obl.index, obl['obliquity'], color='k')
axes[0].set_ylabel('Obliquity (°)')
axes[4].plot(obl.index, obl['obliquity'], color='k')
axes[4].set_ylabel('Obliquity (°)')

#%% calculate sed rate
Pacific_sed_rate_normalized_interpolated_Series_sum = pd.Series(dtype=float)

for index, row in df_Pacific.iterrows():
    d18O = ma.fix_invalid(row['d18O']).mean(axis=1)
    shift = ma.squeeze(row['d18O_shift'])
    scale = ma.squeeze(row['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(row['median'])
    age = age[~d18O.mask.transpose()]
    depth = ma.squeeze(row['depth'])
    depth = depth[~d18O.mask.transpose()]
    d18O = d18O[~d18O.mask] # this line must be behind other lines using d18O.mask
    # from m to cm
    depth *= 100
    sed_rate = (depth[1:] - depth[:-1]) / (age[1:] - age[:-1])
    sed_rate_normalized = sed_rate / sed_rate.mean()
    sed_rate_normalized_interpolated = age_model_interp((age[1:]+age[:-1])/2, sed_rate_normalized, np.arange(int(age[0]), int(age[-1])))
    sed_rate_normalized_interpolated_Series = pd.Series(data=sed_rate_normalized_interpolated, index=np.arange(int(age[0]), int(age[-1])))
    Pacific_sed_rate_normalized_interpolated_Series_sum = pd.concat([Pacific_sed_rate_normalized_interpolated_Series_sum,
                                                                    sed_rate_normalized_interpolated_Series])
Pacific_sed_rate_normalized_interpolated_Series_mean = Pacific_sed_rate_normalized_interpolated_Series_sum.groupby(level=0).mean()

Atlantic_sed_rate_normalized_interpolated_Series_sum = pd.Series(dtype=float)

for index, row in df_Atlantic.iterrows():
    d18O = ma.fix_invalid(row['d18O']).mean(axis=1)
    shift = ma.squeeze(row['d18O_shift'])
    scale = ma.squeeze(row['d18O_scale'])
    d18O = (d18O - shift) / scale # from BIGMACS saveFigures.m
    age = ma.squeeze(row['median'])
    age = age[~d18O.mask.transpose()]
    depth = ma.squeeze(row['depth'])
    depth = depth[~d18O.mask.transpose()]
    d18O = d18O[~d18O.mask] # this line must be behind other lines using d18O.mask
    # from m to cm
    depth *= 100
    sed_rate = (depth[1:] - depth[:-1]) / (age[1:] - age[:-1])
    sed_rate_normalized = sed_rate / sed_rate.mean()
    sed_rate_normalized_interpolated = age_model_interp((age[1:]+age[:-1])/2, sed_rate_normalized, np.arange(int(age[0]), int(age[-1])))
    sed_rate_normalized_interpolated_Series = pd.Series(data=sed_rate_normalized_interpolated, index=np.arange(int(age[0]), int(age[-1])))
    # ############# TEST ###############
    # plt.figure()
    # plt.plot(sed_rate_normalized_interpolated_Series.index,
    #          sed_rate_normalized_interpolated_Series)
    # plt.title(row['name'][0])
    # ##################################
    Atlantic_sed_rate_normalized_interpolated_Series_sum = pd.concat([Atlantic_sed_rate_normalized_interpolated_Series_sum,
                                                                    sed_rate_normalized_interpolated_Series])
Atlantic_sed_rate_normalized_interpolated_Series_mean = Atlantic_sed_rate_normalized_interpolated_Series_sum.groupby(level=0).mean()


#%% plot sed rates

axes[2].plot(Pacific_sed_rate_normalized_interpolated_Series_mean.index,
              Pacific_sed_rate_normalized_interpolated_Series_mean,
              'o-', alpha=1, color='C4',markersize=2, label='Pacific')
axes[2].plot(Atlantic_sed_rate_normalized_interpolated_Series_mean.index,
              Atlantic_sed_rate_normalized_interpolated_Series_mean,
              'o-', alpha=1, color='C5',markersize=2, label='Atlantic')
# axes[2].plot(LR04.index/1000, LR04, color='k', alpha=0.3)

# axes.fill_between(stack['age(kyr)'],
#                   stack['mean(permil)']+2*stack['sigma(permil)'],
#                   stack['mean(permil)']-2*stack['sigma(permil)'],
#                   alpha=0.3,
#                   label='BIGMACS 2sigma')

#%% beautification
# axes.plot(LR04.index/1000, LR04, label='LRO4', color='k')
axes[1].set_xlabel('')
axes[3].set_xlabel('')

axes[2].set_xlim((1500, 2100))
axes[2].set_ylim((0.3, 1.7))
# axes[2].invert_yaxis()

# axes.axvspan(1800, 1900, color='lightgray')

axes[2].legend(loc='lower right')

axes[2].set_ylabel('Normalized sed. rate')
axes[4].set_xlabel('Age (ka BP)')

sns.despine(ax=axes[0], top=True,right=True, left=False, bottom=True)
sns.despine(ax=axes[1], top=True,right=False, left=True, bottom=True)
sns.despine(ax=axes[2], top=True,right=True, left=False, bottom=True)
sns.despine(ax=axes[3], top=True,right=False, left=True, bottom=True)
sns.despine(ax=axes[4], top=True,right=True, left=False, bottom=False)

for i in range(4):
    axes[i].xaxis.set_ticks_position('none')

pos = axes[0].get_position()
pos.y0 -= 0.1
pos.y1 -= 0.1
axes[0].set_position(pos)

pos = axes[4].get_position()
pos.y0 += 0.1
pos.y1 += 0.1
axes[4].set_position(pos)

# shade(fig,axes,1800,1900, 'lightgray')
# shade(fig,axes,1828,1838, 'lightblue')
# shade(fig,axes,1858,1870, 'lightblue')
# axes[2].axvspan(1828,1838, color='lightblue')
# axes[2].axvspan(1858,1870, color='lightblue')

# axes[0].axvspan(1832,1842, color='lightblue')
# axes[3].axvspan(1832,1842, color='lightblue')

# axes[0].axvspan(1862,1874, color='lightblue')
# axes[3].axvspan(1862,1874, color='lightblue')

# letters
axes[0].text(0.01, 0.8, 'A', transform=axes[0].transAxes, fontweight='bold', color='k')
axes[2].text(0.01, 0.8, 'B', transform=axes[2].transAxes, fontweight='bold', color='k')
axes[3].text(0.01, 0.7, 'C', transform=axes[3].transAxes, fontweight='bold', color='k')

for ax in axes:
    ax.axvline(1793, linestyle='dashed', color='gray', zorder=0)
    ax.axvline(1844, linestyle='dashed', color='gray', zorder=0)
    ax.axvline(1875, linestyle='dashed', color='gray', zorder=0)
    ax.axvline(1917, linestyle='dashed', color='gray', zorder=0)
    # ax.axvline(1958, linestyle='dashed', color='gray', zorder=0)
    # ax.axvline(2050, linestyle='dashed', color='gray', zorder=0)
    
axes[2].axhline(1.5, color='gray', zorder=0, alpha=0.5)
axes[2].axhline(1, color='gray', zorder=0, alpha=0.5)
axes[2].axhline(0.5, color='gray', zorder=0, alpha=0.5)
    
for ax in axes:
    ax.set_zorder(10)
    ax.set_facecolor('none')

fig.set_size_inches(6,8)

# plt.savefig('Stack_prec_obliquity_comparison.pdf')
# plt.savefig('Stack_inso_comparison.png', dpi=700)
plt.savefig('Normalized_sed_rate_inso.pdf')