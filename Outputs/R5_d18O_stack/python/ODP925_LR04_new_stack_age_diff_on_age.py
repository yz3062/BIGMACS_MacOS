#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 15:34:58 2022

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

ODP925_aligned_file_path = '../ages/ODP925.txt'
ODP925_aligned = pd.read_table(ODP925_aligned_file_path, delimiter=' ',)
ODP925_aligned.set_index('depth(m)',inplace=True)

ODP925_original_file_path = '../../../../../Work/Lorraine/Stacking/Stack/LR04/925_LR04age_3.txt'
ODP925_original = pd.read_table(ODP925_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

LR04 = LR04_fetching_func.fetch_d18O()

#%% calculate diff
ODP925_age_diff = ODP925_aligned['median(kyr)'] - ODP925_original.set_index('Depth (mcd)')['Age (ka)']
ODP925_age_diff.dropna(inplace=True)

#%% interp from depth to age
ODP925_age_diff_LR04_age = age_model_interp(ODP925_original['Depth (mcd)'],
                 ODP925_original['Age (ka)'],
                 ODP925_age_diff.index)
#%% interp original d18O to newly aligned depth
ODP925_aligned_d18O = age_model_interp(ODP925_original['Depth (mcd)'], ODP925_original['d18O'], ODP925_aligned.index)

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

ln3 = axes.plot(ODP925_aligned['median(kyr)'], ODP925_aligned_d18O,label='new alignment')
ln1 = axes.plot(LR04.index/1000, LR04, color='k', label='LR04')
axes.set_xlim((ODP925_age_diff_LR04_age.min(),ODP925_age_diff_LR04_age.max()))
axes.invert_yaxis()

ax_twin = axes.twinx()
ln2 = ax_twin.plot(ODP925_age_diff_LR04_age,ODP925_age_diff,'--',color='k',
                   label='Alignment and LR04 diff.')

# legend
lns = ln1+ln2+ln3
labs = [l.get_label() for l in lns]
axes.legend(lns, labs, loc=4)

axes.set_ylabel(u'${\delta}^{18}$O (‰)')
ax_twin.set_ylabel('LR04 and new stack age difference (kyr)')
axes.set_xlabel('Age (ka)')
axes.set_title('ODP 925')


fig.set_size_inches(6,4)

plt.savefig('ODP925_LR04_new_stack_age_diff_on_age.png', dpi=500)