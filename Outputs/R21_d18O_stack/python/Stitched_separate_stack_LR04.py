#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:25:09 2022

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../../Work/Lorraine/LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.io

from scipy import interpolate

def age_model_interp(dated_depths, dated_ages, all_depths):
    f = interpolate.interp1d(dated_depths, dated_ages, fill_value='extrapolate')
    all_ages = f(all_depths)
    return all_ages

sns.set(font='Arial',palette='husl',style='whitegrid',context='paper')

stack_path = '../stack.txt'
# stack = scipy.io.loadmat(stack_path)
stack = pd.read_table(stack_path, delimiter=' ')

stack_2_path = '../../R20_d18O_stack/stack.txt'
stack_2 = pd.read_table(stack_2_path, delimiter=' ')

stack_3_path = '../../R18_d18O_stack/stack.txt'
stack_3 = pd.read_table(stack_3_path, delimiter=' ')

stack_4_path = '../../R16_d18O_stack/stack.txt'
stack_4 = pd.read_table(stack_4_path, delimiter=' ')

stack_5_path = '../../R7_d18O_stack/stack.txt'
stack_5 = pd.read_table(stack_5_path, delimiter=' ')

LR04 = LR04_fetching_func.fetch_d18O()

#%% plot
fig, axes = plt.subplots(2,1, sharex=False)

axes[0].plot(stack['age(kyr)'], stack['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[0].fill_between(stack['age(kyr)'],
                  stack['mean(permil)']+2*stack['sigma(permil)'],
                  stack['mean(permil)']-2*stack['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[0].plot(stack_2['age(kyr)'], stack_2['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[0].fill_between(stack_2['age(kyr)'],
                  stack_2['mean(permil)']+2*stack_2['sigma(permil)'],
                  stack_2['mean(permil)']-2*stack_2['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[0].plot(stack_3['age(kyr)'], stack_3['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[0].fill_between(stack_3['age(kyr)'],
                  stack_3['mean(permil)']+2*stack_3['sigma(permil)'],
                  stack_3['mean(permil)']-2*stack_3['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[0].plot(stack_4['age(kyr)'], stack_4['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[0].fill_between(stack_4['age(kyr)'],
                  stack_4['mean(permil)']+2*stack_4['sigma(permil)'],
                  stack_4['mean(permil)']-2*stack_4['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[0].plot(stack_5['age(kyr)'], stack_5['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[0].fill_between(stack_5['age(kyr)'],
                  stack_5['mean(permil)']+2*stack_5['sigma(permil)'],
                  stack_5['mean(permil)']-2*stack_5['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[0].plot(LR04.index/1000, LR04, label='LRO4', color='k', zorder=1, alpha=0.5)
axes[0].set_xlim((0, 1350))
axes[0].invert_yaxis()

# axes.legend()

axes[0].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')

axes[1].plot(stack['age(kyr)'], stack['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[1].fill_between(stack['age(kyr)'],
                  stack['mean(permil)']+2*stack['sigma(permil)'],
                  stack['mean(permil)']-2*stack['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[1].plot(stack_2['age(kyr)'], stack_2['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[1].fill_between(stack_2['age(kyr)'],
                  stack_2['mean(permil)']+2*stack_2['sigma(permil)'],
                  stack_2['mean(permil)']-2*stack_2['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[1].plot(stack_3['age(kyr)'], stack_3['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[1].fill_between(stack_3['age(kyr)'],
                  stack_3['mean(permil)']+2*stack_3['sigma(permil)'],
                  stack_3['mean(permil)']-2*stack_3['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[1].plot(stack_4['age(kyr)'], stack_4['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[1].fill_between(stack_4['age(kyr)'],
                  stack_4['mean(permil)']+2*stack_4['sigma(permil)'],
                  stack_4['mean(permil)']-2*stack_4['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[1].plot(stack_5['age(kyr)'], stack_5['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[1].fill_between(stack_5['age(kyr)'],
                  stack_5['mean(permil)']+2*stack_5['sigma(permil)'],
                  stack_5['mean(permil)']-2*stack_5['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[1].plot(LR04.index/1000, LR04, label='LRO4', color='k', zorder=1, alpha=0.5)
axes[1].set_xlim((1350, 2700))
axes[1].invert_yaxis()

# axes.legend()

axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[1].set_xlabel('Age (ka BP)')

fig.set_size_inches(6,4)

plt.savefig('Stitched_stack_LR04.png', dpi=500)

