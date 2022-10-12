#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:03:36 2022

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

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

stack_path = '../stack.txt'
# stack = scipy.io.loadmat(stack_path)
stack = pd.read_table(stack_path, delimiter=' ')

LR04 = LR04_fetching_func.fetch_d18O()

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

axes.plot(stack['age(kyr)'], stack['mean(permil)'])
axes.plot(LR04.index/1000, LR04, label='LRO4', color='k')
axes.set_xlim((stack['age(kyr)'].min(),stack['age(kyr)'].max()))
axes.invert_yaxis()

axes.legend()

axes.set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes.set_xlabel('Age (ka BP)')

fig.set_size_inches(6,4)

# plt.savefig('Stack_LR04.png', dpi=500)