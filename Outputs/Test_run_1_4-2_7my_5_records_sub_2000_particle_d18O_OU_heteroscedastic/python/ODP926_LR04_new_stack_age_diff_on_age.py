#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 14:46:43 2022

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

ODP926_aligned_file_path = '../ages/ODP926.txt'
ODP926_aligned = pd.read_table(ODP926_aligned_file_path, delimiter=' ',)
ODP926_aligned.set_index('depth(m)',inplace=True)

ODP926_original_file_path = '../../../../Stacking/Stack/NewRecords/ODP926.txt'
ODP926_original = pd.read_table(ODP926_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

LR04 = LR04_fetching_func.fetch_d18O()

#%% calculate diff
ODP926_age_diff = ODP926_aligned['median(kyr)'] - ODP926_original.set_index('Depth (mcd)')['Age (ka)']
ODP926_age_diff.dropna(inplace=True)

#%% interp from depth to age
ODP926_age_diff_LR04_age = age_model_interp(ODP926_original['Depth (mcd)'],
                 ODP926_original['Age (ka)'],
                 ODP926_age_diff.index)

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

axes.plot(ODP926_original['Age (ka)'], ODP926_original['d18O'])
axes.set_xlim((ODP926_age_diff_LR04_age.min(),ODP926_age_diff_LR04_age.max()))
axes.invert_yaxis()

ax_twin = axes.twinx()
ax_twin.plot(ODP926_age_diff_LR04_age,ODP926_age_diff,'--',color='k')

axes.set_ylabel(u'${\delta}^{18}$O (‰)')
ax_twin.set_ylabel('LR04 and new stack age difference (kyr)')
axes.set_xlabel('Age (ka)')

fig.set_size_inches(6,4)

plt.savefig('ODP926_LR04_new_stack_age_diff_on_age.png', dpi=500)