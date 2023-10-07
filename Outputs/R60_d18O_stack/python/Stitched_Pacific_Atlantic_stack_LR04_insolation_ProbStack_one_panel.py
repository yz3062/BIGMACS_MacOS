#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 23:12:54 2023

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

sns.set(font='Arial',palette='husl',style='whitegrid',context='talk')

stack_1_path = '../../R59_d18O_stack/stack.txt'
stack_1 = pd.read_table(stack_1_path, delimiter=' ')

stack_2_path = '../../R44_d18O_stack/stack.txt'
stack_2 = pd.read_table(stack_2_path, delimiter=' ')

Pacific_stack = pd.concat([stack_1, stack_2])
Pacific_stack = Pacific_stack.groupby('age(kyr)').mean()

stack_1_path = '../../R60_d18O_stack/stack.txt'
stack_1 = pd.read_table(stack_1_path, delimiter=' ')

stack_2_path = '../../R45_d18O_stack/stack.txt'
stack_2 = pd.read_table(stack_2_path, delimiter=' ')

Atlantic_stack = pd.concat([stack_1, stack_2])
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
l1 = axes[1].plot(Pacific_stack.index, Pacific_stack['mean(permil)'], label='BIGMACS Pacific', alpha=0.8, color='C4')
l4 = axes[1].plot(Atlantic_stack.index, Atlantic_stack['mean(permil)'], label='BIGMACS Atlantic', alpha=0.8, color='C5')

l2 = axes[1].plot(LR04.index/1000, LR04, label='LR04', color='gray', zorder=1, alpha=0.5)

# axes[1].axvline(300, color='C4', linestyle='--')
# axes[1].axvline(700, color='C5', linestyle='--')

# axes[1].axvline(1750, color='r', linestyle='--')
# axes[1].axvline(1950, color='r', linestyle='--')

axes[1].axvspan(1800, 1900, color='lightgray')

axes[1].set_xlim((0, 2700))
axes[1].invert_yaxis()

axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[1].set_ylim(bottom=5.7)

axes[1].legend(handles=[l2[0], l1[0], l4[0]], ncol=3, loc=[0.3,0.11], fancybox=True)

fig.set_size_inches(15,8)

#%% plot geomagnetic chrons
bar_height = 0.25
y_lim_bottom = axes[1].get_ylim()[0]
axes[1].add_patch(patches.Rectangle((0, y_lim_bottom-bar_height),
                                    773,
                                    bar_height,
                                    facecolor='k',
                                    edgecolor='k'))
axes[1].text(773/2, y_lim_bottom-bar_height/2, 'Brunhes',
             horizontalalignment='center',
             verticalalignment='center',
             color='w')
axes[1].add_patch(patches.Rectangle((773, y_lim_bottom-bar_height),
                                    2595-773,
                                    bar_height,
                                    facecolor='None',
                                    edgecolor='k'))
axes[1].text((2595+773)/2, y_lim_bottom-bar_height/2, 'Matuyama',
             horizontalalignment='center',
             verticalalignment='center',
             color='k')

axes[1].add_patch(patches.Rectangle((2595, y_lim_bottom-bar_height),
                                    2700-2595,
                                    bar_height,
                                    facecolor='k',
                                    edgecolor='k'))
axes[1].text((2700+2595)/2, y_lim_bottom-bar_height/2, 'Gauss',
              horizontalalignment='center',
              verticalalignment='center',
              color='w')

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
plt.savefig('Stitched_long_Pacific_Atlantic_stack_LR04_insolation.png', dpi=700)
