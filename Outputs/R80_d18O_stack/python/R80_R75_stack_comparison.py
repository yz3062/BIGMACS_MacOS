#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:03:36 2022

@author: zhou
"""

import pandas as pd
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

stack_2_path = '../../R75_d18O_stack/stack.txt'
# stack = scipy.io.loadmat(stack_path)
stack_2 = pd.read_table(stack_2_path, delimiter=' ')

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

axes.plot(stack['age(kyr)'], stack['mean(permil)'], label='Additional tie points')
axes.fill_between(stack['age(kyr)'],
                  stack['mean(permil)']+2*stack['sigma(permil)'],
                  stack['mean(permil)']-2*stack['sigma(permil)'],
                  alpha=0.3)
axes.plot(stack_2['age(kyr)'], stack_2['mean(permil)'], label='Original',
          color='C1')
axes.fill_between(stack_2['age(kyr)'],
                  stack_2['mean(permil)']+2*stack_2['sigma(permil)'],
                  stack_2['mean(permil)']-2*stack_2['sigma(permil)'],
                  alpha=0.3)

axes.set_xlim((stack['age(kyr)'].min(),stack['age(kyr)'].max()))
axes.set_ylim((3.2, 4.6))
axes.invert_yaxis()

axes.legend()

axes.set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes.set_xlabel('Age (ka BP)')

fig.set_size_inches(6,4)

plt.savefig('R80_R75_stack_comparison.png', dpi=500)