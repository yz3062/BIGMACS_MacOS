#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 17:53:03 2023

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
import pyleoclim as pyleo

from scipy import interpolate

sns.set(font='Myriad Pro',palette='husl',style='ticks',context='paper')

plt.rc('text', usetex=True)

# read pacific data
Pacific_path = '../stack.txt'
Pacific_stack = pd.read_table(Pacific_path, delimiter=' ')
Pacific_stack = Pacific_stack.groupby('age(kyr)').mean()

# Atlantic data
Atlantic_path = '../../R58_d18O_stack/stack.txt'
Atlantic_stack = pd.read_table(Atlantic_path, delimiter=' ')
Atlantic_stack = Atlantic_stack.groupby('age(kyr)').mean()

LR04 = LR04_fetching_func.fetch_d18O()

#%% plot
fig, axes = plt.subplots(2,1, sharex=True)
# read into pyleoclim time series
d18O_ts = pyleo.Series(time=Atlantic_stack.index, value=Atlantic_stack['mean(permil)'],
                       time_name='Age',
                       time_unit='kyr BP',
                       value_name='d18O_benthic',
                       value_unit='permil')
# inso_ts.plot()
scal = d18O_ts.wavelet()
# scal.plot(contourf_style={'levels': 30, 'cmap': 'plasma'})
scal_sig = scal.signif_test(method='ar1asym')
scal_sig.plot(ylim=(10, 500),
              ax=axes[0],
              contourf_style={'levels': 30,
                              'cmap': 'plasma',
                              'vmin': 0,
                              'vmax': 8})
axes[0].set_title('')

# read into pyleoclim time series
d18O_ts = pyleo.Series(time=Pacific_stack.index, value=Pacific_stack['mean(permil)'],
                       time_name='Age',
                       time_unit='kyr BP',
                       value_name='d18O_benthic',
                       value_unit='permil')
# inso_ts.plot()
scal = d18O_ts.wavelet()
# scal.plot(contourf_style={'levels': 30, 'cmap': 'plasma'})
scal_sig = scal.signif_test(method='ar1asym')
scal_sig.plot(ylim=(10, 500),
              ax=axes[1],
              contourf_style={'levels': 30,
                              'cmap': 'plasma',
                              'vmin': 0,
                              'vmax': 8})
axes[1].set_title('')

#%% beautification
# plt.subplots_adjust(hspace=0.1)

axes[0].set_xlim(1550, 2100)

# # shade
# shade(fig,axes,1800, 1900)
# for ax in axes:
#     ax.set_zorder(10)
#     ax.set_facecolor('none')
    
# # vertical dashed lines
# for ax in axes:
#     ax.axvline(1719, linestyle='dashed', color='gray', zorder=0)
#     ax.axvline(1736, linestyle='dashed', color='gray', zorder=0)
#     ax.axvline(2025, linestyle='dashed', color='gray', zorder=0)
#     ax.axvline(2055, linestyle='dashed', color='gray', zorder=0)

# axes[0].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
# axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
# axes[-1].set_xlabel('Age (ka BP)')

fig.set_size_inches(8,6)

plt.savefig('Stack_18ma_wavelet.png', dpi=700)
# plt.savefig('Raw_d18O_alignment_18ma_pan.pdf')