#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 17:08:51 2022

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

ODP929_aligned_file_path = '../ages/ODP929.txt'
ODP929_aligned = pd.read_table(ODP929_aligned_file_path, delimiter=' ',)
ODP929_aligned.set_index('depth(m)',inplace=True)

ODP929_original_file_path = '../../../../Stacking/Stack/LR04/929_LR04age.txt'
ODP929_original = pd.read_table(ODP929_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])
# ODP929_original.set_index('Depth (mcd)',inplace=True)

LR04 = LR04_fetching_func.fetch_d18O()

#%% calculate diff
ODP929_age_diff = ODP929_aligned['median(kyr)'] - ODP929_original.set_index('Depth (mcd)')['Age (ka)']
ODP929_age_diff.dropna(inplace=True)
#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

axes.plot(ODP929_original['Depth (mcd)'], ODP929_original['d18O'])
axes.set_xlim((ODP929_age_diff.index.min(),ODP929_age_diff.index.max()))
axes.invert_yaxis()

ax_twin = axes.twinx()
ax_twin.plot(ODP929_age_diff.index,ODP929_age_diff,'--',color='k')

axes.set_ylabel(u'${\delta}^{18}$O (‰)')
ax_twin.set_ylabel('LR04 and new stack age difference (kyr)')
axes.set_xlabel('Depth (mcd)')

# axes[1].plot(ODP929_original['Age (ka)'], ODP929_original['d18O'],
#              label='ODP-929 on LR04 age')

# # Find original depths that exist in aligned and select only those rows
# # Source: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#deprecate-loc-reindex-listlike
# axes[1].plot(ODP929_aligned.loc[ODP929_aligned.index.intersection(ODP929_original['Depth (mcd)'])]['median(kyr)'],
#               ODP929_original['d18O'])

# # axes[1].plot(LR04.index/1000, LR04, label='LR04')
# axes[1].set_xlim((0,2000))
# axes[1].legend()
# axes[1].invert_yaxis()

# axes[2].plot(ODP929_age_diff.index,ODP929_age_diff,'-',label='ODP 929')
# axes[2].set_xlim((0,67.4))

fig.set_size_inches(6,4)

plt.savefig('ODP929_LR04_new_stack_age_diff.png', dpi=500)