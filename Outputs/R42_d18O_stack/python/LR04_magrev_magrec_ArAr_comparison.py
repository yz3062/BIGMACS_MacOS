#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 12:26:34 2025

@author: zhou

This script plots the magrev stack with astronomically tuned and ArAr-based reversal and excursion ages
This script was made in mistake. I meant to compare the AstroChron results using these two magrev stacks as input
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
from scipy import interpolate

sns.set(font='Arial',palette='husl',style='whitegrid',context='notebook')

def age_model_interp(dated_depths, dated_ages, all_depths):
    f = interpolate.interp1d(dated_depths, dated_ages, fill_value='extrapolate')
    all_ages = f(all_depths)
    return all_ages

stack_1_path = '../stack.txt'
stack_1 = pd.read_table(stack_1_path, delimiter=' ')

stack_2_path = '../../R38_d18O_stack/stack.txt'
stack_2 = pd.read_table(stack_2_path, delimiter=' ')

stack_3_path = '../../R39_d18O_stack/stack.txt'
stack_3 = pd.read_table(stack_3_path, delimiter=' ')

stack_4_path = '../../R40_d18O_stack/stack.txt'
stack_4 = pd.read_table(stack_4_path, delimiter=' ')

stack_5_path = '../../R41_d18O_stack/stack.txt'
stack_5 = pd.read_table(stack_5_path, delimiter=' ')

stack = pd.concat([stack_1, stack_2, stack_3, stack_4, stack_5])
stack = stack.groupby('age(kyr)').mean()

# read untuned ArAr ages
untuned_ArAr_df = pd.read_excel('Untuned_results_mean_exclusion_expanded_1172_removed_ArAr.xlsx')
# ignore reversals
untuned_ArAr_df = untuned_ArAr_df[untuned_ArAr_df['Reversal']!='y']

stack_untuned_ArAr_age = age_model_interp(untuned_ArAr_df['Old age'],
                               untuned_ArAr_df['New age'],
                               stack.index)

# read untuned ages
untuned_df = pd.read_excel('Untuned_results_mean_exclusion_expanded_1172_removed_GTS2020_global.xlsx')
# ignore reversals
untuned_df = untuned_df[untuned_df['Reversal']!='y']

stack_untuned_age = age_model_interp(untuned_df['Old age'],
                               untuned_df['New age'],
                               stack.index)

LR04 = LR04_fetching_func.fetch_d18O()

insolation = Milankovitch_fetching_func.fetch_65N_summer_insolation()

# ProbStack = Probstack_fetching_func.fetch_d18O()

tuned_stack = pd.read_excel('../R/tuned_stack_unextrapolated.xlsx')

#%% plot
fig, axes = plt.subplots(4,1, sharex=False, sharey=False)
gs  = gridspec.GridSpec(4, 1, height_ratios=[0.3, 1, 0.3, 1])
axes = [plt.subplot(gs[0]),
        plt.subplot(gs[1]),
        plt.subplot(gs[2]),
        plt.subplot(gs[3])]
# # BIAGMACS
# axes[1].plot(stack.index, stack['mean(permil)'], label='BIGMACS', alpha=0.8, color='C4')
# axes[1].fill_between(stack.index,
#                   stack['mean(permil)']+2*stack['sigma(permil)'],
#                   stack['mean(permil)']-2*stack['sigma(permil)'],
#                   alpha=0.3,
#                   label='BIGMACS 2sigma',
#                   color='C4')
# LR04
axes[1].plot(LR04.index/1000, LR04, label='LRO4', color='k', zorder=1, alpha=0.5)
# # ProbStack
# axes[1].plot(ProbStack.index/1000, ProbStack, label='ProbStack', color='C3', zorder=1, alpha=0.5)
axes[1].set_xlim((0, 1350))
axes[1].invert_yaxis()
# BIAGMACS untuned ArAr
axes[1].plot(stack_untuned_ArAr_age, stack['mean(permil)'], label='BIGMACS untuned ArAr', alpha=0.8, color='C0')

# BIAGMACS untuned
axes[1].plot(stack_untuned_age, stack['mean(permil)'], label='BIGMACS untuned', alpha=0.8, color='dodgerblue')

# axes[1].fill_between(stack_untuned_age,
#                   stack['mean(permil)']+2*stack['sigma(permil)'],
#                   stack['mean(permil)']-2*stack['sigma(permil)'],
#                   alpha=0.3,
#                   label='BIGMACS 2sigma',
#                   color='C0')

# BIGMACS intermediate tuned
# axes[1].plot(tuned_stack['X1'], tuned_stack['X2'], label='BIGMACS intermediate tuned', alpha=0.8, color='dodgerblue')

# BIGMACS full tuned
# axes[1].plot(tuned_stack['X1']+2.2, tuned_stack['X2'], label='BIGMACS full tuned', alpha=0.8, color='olivedrab')

axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[1].set_ylim(bottom=5.7)

