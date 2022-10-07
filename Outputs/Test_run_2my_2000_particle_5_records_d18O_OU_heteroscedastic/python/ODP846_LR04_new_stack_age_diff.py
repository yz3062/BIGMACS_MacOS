#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 21:42:26 2022

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

ODP846_aligned_file_path = '../ages/ODP846.txt'
ODP846_aligned = pd.read_table(ODP846_aligned_file_path, delimiter=' ',)
ODP846_aligned.set_index('depth(m)',inplace=True)

ODP846_original_file_path = '../../../../Stacking/Stack/LR04/846_LR04age.txt'
ODP846_original = pd.read_table(ODP846_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

LR04 = LR04_fetching_func.fetch_d18O()

#%% calculate diff
ODP846_age_diff = ODP846_aligned['median(kyr)'] - ODP846_original.set_index('Depth (mcd)')['Age (ka)']
ODP846_age_diff.dropna(inplace=True)

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

axes.plot(ODP846_original['Depth (mcd)'], ODP846_original['d18O'])
axes.set_xlim((0,76.05))
axes.invert_yaxis()

ax_twin = axes.twinx()
ax_twin.plot(ODP846_age_diff.index,ODP846_age_diff,'--',color='k')

axes.set_ylabel(u'${\delta}^{18}$O (‰)')
ax_twin.set_ylabel('LR04 and new stack age difference (kyr)')
axes.set_xlabel('Depth (mcd)')



fig.set_size_inches(6,4)

plt.savefig('ODP846_LR04_new_stack_age_diff.png', dpi=700)