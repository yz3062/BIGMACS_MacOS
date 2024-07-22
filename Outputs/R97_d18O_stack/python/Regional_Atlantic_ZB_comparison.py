#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 19:11:00 2024

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../../Work/Lorraine/LR04/python")
sys.path.append("../../../../../Work/McManus/HMM-Stack-master/python")
import LR04_fetching_func
import Probstack_fetching_func
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
# import scipy.io
from matplotlib import gridspec
from scipy import interpolate
import numpy as np
import matplotlib

sns.set(font='Arial',palette='husl',style='whitegrid',context='notebook')

def shade(fig,axes,left_x,right_x, color='lightgray'):
    # the following code will shade HEs
    # 1. Get transformation operators for axis and figure
    top_axtr = axes[0].transData # Axis top -> Display
    bottom_axtr = axes[-1].transData # Axis bottom -> Display
    figtr = fig.transFigure.inverted() # Display -> Figure
    # 2. Transform points from axis to figure coordinates
    shade_lower_limit = axes[-1].viewLim.get_points()[0][1] # lower ylim in lowest axis
    shade_upper_limit = axes[0].viewLim.get_points()[1][1] # upper ylim in highest axis
    lower_left = figtr.transform(bottom_axtr.transform((left_x, shade_lower_limit)))
    lower_right = figtr.transform(bottom_axtr.transform((right_x, shade_lower_limit)))
    upper_left = figtr.transform(top_axtr.transform((left_x, shade_upper_limit)))
    upper_right = figtr.transform(top_axtr.transform((right_x, shade_upper_limit)))
    # 4. Create the patch
    rect = matplotlib.patches.Polygon([lower_left,lower_right,upper_right,upper_left], transform=fig.transFigure,color=color)
    fig.patches.append(rect)

# read regional stacks
Pacific_stack_path = '../../R86_d18O_stack/stack.txt'
# stack = scipy.io.loadmat(stack_path)
Pacific_stack = pd.read_table(Pacific_stack_path, delimiter=' ')

Atlantic_stack_path = '../../R97_d18O_stack/stack.txt'
# stack = scipy.io.loadmat(stack_path)
Atlantic_stack = pd.read_table(Atlantic_stack_path, delimiter=' ')

# fetch insolation # needs to be updated by ZB
insolation_65N = pd.read_excel('../../../../../Work/Lorraine/Zeebe orbital solutions/ZB_insolation_from_website_65N.xlsx')
insolation_65S = pd.read_excel('../../../../../Work/Lorraine/Zeebe orbital solutions/ZB_insolation_from_website_65S.xlsx')

# read QAnalySeries hand tuned stack
hand_tuned_stack = pd.read_table('../../../../../Work/Lorraine/Hand tuning/Tuning results fewer tie points 1819/Data_with_ages.txt',
                                 delimiter=' ')
hand_tuned_stack['Value'] = hand_tuned_stack['Value'] * -1

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
    tuned_cut_duration = (tuned_stack.iloc[tuned_cut_end] - tuned_stack.iloc[tuned_cut_start])['Age']
    # for this method to work, regional stack must be regularly spaced
    regional_cut_new_age = np.linspace(tuned_stack.iloc[tuned_cut_start]['Age'],
                                       tuned_stack.iloc[tuned_cut_end-1]['Age'],
                                       num=regional_cut_len)
    regional_cut_df_data = {'Age': regional_cut_new_age, 'Value': regional_stack_cut['mean(permil)']}
    regional_cut_df = pd.DataFrame(data=regional_cut_df_data)
    # paste in
    tuned_stack_paste = pd.concat([tuned_stack_cut, regional_cut_df])
    # sort
    tuned_stack_paste.sort_values(by='Age', inplace=True)
    return tuned_stack_paste

# the following four are indexes of the glacials around 1.8 and 1.9 Ma
tuned_cut_start = 1789 # correspond to age of 1793 ka
tuned_cut_end = 1901 # correspond to age of 1913 ka
regional_cut_start = 313
regional_cut_end = 423
# do Pacific
Pacific_stack_paste_in = regional_paste_in(tuned_cut_start, tuned_cut_end, regional_cut_start,
                                           regional_cut_end, hand_tuned_stack, Pacific_stack)
# Pacific_stack_paste_in_segment = Pacific_stack_paste_in[(Pacific_stack_paste_in['X1']>1787) &
#                                                           (Pacific_stack_paste_in['X1']<1896)]

# the following four are indexes of the glacials around 1.8 and 1.9 Ma
tuned_cut_start = 1789 # correspond to age of 1793 ka
tuned_cut_end = 1901 # correspond to age of 1913 ka
regional_cut_start = 315
regional_cut_end = 424
# do Atlantic
Atlantic_stack_paste_in = regional_paste_in(tuned_cut_start, tuned_cut_end, regional_cut_start,
                                           regional_cut_end, hand_tuned_stack, Atlantic_stack)
# Atlantic_stack_paste_in_segment = Atlantic_stack_paste_in[(Atlantic_stack_paste_in['X1']>1787) &
#                                                           (Atlantic_stack_paste_in['X1']<1896)]

#%% plot
fig, axes = plt.subplots(3,1, sharex=True, sharey=False)
plt.subplots_adjust(hspace=0)

axes[1].set_xlim((1500, 2100))
axes[1].set_ylim((3.2, 4.3))
axes[1].invert_yaxis()

# Atlantic paste in
axes[1].plot(Atlantic_stack_paste_in['Age'], Atlantic_stack_paste_in['Value'], label='Atlantic', alpha=0.5, color='C5')

# Pacific paste in
axes[1].plot(Pacific_stack_paste_in['Age'], Pacific_stack_paste_in['Value'], label='Pacific', alpha=0.5, color='C4')

axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')


fig.set_size_inches(10,8)

#%% plot Milankovitch
axes[0].plot(insolation_65N['% Time (kyr)'], insolation_65N['Insolation (W/m2)'], color='C5')
# axes[0].set_xlim((0, 1350))
axes[0].set_ylabel('65°N'
                   '\n'
                   'summer'
                   '\n'
                   r'(W/$\mathrm{m}^\mathrm{2}$')
axes[2].plot(insolation_65S['% Time (kyr)'], insolation_65S['Insolation (W/m2)'], color='C4')
# axes[2].set_xlim((1350, 2700))
axes[2].set_ylabel('65°S'
                   '\n'
                   'summer'
                   '\n'
                   r'(W/$\mathrm{m}^\mathrm{2}$')
# remove x axis
sns.despine(ax=axes[0], bottom=True)
sns.despine(ax=axes[1], bottom=True)
sns.despine(ax=axes[2], bottom=False)

shade(fig,axes,1863,1878, 'lightgray')
shade(fig,axes,1837,1842, 'lightgray')

for ax in axes:
    ax.set_zorder(10)
    ax.set_facecolor('none')
plt.savefig('Regional_Atlantic_ZB_comparison.png', dpi=700)
# plt.savefig('LR04_tuned_regional.pdf')
# plt.savefig('Untuned_results_mean_exclusion_expanded_1172_removed_GTS2012_Hobart2023.png', dpi=700)
# plt.savefig('Stitched_stack_LR04_insolation_untuned_no_compaction_corx.pdf')
# plt.savefig('Stitched_neptune_stack_LR04_insolation_ProbStack.pdf')