#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 23:25:09 2023

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../../Work/Lorraine/LR04/python")
sys.path.append("../../../../../Work/McManus/Milankovitch/python")
sys.path.append("../../../../../Work/McManus/HMM-Stack-master/python")
import LR04_fetching_func
import Milankovitch_fetching_func
import Probstack_fetching_func
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
# import scipy.io
from matplotlib import gridspec

sns.set(font='Arial',palette='husl',style='whitegrid',context='paper')

stack_1_path = '../stack.txt'
stack_1 = pd.read_table(stack_1_path, delimiter=' ')

stack_2_path = '../../R13_d18O_stack/stack.txt'
stack_2 = pd.read_table(stack_2_path, delimiter=' ')

stack_3_path = '../../R23_d18O_stack/stack.txt'
stack_3 = pd.read_table(stack_3_path, delimiter=' ')

stack_4_path = '../../R25_d18O_stack/stack.txt'
stack_4 = pd.read_table(stack_4_path, delimiter=' ')

stack_5_path = '../../R27_d18O_stack/stack.txt'
stack_5 = pd.read_table(stack_5_path, delimiter=' ')

stack_6_path = '../../R29_d18O_stack/stack.txt'
stack_6 = pd.read_table(stack_5_path, delimiter=' ')

Pacific_stack = pd.concat([stack_1, stack_2, stack_3, stack_4, stack_5, stack_6])
Pacific_stack = Pacific_stack.groupby('age(kyr)').mean()

stack_1_path = '../../R28_d18O_stack/stack.txt'
stack_1 = pd.read_table(stack_1_path, delimiter=' ')

stack_2_path = '../../R12_d18O_stack/stack.txt'
stack_2 = pd.read_table(stack_2_path, delimiter=' ')

stack_3_path = '../../R22_d18O_stack/stack.txt'
stack_3 = pd.read_table(stack_3_path, delimiter=' ')

stack_4_path = '../../R24_d18O_stack/stack.txt'
stack_4 = pd.read_table(stack_4_path, delimiter=' ')

stack_5_path = '../../R26_d18O_stack/stack.txt'
stack_5 = pd.read_table(stack_5_path, delimiter=' ')

stack_6_path = '../../R28_d18O_stack/stack.txt'
stack_6 = pd.read_table(stack_5_path, delimiter=' ')

Atlantic_stack = pd.concat([stack_1, stack_2, stack_3, stack_4, stack_5, stack_6])
Atlantic_stack = Atlantic_stack.groupby('age(kyr)').mean()

LR04 = LR04_fetching_func.fetch_d18O()

insolation = Milankovitch_fetching_func.fetch_65N_summer_insolation()

ProbStack = Probstack_fetching_func.fetch_d18O()

#%% plot
fig, axes = plt.subplots(2,1, sharex=False, sharey=False)
gs  = gridspec.GridSpec(2, 1, height_ratios=[0.3, 1])
axes = [plt.subplot(gs[0]),
        plt.subplot(gs[1])]
# BIAGMACS
# l1 = axes[1].plot(Pacific_stack.index, Pacific_stack['mean(permil)'], label='BIGMACS Pacific', alpha=0.8, color='C4')
# l4 = axes[1].plot(Atlantic_stack.index, Atlantic_stack['mean(permil)'], label='BIGMACS Atlantic', alpha=0.8, color='C5')
basin_diff = Atlantic_stack['mean(permil)'] - Pacific_stack['mean(permil)']
axes[1].plot(Pacific_stack.index, 
             basin_diff,
             color='pink')
axes[1].set_xlim((0, 2700))
axes[1].invert_yaxis()

axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
# axes[1].set_ylim(bottom=5.7)

fig.set_size_inches(15,8)

axes[1].axvline(1400, color='r')
axes[1].axvline(700, color='r')
axes[1].axvline(300, color='r')
axes[1].axvline(100, color='r')

#%% plot Milankovitch
axes[0].plot(insolation.index, insolation, color='C1')
axes[0].set_xlim((0, 2700))
axes[0].set_ylabel('65°N'
                   '\n'
                   'summer'
                   '\n'
                   r'(W/$\mathrm{m}^\mathrm{2}$')

# remove x axis
sns.despine(ax=axes[0], bottom=True)
# remove x axis labels
axes[0].xaxis.set_ticklabels([])
# move down
pos = axes[0].get_position()
pos.y0 -= 0.03
pos.y1 -= 0.03
axes[0].set_position(pos)

# plt.savefig('Stitched_stack_LR04_insolation.png', dpi=500)
plt.savefig('Basin_diff_insolation.pdf')