# # BIGMACS
# l1 = axes[3].plot(stack.index, stack['mean(permil)'], label='BIGMACS', alpha=0.8, color='C4')
# axes[3].fill_between(stack.index,
#                   stack['mean(permil)']+2*stack['sigma(permil)'],
#                   stack['mean(permil)']-2*stack['sigma(permil)'],
#                   alpha=0.3,
#                   label='BIGMACS 2sigma',
#                   color='C4')
# LR04
l1 = axes[3].plot(LR04.index/1000, LR04, label='LR04', color='k', zorder=1, alpha=0.5)
# # ProbStack
# l3 = axes[3].plot(ProbStack.index/1000, ProbStack, label='ProbStack', color='C3', zorder=1, alpha=0.5)
axes[3].set_xlim((1350, 2700))
axes[3].invert_yaxis()
# BIGMACS untuned ArAr
l2 = axes[3].plot(stack_untuned_ArAr_age, stack['mean(permil)'], label=r'$\mathrm{BIGMACS}_\mathrm{magrev}$ ArAr', alpha=0.8, color='C0')

# BIAGMACS untuned
l3 = axes[3].plot(stack_untuned_age, stack['mean(permil)'], label=r'$\mathrm{BIGMACS}_\mathrm{magrev}$', alpha=0.8, color='dodgerblue')
# axes[3].fill_between(stack_untuned_age,
#                   stack['mean(permil)']+2*stack['sigma(permil)'],
#                   stack['mean(permil)']-2*stack['sigma(permil)'],
#                   alpha=0.3,
#                   label='BIGMACS 2sigma',
#                   color='C0')

# BIGMACS intermediate tuned
# l3 = axes[3].plot(tuned_stack['X1'], tuned_stack['X2'], label='BIGMACS tuned', alpha=0.8, color='dodgerblue')

# BIGMACS full tuned
# l4 = axes[3].plot(tuned_stack['X1']+2.2, tuned_stack['X2'], label='BIGMACS tuned', alpha=0.8, color='olivedrab')

axes[3].legend(handles=[l1[0], l2[0], l3[0]], ncol=3, loc=[0.1,0.11])

axes[3].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[3].set_xlabel('Age (ka BP)')
axes[3].set_ylim(bottom=5)

fig.set_size_inches(10,8)

#%% plot geomagnetic chrons
# upper panel
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
axes[1].text(880, y_lim_bottom-bar_height/2, 'Matuyama',
             horizontalalignment='center',
             verticalalignment='center',
             color='k')
axes[1].text(1282.5, y_lim_bottom-bar_height/2, 'Matuyama',
             horizontalalignment='center',
             verticalalignment='center',
             color='k')
# Jaramillo
axes[1].add_patch(patches.Rectangle((990, y_lim_bottom-bar_height),
                                    80,
                                    bar_height,
                                    facecolor='k',
                                    edgecolor='k'))
# Cobb Mountain
axes[1].add_patch(patches.Rectangle((1180, y_lim_bottom-bar_height),
                                    35,
                                    bar_height,
                                    facecolor='k',
                                    edgecolor='k'))

# lower panel
y_lim_bottom = axes[3].get_ylim()[0]
bar_height = 0.23 # a shorter bar height cuz plot is broader
axes[3].add_patch(patches.Rectangle((1350, y_lim_bottom-bar_height),
                                    2595-1350,
                                    bar_height,
                                    facecolor='None',
                                    edgecolor='k'))
axes[3].text(1562.5, y_lim_bottom-bar_height/2, 'Matuyama',
             horizontalalignment='center',
             verticalalignment='center',
             color='k')
axes[3].text(2350, y_lim_bottom-bar_height/2, 'Matuyama',
             horizontalalignment='center',
             verticalalignment='center',
             color='k')
# Olduvai
axes[3].add_patch(patches.Rectangle((1775, y_lim_bottom-bar_height),
                                    159,
                                    bar_height,
                                    facecolor='k',
                                    edgecolor='k'))
# Reunion
axes[3].add_patch(patches.Rectangle((2116, y_lim_bottom-bar_height),
                                    24,
                                    bar_height,
                                    facecolor='k',
                                    edgecolor='k'))

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

#%% beautification
# for i in range(0,3):
#     axes[i].xaxis.set_ticks_position('none')
#     axes[i].xaxis.set_ticklabels([])
    
axes[0].set_ylabel('65°N'
                   '\n'
                   'summer'
                   '\n'
                   r'(W/$\mathrm{m}^\mathrm{2}$')
axes[0].xaxis.tick_top()

# axes[1].yaxis.set_label_position("right")

axes[2].plot(insolation.index, insolation, color='C1')
axes[2].set_xlim((1350, 2700))
axes[2].set_ylabel('65°N'
                   '\n'
                   'summer'
                   '\n'
                   r'(W/$\mathrm{m}^\mathrm{2}$')

# axes[3].yaxis.set_label_position("right")

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
# plt.savefig('LR04_magrev_magrev_ArAr_comparison.png', dpi=700)
# plt.savefig('Untuned_results_mean_exclusion_expanded_1172_removed_GTS2012_Hobart2023.png', dpi=700)
# plt.savefig('Stitched_stack_LR04_insolation_untuned_no_compaction_corx.pdf')
# plt.savefig('Stitched_neptune_stack_LR04_insolation_ProbStack.pdf')
