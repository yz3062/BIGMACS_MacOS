#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 01:39:32 2022

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../../Work/Lorraine/LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import scipy.io

from scipy import interpolate

def age_model_interp(dated_depths, dated_ages, all_depths):
    f = interpolate.interp1d(dated_depths, dated_ages, fill_value='extrapolate')
    all_ages = f(all_depths)
    return all_ages

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

#%% plot
fig, axes = plt.subplots(2,1, sharex=False, sharey=False)

axes[0].plot(stack.index, stack['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[0].fill_between(stack.index,
                  stack['mean(permil)']+2*stack['sigma(permil)'],
                  stack['mean(permil)']-2*stack['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[0].plot(LR04.index/1000, LR04, label='LRO4', color='k', zorder=1, alpha=0.5)
axes[0].set_xlim((0, 1350))
axes[0].invert_yaxis()

axes[0].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[0].set_ylim(bottom=5.7)

axes[1].plot(stack.index, stack['mean(permil)'], label='BIGMACS', alpha=0.8)
axes[1].fill_between(stack.index,
                  stack['mean(permil)']+2*stack['sigma(permil)'],
                  stack['mean(permil)']-2*stack['sigma(permil)'],
                  alpha=0.3,
                  label='BIGMACS 2sigma')

axes[1].plot(LR04.index/1000, LR04, label='LRO4', color='k', zorder=1, alpha=0.5)
axes[1].set_xlim((1350, 2700))
axes[1].invert_yaxis()

# axes.legend()

axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[1].set_xlabel('Age (ka BP)')
axes[1].set_ylim(bottom=5)

fig.set_size_inches(10,8)

#%% plot geomagnetic chrons
bar_height = 0.25
y_lim_bottom = axes[0].get_ylim()[0]
axes[0].add_patch(patches.Rectangle((0, y_lim_bottom-bar_height),
                                    773,
                                    bar_height,
                                    facecolor='k',
                                    edgecolor='k'))
axes[0].text(773/2, y_lim_bottom-0.125, 'Brunhes',
             horizontalalignment='center',
             verticalalignment='center',
             color='w')
axes[0].add_patch(patches.Rectangle((773, y_lim_bottom-bar_height),
                                    1350-773,
                                    bar_height,
                                    facecolor='None',
                                    edgecolor='k'))
axes[0].text((1350+773)/2, y_lim_bottom-0.125, 'Matuyama',
             horizontalalignment='center',
             verticalalignment='center',
             color='k')
y_lim_bottom = axes[1].get_ylim()[0]
axes[1].add_patch(patches.Rectangle((1350, y_lim_bottom-bar_height),
                                    2595-1350,
                                    bar_height,
                                    facecolor='None',
                                    edgecolor='k'))
axes[1].text((2595+1350)/2, y_lim_bottom-0.125, 'Matuyama',
             horizontalalignment='center',
             verticalalignment='center',
             color='k')
axes[1].add_patch(patches.Rectangle((2595, y_lim_bottom-bar_height),
                                    2700-2595,
                                    bar_height,
                                    facecolor='k',
                                    edgecolor='k'))
axes[1].text((2700+2595)/2, y_lim_bottom-0.125, 'Gauss',
              horizontalalignment='center',
              verticalalignment='center',
              color='w')
# axes[0].add_patch(patches.Rectangle((1215, y_lim_bottom-bar_height),
#                                     1350-1215,
#                                     bar_height,
#                                     facecolor='k',
#                                     edgecolor='k'))
# axes[0].text((1350+1215)/2, y_lim_bottom-0.125, 'Cobb Mountain',
#              horizontalalignment='center',
#              verticalalignment='center',
#              color='w',
#              fontsize=8)
# axes[1].add_patch(patches.Rectangle((1350, y_lim_bottom-bar_height),
#                                     1770-1350,
#                                     bar_height,
#                                     facecolor='k',
#                                     edgecolor='k'))
# axes[1].text((1770+1350)/2, y_lim_bottom-0.125, 'Cobb Mountain',
#              horizontalalignment='center',
#              verticalalignment='center',
#              color='w')
# axes[1].add_patch(patches.Rectangle((1770, y_lim_bottom-bar_height),
#                                     1925-1770,
#                                     bar_height,
#                                     facecolor='None',
#                                     edgecolor='k'))
# # axes[1].text((1925+1770)/2, y_lim_bottom-0.125, 'C1r.3r',
# #              horizontalalignment='center',
# #              verticalalignment='center',
# #              color='w')
# axes[1].add_patch(patches.Rectangle((1925, y_lim_bottom-bar_height),
#                                     2125-1925,
#                                     bar_height,
#                                     facecolor='k',
#                                     edgecolor='k'))
# axes[1].text((2125+1925)/2, y_lim_bottom-0.125, 'Olduvair',
#              horizontalalignment='center',
#              verticalalignment='center',
#              color='white')
# axes[1].add_patch(patches.Rectangle((2125, y_lim_bottom-bar_height),
#                                     2595-2125,
#                                     bar_height,
#                                     facecolor='None',
#                                     edgecolor='k'))
# # axes[1].text((2595+2125)/2, y_lim_bottom-0.125, 'C2r.1n-C2r.1r',
# #              horizontalalignment='center',
# #              verticalalignment='center',
# #              color='w')
# axes[1].add_patch(patches.Rectangle((2125, y_lim_bottom-bar_height),
#                                     2595-2125,
#                                     bar_height,
#                                     facecolor='None',
#                                     edgecolor='k'))
# axes[1].text((2125+1925)/2, y_lim_bottom-0.125, 'Feni',
#              horizontalalignment='center',
#              verticalalignment='center',
#              color='white')
# axes[1].add_patch(patches.Rectangle((2595, y_lim_bottom-bar_height),
#                                     2700-2595,
#                                     bar_height,
#                                     facecolor='k',
#                                     edgecolor='k'))
# axes[1].text((2700+2595)/2, y_lim_bottom-0.125, 'Matuyama',
#              horizontalalignment='center',
#              verticalalignment='center',
#              color='w',
#              fontsize=8)
plt.savefig('Stitched_stack_LR04.png', dpi=500)
# plt.savefig('Stitched_stack_LR04.pdf')

