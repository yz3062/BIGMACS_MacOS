#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 18:46:01 2022

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
# stack = scipy.io.loadmat(stack_path)
stack_1 = pd.read_table(stack_1_path, delimiter=' ')
# stack_1.set_index('age(kyr)', inplace=True)

stack_2_path = '../../R20_d18O_stack/stack.txt'
stack_2 = pd.read_table(stack_2_path, delimiter=' ')
# stack_2.set_index('age(kyr)', inplace=True)

stack_3_path = '../../R18_d18O_stack/stack.txt'
stack_3 = pd.read_table(stack_3_path, delimiter=' ')
# stack_3.set_index('age(kyr)', inplace=True)

stack_4_path = '../../R16_d18O_stack/stack.txt'
stack_4 = pd.read_table(stack_4_path, delimiter=' ')
# stack_4.set_index('age(kyr)', inplace=True)

stack_5_path = '../../R7_d18O_stack/stack.txt'
stack_5 = pd.read_table(stack_5_path, delimiter=' ')
# stack_5.set_index('age(kyr)', inplace=True)

stack = pd.concat([stack_1, stack_2, stack_3, stack_4, stack_5])
stack = stack.groupby('age(kyr)').mean()

LR04 = LR04_fetching_func.fetch_d18O()

insolation = Milankovitch_fetching_func.fetch_65N_summer_insolation()

ProbStack = Probstack_fetching_func.fetch_d18O()

#%% plot
fig, axes = plt.subplots(4,1, sharex=False, sharey=False)
gs  = gridspec.GridSpec(4, 1, height_ratios=[0.3, 1, 0.3, 1])
axes = [plt.subplot(gs[0]),
        plt.subplot(gs[1]),
        plt.subplot(gs[2]),
        plt.subplot(gs[3])]
# BIAGMACS
axes[1].plot(stack.index, stack['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[1].fill_between(stack.index,
                  stack['mean(permil)']+2*stack['sigma(permil)'],
                  stack['mean(permil)']-2*stack['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')
# LR04
axes[1].plot(LR04.index/1000, LR04, label='LRO4', color='k', zorder=1, alpha=0.5)
# ProbStack
axes[1].plot(ProbStack.index/1000, ProbStack, label='ProbStack', color='C3', zorder=1, alpha=0.5)
axes[1].set_xlim((0, 1350))
axes[1].invert_yaxis()

axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[1].set_ylim(bottom=5.7)

# BIGMACS
l1 = axes[3].plot(stack.index, stack['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[3].fill_between(stack.index,
                  stack['mean(permil)']+2*stack['sigma(permil)'],
                  stack['mean(permil)']-2*stack['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')
# LR04
l2 = axes[3].plot(LR04.index/1000, LR04, label='LR04', color='k', zorder=1, alpha=0.5)
# ProbStack
l3 = axes[3].plot(ProbStack.index/1000, ProbStack, label='ProbStack', color='C3', zorder=1, alpha=0.5)
axes[3].set_xlim((1350, 2700))
axes[3].invert_yaxis()

axes[3].legend(handles=[l1[0], l2[0], l3[0]], ncol=3, loc=[0.6,0.11])

axes[3].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[3].set_xlabel('Age (ka BP)')
axes[3].set_ylim(bottom=5)

fig.set_size_inches(10,8)

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
                                    1350-773,
                                    bar_height,
                                    facecolor='None',
                                    edgecolor='k'))
axes[1].text((1350+773)/2, y_lim_bottom-bar_height/2, 'Matuyama',
             horizontalalignment='center',
             verticalalignment='center',
             color='k')
y_lim_bottom = axes[3].get_ylim()[0]
bar_height = 0.23 # a shorter bar height cuz plot is broader
axes[3].add_patch(patches.Rectangle((1350, y_lim_bottom-bar_height),
                                    2595-1350,
                                    bar_height,
                                    facecolor='None',
                                    edgecolor='k'))
axes[3].text((2595+1350)/2, y_lim_bottom-bar_height/2, 'Matuyama',
             horizontalalignment='center',
             verticalalignment='center',
             color='k')
axes[3].add_patch(patches.Rectangle((2595, y_lim_bottom-bar_height),
                                    2700-2595,
                                    bar_height,
                                    facecolor='k',
                                    edgecolor='k'))
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
# plt.savefig('Stitched_stack_LR04_insolation.png', dpi=500)
plt.savefig('Stitched_stack_LR04_insolation_ProbStack.pdf')

