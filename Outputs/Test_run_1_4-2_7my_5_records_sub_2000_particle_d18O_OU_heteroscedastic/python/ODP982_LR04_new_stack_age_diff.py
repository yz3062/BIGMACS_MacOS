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

ODP982_aligned_file_path = '../ages/ODP982.txt'
ODP982_aligned = pd.read_table(ODP982_aligned_file_path, delimiter=' ',)
ODP982_aligned.set_index('depth(m)',inplace=True)

ODP982_original_file_path = '../../../../Stacking/Stack/LR04/982_LR04age.txt'
ODP982_original = pd.read_table(ODP982_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

LR04 = LR04_fetching_func.fetch_d18O()

#%% calculate diff
ODP982_age_diff = ODP982_aligned['median(kyr)'] - ODP982_original.set_index('Depth (mcd)')['Age (ka)']
ODP982_age_diff.dropna(inplace=True)

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

axes.plot(ODP982_original['Depth (mcd)'], ODP982_original['d18O'])
axes.set_xlim((ODP982_age_diff.index.min(),ODP982_age_diff.index.max()))
axes.invert_yaxis()

ax_twin = axes.twinx()
ax_twin.plot(ODP982_age_diff.index,ODP982_age_diff,'--',color='k')

axes.set_ylabel(u'${\delta}^{18}$O (‰)')
ax_twin.set_ylabel('LR04 and new stack age difference (kyr)')
axes.set_xlabel('Depth (mcd)')



fig.set_size_inches(6,4)

plt.savefig('ODP982_LR04_new_stack_age_diff.png', dpi=500)