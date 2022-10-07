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

ODP928_aligned_file_path = '../ages/ODP928.txt'
ODP928_aligned = pd.read_table(ODP928_aligned_file_path, delimiter=' ',)
ODP928_aligned.set_index('depth(m)',inplace=True)

ODP928_original_file_path = '../../../../../Work/Lorraine/Stacking/Stack/LR04/928_LR04age.txt'
ODP928_original = pd.read_table(ODP928_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

LR04 = LR04_fetching_func.fetch_d18O()

#%% calculate diff
ODP928_age_diff = ODP928_aligned['median(kyr)'] - ODP928_original.set_index('Depth (mcd)')['Age (ka)']
ODP928_age_diff.dropna(inplace=True)

#%% interp from depth to age
ODP928_age_diff_LR04_age = age_model_interp(ODP928_original['Depth (mcd)'],
                 ODP928_original['Age (ka)'],
                 ODP928_age_diff.index)
#%% interp original d18O to newly aligned depth
ODP928_aligned_d18O = age_model_interp(ODP928_original['Depth (mcd)'], ODP928_original['d18O'], ODP928_aligned.index)

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

ln1 = axes.plot(ODP928_aligned['median(kyr)'], ODP928_aligned_d18O,label='new alignment')
ln2 = axes.plot(ODP928_original['Age (ka)'], ODP928_original['d18O'],label='LR04 alignment')
ln3 = axes.plot(LR04.index/1000, LR04, color='k', label='LR04')
axes.set_xlim((ODP928_age_diff_LR04_age.min(),ODP928_age_diff_LR04_age.max()))
axes.invert_yaxis()

ax_twin = axes.twinx()
ln4 = ax_twin.plot(ODP928_age_diff_LR04_age,ODP928_age_diff,'--',color='k',
                   label='Alignment and LR04 diff.')

# legend
lns = ln1+ln2+ln3+ln4
labs = [l.get_label() for l in lns]
axes.legend(lns, labs, loc=4)

axes.set_ylabel(u'${\delta}^{18}$O (‰)')
ax_twin.set_ylabel('LR04 and new stack age difference (kyr)')
axes.set_xlabel('Age (ka)')
axes.set_title('ODP 928')


fig.set_size_inches(6,4)

plt.savefig('ODP928_LR04_new_stack_age_diff_on_age.png', dpi=500)