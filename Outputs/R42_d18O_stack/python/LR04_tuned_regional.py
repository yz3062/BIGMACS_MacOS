#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:44:48 2024

@author: zhou
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 11:33:56 2024

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
from scipy import interpolate
import numpy as np

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

# read regional stacks
Pacific_stack_path = '../../R86_d18O_stack/stack.txt'
# stack = scipy.io.loadmat(stack_path)
Pacific_stack = pd.read_table(Pacific_stack_path, delimiter=' ')

Atlantic_stack_path = '../../R87_d18O_stack/stack.txt'
# stack = scipy.io.loadmat(stack_path)
Atlantic_stack = pd.read_table(Atlantic_stack_path, delimiter=' ')

# read untuned ages
untuned_df = pd.read_excel('Untuned_results_mean_exclusion_expanded_1172_removed_Hobart2023.xlsx')
# ignore reversals
untuned_df = untuned_df[untuned_df['Reversal']!='y']

stack_untuned_age = age_model_interp(untuned_df['Old age'],
                               untuned_df['New age'],
                               stack.index)

LR04 = LR04_fetching_func.fetch_d18O()

insolation = Milankovitch_fetching_func.fetch_65N_summer_insolation()

# ProbStack = Probstack_fetching_func.fetch_d18O()

tuned_stack_win400 = pd.read_excel('../R/tuned_stack_unextrapolated.xlsx')
tuned_stack_win200 = pd.read_excel('../R/tuned_stack_unextrapolated_win200.xlsx')
tuned_stack_win150 = pd.read_excel('../R/tuned_stack_unextrapolated_win150.xlsx')

#%% pasting in data processing
# paste in
def regional_paste_in(tuned_cut_start, tuned_cut_end, regional_cut_start,
                      regional_cut_end, tuned_stack, regional_stack):

    # remove 1.8-1.9 Ma in tuned stack
    tuned_stack_cut = tuned_stack.drop(tuned_stack.index[tuned_cut_start:tuned_cut_end])
    # obtain Pacific 1.8-1.9 Ma
    regional_stack_cut = regional_stack.iloc[regional_cut_start:regional_cut_end]
    regional_cut_len = len(regional_stack_cut)
    regional_cut_duration = regional_stack_cut.iloc[-1]['age(kyr)'] - regional_stack_cut.iloc[0]['age(kyr)']
    tuned_cut_duration = (tuned_stack.iloc[tuned_cut_end] - tuned_stack.iloc[tuned_cut_start])['X1']
    # for this method to work, regional stack must be regularly spaced
    regional_cut_new_age = np.linspace(tuned_stack.iloc[tuned_cut_start]['X1'],
                                       tuned_stack.iloc[tuned_cut_end-1]['X1'],
                                       num=regional_cut_len)
    regional_cut_df_data = {'X1': regional_cut_new_age, 'X2': regional_stack_cut['mean(permil)']}
    regional_cut_df = pd.DataFrame(data=regional_cut_df_data)
    # paste in
    tuned_stack_paste = pd.concat([tuned_stack_cut, regional_cut_df])
    # sort
    tuned_stack_paste.sort_values(by='X1', inplace=True)
    return tuned_stack_paste

# the following four are indexes of the glacials around 1.8 and 1.9 Ma
tuned_cut_start = 1584
tuned_cut_end = 1693
regional_cut_start = 313
regional_cut_end = 424
# do Pacific
Pacific_stack_paste_in = regional_paste_in(tuned_cut_start, tuned_cut_end, regional_cut_start,
                                           regional_cut_end, tuned_stack_win400, Pacific_stack)
Pacific_stack_paste_in_segment = Pacific_stack_paste_in[(Pacific_stack_paste_in['X1']>1787) &
                                                          (Pacific_stack_paste_in['X1']<1896)]

# the following four are indexes of the glacials around 1.8 and 1.9 Ma
tuned_cut_start = 1584
tuned_cut_end = 1693
regional_cut_start = 314
regional_cut_end = 424
# do Atlantic
Atlantic_stack_paste_in = regional_paste_in(tuned_cut_start, tuned_cut_end, regional_cut_start,
                                           regional_cut_end, tuned_stack_win400, Atlantic_stack)
