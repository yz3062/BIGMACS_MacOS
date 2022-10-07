#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 01:27:53 2022

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import seaborn as sns

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

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

axes.plot(ODP1146_original['Depth (mcd)'], ODP1146_original['d18O'])
axes.set_xlim((0,194.885))
axes.invert_yaxis()

ax_twin = axes.twinx()
ax_twin.plot(ODP1146_age_diff.index,ODP1146_age_diff,'--',color='k')

axes.set_ylabel(u'${\delta}^{18}$O (‰)')
ax_twin.set_ylabel('LR04 and new stack age difference (kyr)')
axes.set_xlabel('Depth (mcd)')



fig.set_size_inches(6,4)

plt.savefig('ODP1146_LR04_new_stack_age_diff.png', dpi=700)