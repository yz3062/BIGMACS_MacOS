#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 14:50:52 2022

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import interpolate

def age_model_interp(dated_depths, dated_ages, all_depths):
    f = interpolate.interp1d(dated_depths, dated_ages, fill_value='extrapolate')
    all_ages = f(all_depths)
    return all_ages

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

ODP1146_aligned_file_path = '../ages/ODP1146.txt'
ODP1146_aligned = pd.read_table(ODP1146_aligned_file_path, delimiter=' ',)
ODP1146_aligned.set_index('depth(m)',inplace=True)

ODP1146_original_file_path = '../../../../Stacking/Stack/NewRecords/ODP1146.txt'
ODP1146_original = pd.read_table(ODP1146_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

LR04 = LR04_fetching_func.fetch_d18O()

#%% calculate diff
ODP1146_age_diff = ODP1146_aligned['median(kyr)'] - ODP1146_original.set_index('Depth (mcd)')['Age (ka)']
ODP1146_age_diff.dropna(inplace=True)

#%% interp from depth to age
ODP1146_age_diff_LR04_age = age_model_interp(ODP1146_original['Depth (mcd)'],
                 ODP1146_original['Age (ka)'],
                 ODP1146_age_diff.index)

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

axes.plot(ODP1146_original['Age (ka)'], ODP1146_original['d18O'])
axes.set_xlim((ODP1146_age_diff_LR04_age.min(),ODP1146_age_diff_LR04_age.max()))
axes.invert_yaxis()

ax_twin = axes.twinx()
ax_twin.plot(ODP1146_age_diff_LR04_age,ODP1146_age_diff,'--',color='k')

axes.set_ylabel(u'${\delta}^{18}$O (‰)')
ax_twin.set_ylabel('LR04 and new stack age difference (kyr)')
axes.set_xlabel('Age (ka)')

fig.set_size_inches(6,4)

plt.savefig('ODP1146_LR04_new_stack_age_diff_on_age.png', dpi=500)