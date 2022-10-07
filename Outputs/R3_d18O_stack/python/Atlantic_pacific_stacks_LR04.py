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

from scipy import interpolate

def age_model_interp(dated_depths, dated_ages, all_depths):
    f = interpolate.interp1d(dated_depths, dated_ages, fill_value='extrapolate')
    all_ages = f(all_depths)
    return all_ages

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

atlantic_stack_path = '../stack.txt'
atlantic_stack = pd.read_table(atlantic_stack_path, delimiter=' ')

pacific_stack_path = '../../R4_d18O_stack/stack.txt'
pacific_stack = pd.read_table(pacific_stack_path, delimiter=' ')

LR04 = LR04_fetching_func.fetch_d18O()

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

axes.plot(atlantic_stack['age(kyr)'], atlantic_stack['mean(permil)']+0.5,label='Atlantic stack')
axes.plot(pacific_stack['age(kyr)'], pacific_stack['mean(permil)'],label='pacific stack')
axes.plot(LR04.index/1000, LR04, label='LRO4', color='k')
axes.set_xlim((pacific_stack['age(kyr)'].min(),pacific_stack['age(kyr)'].max()))
axes.invert_yaxis()

axes.legend()

axes.set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes.set_xlabel('Age (ka BP)')

fig.set_size_inches(6,4)

plt.savefig('Atlantic_pacific_stacks_LR04.png', dpi=500)