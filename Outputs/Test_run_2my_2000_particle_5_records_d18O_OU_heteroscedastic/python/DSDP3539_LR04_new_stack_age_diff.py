#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 01:32:47 2022

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

DSDP593_aligned_file_path = '../ages/DSDP593.txt'
DSDP593_aligned = pd.read_table(DSDP593_aligned_file_path, delimiter=' ',)
DSDP593_aligned.set_index('depth(m)',inplace=True)

DSDP593_original_file_path = '../../../../Stacking/Stack/NewRecords/DSDP593.txt'
DSDP593_original = pd.read_table(DSDP593_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

LR04 = LR04_fetching_func.fetch_d18O()

#%% calculate diff
DSDP593_age_diff = DSDP593_aligned['median(kyr)'] - DSDP593_original.set_index('Depth (mcd)')['Age (ka)']
DSDP593_age_diff.dropna(inplace=True)

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

axes.plot(DSDP593_original['Depth (mcd)'], DSDP593_original['d18O'])
axes.set_xlim((0,35.39))
axes.invert_yaxis()

ax_twin = axes.twinx()
ax_twin.plot(DSDP593_age_diff.index,DSDP593_age_diff,'--',color='k')

axes.set_ylabel(u'${\delta}^{18}$O (‰)')
ax_twin.set_ylabel('LR04 and new stack age difference (kyr)')
axes.set_xlabel('Depth (mcd)')



fig.set_size_inches(6,4)

plt.savefig('DSDP593_LR04_new_stack_age_diff.png', dpi=700)