Atlantic_stack_paste_in_segment = Atlantic_stack_paste_in[(Atlantic_stack_paste_in['X1']>1787) &
                                                          (Atlantic_stack_paste_in['X1']<1896)]

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
# axes[1].plot(LR04.index/1000, LR04, label='LRO4', color='k', zorder=1, alpha=0.5)
# # ProbStack
# axes[1].plot(ProbStack.index/1000, ProbStack, label='ProbStack', color='C3', zorder=1, alpha=0.5)
axes[1].set_xlim((0, 1350))
axes[1].invert_yaxis()
# BIAGMACS untuned
# axes[1].plot(stack_untuned_age, stack['mean(permil)'], label='BIGMACS untuned', alpha=0.8, color='C0')
# axes[1].fill_between(stack_untuned_age,
#                   stack['mean(permil)']+2*stack['sigma(permil)'],
#                   stack['mean(permil)']-2*stack['sigma(permil)'],
#                   alpha=0.3,
#                   label='BIGMACS 2sigma',
#                   color='C0')

# Win=400kyr
# axes[1].plot(tuned_stack_win400['X1'], tuned_stack_win400['X2'], label='Win=400kyr', alpha=0.8, color='lightgray')

# Win=200kyr
# axes[1].plot(tuned_stack_win200['X1'], tuned_stack_win200['X2'], label='Win=200kyr', alpha=0.8, color='olivedrab')

# # Win=150kyr
# axes[1].plot(tuned_stack_win150['X1'], tuned_stack_win150['X2'], label='Win=150kyr', alpha=0.5, color='indigo')

# Pacific paste in
axes[1].plot(Pacific_stack_paste_in['X1'], Pacific_stack_paste_in['X2'], label='Pacific', alpha=0.5, color='C5')

# Atlantic paste in
axes[1].plot(Atlantic_stack_paste_in['X1'], Atlantic_stack_paste_in['X2'], label='Atlantic', alpha=0.5, color='C4')

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
# l1 = axes[3].plot(LR04.index/1000, LR04, label='LR04', color='k', zorder=1, alpha=0.5)
# # ProbStack
# l3 = axes[3].plot(ProbStack.index/1000, ProbStack, label='ProbStack', color='C3', zorder=1, alpha=0.5)
axes[3].set_xlim((1350, 2700))
axes[3].invert_yaxis()
# BIGMACS untuned
# l2 = axes[3].plot(stack_untuned_age, stack['mean(permil)'], label='BIGMACS untuned', alpha=0.8, color='C0')
# axes[3].fill_between(stack_untuned_age,
#                   stack['mean(permil)']+2*stack['sigma(permil)'],
#                   stack['mean(permil)']-2*stack['sigma(permil)'],
#                   alpha=0.3,
#                   label='BIGMACS 2sigma',
#                   color='C0')

# Win=400kyr
# l3 = axes[3].plot(tuned_stack_win400['X1'], tuned_stack_win400['X2'], label='Win=400kyr', alpha=0.8, color='lightgray')

# Win=200kyr
# l4 = axes[3].plot(tuned_stack_win200['X1'], tuned_stack_win200['X2'], label='Win=200kyr', alpha=0.8, color='olivedrab')

# # Win=150kyr
# l5 = axes[3].plot(tuned_stack_win150['X1'], tuned_stack_win150['X2'], label='Win=150kyr', alpha=0.5, color='indigo')

# Pacific paste in
axes[3].plot(Pacific_stack_paste_in['X1'], Pacific_stack_paste_in['X2'], label='Pacific', alpha=0.5, color='C5')

# Atlantic paste in
axes[3].plot(Atlantic_stack_paste_in['X1'], Atlantic_stack_paste_in['X2'], label='Atlantic', alpha=0.5, color='C4')

# axes[3].legend(handles=[l3[0], l4[0]], loc=[0.8,0.11])

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
# plt.savefig('LR04_tuned_regional.png', dpi=700)
# plt.savefig('LR04_tuned_regional.pdf')
# plt.savefig('Untuned_results_mean_exclusion_expanded_1172_removed_GTS2012_Hobart2023.png', dpi=700)
# plt.savefig('Stitched_stack_LR04_insolation_untuned_no_compaction_corx.pdf')
# plt.savefig('Stitched_neptune_stack_LR04_insolation_ProbStack.pdf')
