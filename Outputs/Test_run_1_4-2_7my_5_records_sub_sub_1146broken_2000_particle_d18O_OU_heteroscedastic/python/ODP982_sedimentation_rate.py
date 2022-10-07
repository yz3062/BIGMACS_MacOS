#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 12:17:04 2022

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

ODP982_aligned_file_path = '../ages/ODP982.txt'
ODP982_aligned = pd.read_table(ODP982_aligned_file_path, delimiter=' ',)

LR04 = LR04_fetching_func.fetch_d18O()

stack_file_path = '../stack.txt'
stack = pd.read_table(stack_file_path, delimiter=' ')

#%% sedimentation rate
ODP982_aligned['Sedimentation rate'] = ODP982_aligned['depth(m)'].diff()*100/ODP982_aligned['median(kyr)'].diff()

#%% plot
fig, axes = plt.subplots(1,1, sharex=False)

ln1 = axes.plot(stack['age(kyr)'], stack['mean(permil)'], label='BIGMACS stack',
                color='#77AC30')
ln2 = axes.plot(LR04.index/1000, LR04, color='k', label='LR04',)
axes.set_xlim((ODP982_aligned['median(kyr)'].min(),ODP982_aligned['median(kyr)'].max()))
axes.invert_yaxis()

ax_twin = axes.twinx()
ln2 = ax_twin.plot(ODP982_aligned['median(kyr)'],ODP982_aligned['Sedimentation rate'])
ax_twin.set_ylim(top=16)

# legend
axes.legend()
# lns = ln1+ln2
# labs = [l.get_label() for l in lns]
# axes.legend(lns, labs, loc=4)

axes.set_ylabel(u'${\delta}^{18}$O (‰)')
ax_twin.set_ylabel('Sedimentation rate (cm/kyr)', color='C0')
ax_twin.spines['right'].set_color('C0')
ax_twin.tick_params(axis='y', colors='C0')
axes.set_xlabel('Age (ka)')
axes.set_title('ODP 982')

fig.set_size_inches(6,4)

plt.savefig('ODP982_sedimentation_rate.png', dpi=500)