#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 15:58:54 2023

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

ProbStack_upper = Probstack_fetching_func.fetch_d18O_upper()
ProbStack_lower = Probstack_fetching_func.fetch_d18O_lower()
#%% plot
fig, axes = plt.subplots(4,1, sharex=False, sharey=False)
gs  = gridspec.GridSpec(4, 1, height_ratios=[0.3, 1, 0.3, 1])
axes = [plt.subplot(gs[0]),
        plt.subplot(gs[1]),
        plt.subplot(gs[2]),
        plt.subplot(gs[3])]
# BIAGMACS
axes[1].plot(Atlantic_stack.index, Atlantic_stack['mean(permil)'], label='BIGMACS Atlantic', color='C5',zorder=10)
axes[1].plot(Pacific_stack.index, Pacific_stack['mean(permil)'], label='BIGMACS Pacific', color='C4',zorder=10)
# axes[1].fill_between(stack.index,
#                   stack['mean(permil)']+2*stack['sigma(permil)'],
#                   stack['mean(permil)']-2*stack['sigma(permil)'],
#                   alpha=0.3,
#                   label='BIGMACS 2sigma',
#                   color='C0')
# LR04
axes[1].plot(LR04.index/1000, LR04, label='LRO4', color='k', zorder=1)
# ProbStack
# axes[1].plot(ProbStack.index/1000, ProbStack, label='ProbStack', color='C3', zorder=1, alpha=0.5)
# axes[1].fill_between(ProbStack_upper.index/1000,
#                   ProbStack_upper,
#                   ProbStack_lower,
#                   alpha=0.3,
#                   label='ProbStack 2sigma',
#                   color='C3')
# # LR04
axes[1].set_xlim((0, 1350))
axes[1].set_ylim((2.7, 5.4))
axes[1].invert_yaxis()

axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')

# BIGMACS
l2 = axes[3].plot(Atlantic_stack.index, Atlantic_stack['mean(permil)'], label='BIGMACS Atlantic', color='C5',zorder=10)
l3 = axes[3].plot(Pacific_stack.index, Pacific_stack['mean(permil)'], label='BIGMACS Pacific', color='C4',zorder=10)
# axes[3].fill_between(stack.index,
#                   stack['mean(permil)']+2*stack['sigma(permil)'],
#                   stack['mean(permil)']-2*stack['sigma(permil)'],
#                   alpha=0.3,
#                   label='BIGMACS 2sigma',
#                   color='C0')
# LR04
l1 = axes[3].plot(LR04.index/1000, LR04, label='LR04', color='k', zorder=2)
# ProbStack
# l3 = axes[3].plot(ProbStack.index/1000, ProbStack, label='ProbStack', color='C3', zorder=1, alpha=0.5)
# axes[3].fill_between(ProbStack_upper.index/1000,
#                   ProbStack_upper,
#                   ProbStack_lower,
#                   alpha=0.3,
#                   label='ProbStack 2sigma',
#                   color='C3')
axes[3].set_xlim((1350, 2700))
axes[3].set_ylim((2.7, 5))
axes[3].invert_yaxis()
axes[3].axvspan(1800, 1900, color='lightgray')

axes[3].legend(handles=[l1[0], l2[0], l3[0]], ncol=3, loc=[0.5,0.115], fancybox=True, frameon=True)

axes[3].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[3].set_xlabel('Age (ka BP)')

fig.set_size_inches(10,8)

#%% draw geomagnetic chrons
# rectangle height
bar_height = 0.25
# rectangle bottom which is the y lower limit
y_lim_bottom = axes[1].get_ylim()[0]
# draw rectangle
axes[1].add_patch(patches.Rectangle((0, y_lim_bottom-bar_height),
                                    773,
                                    bar_height,
                                    facecolor='k',
                                    edgecolor='k'))
# label rectangle
axes[1].text(773/2, y_lim_bottom-bar_height/2, 'Brunhes',
             horizontalalignment='center',
             verticalalignment='center',
             color='w')
# draw rectangle
axes[1].add_patch(patches.Rectangle((773, y_lim_bottom-bar_height),
                                    1350-773,
                                    bar_height,
                                    facecolor='None',
                                    edgecolor='k'))
# label rectangle
axes[1].text((1350+773)/2, y_lim_bottom-bar_height/2, 'Matuyama',
             horizontalalignment='center',
             verticalalignment='center',
             color='k')
y_lim_bottom = axes[3].get_ylim()[0]
bar_height = 0.23 # a shorter bar height cuz plot is broader
# draw rectangle
axes[3].add_patch(patches.Rectangle((1350, y_lim_bottom-bar_height),
                                    2595-1350,
                                    bar_height,
                                    facecolor='None',
                                    edgecolor='k'))
# label rectangle
axes[3].text((2595+1350)/2, y_lim_bottom-bar_height/2, 'Matuyama',
             horizontalalignment='center',
             verticalalignment='center',
             color='k')
# draw rectangle
axes[3].add_patch(patches.Rectangle((2595, y_lim_bottom-bar_height),
                                    2700-2595,
                                    bar_height,
                                    facecolor='k',
                                    edgecolor='k'))
# label rectangle
axes[3].text((2700+2595)/2, y_lim_bottom-bar_height/2, 'Gauss',
              horizontalalignment='center',
              verticalalignment='center',
              color='w')

#%% plot Milankovitch
axes[0].plot(insolation.index, insolation, color='C1')
axes[0].set_xlim((0, 1350))
axes[0].set_ylabel('65°N'
                   '\n'
                   'summer'
                   '\n'
                   r'(W/$\mathrm{m}^\mathrm{2}$')
axes[2].plot(insolation.index, insolation, color='C1')
axes[2].axvspan(1800, 1900, color='lightgray')
axes[2].set_xlim((1350, 2700))
axes[2].set_ylabel('65°N'
                   '\n'
                   'summer'
                   '\n'
                   r'(W/$\mathrm{m}^\mathrm{2}$')
# remove x axis
sns.despine(ax=axes[0], bottom=True)
sns.despine(ax=axes[2], bottom=True)
# remove x axis labels
axes[0].xaxis.set_ticklabels([])
axes[2].xaxis.set_ticklabels([])
# move down
pos = axes[0].get_position()
pos.y0 -= 0.03
pos.y1 -= 0.03
axes[0].set_position(pos)
pos = axes[2].get_position()
pos.y0 -= 0.03
pos.y1 -= 0.03
axes[2].set_position(pos)
# plt.savefig('Stitched_stack_insolation_two_panel.png', dpi=700)
# plt.savefig('Stitched_stack_insolation_two_panel.pdf')

