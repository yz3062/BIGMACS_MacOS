#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 11:26:42 2023

@author: zhou
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 17:51:57 2023

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../../Work/Lorraine/LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import seaborn as sns
import pyleoclim as pyleo
import matplotlib

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

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

Pacific_stack_path = '../stack.txt'
# stack = scipy.io.loadmat(stack_path)
Pacific_stack = pd.read_table(Pacific_stack_path, delimiter=' ')

Atlantic_stack_path = '../../R62_d18O_stack/stack.txt'
# stack = scipy.io.loadmat(stack_path)
Atlantic_stack = pd.read_table(Atlantic_stack_path, delimiter=' ')

LR04 = LR04_fetching_func.fetch_d18O()

#%% figure set up
fig, axes = plt.subplots(3,1, sharex=True)
plt.subplots_adjust(hspace=-0.3)

#%% NH inso
inso_summer_65N = pd.read_table('../../../../../Work/McManus/Milankovitch/python/inso_summer_65N.txt',
                                delimiter=' ',
                                names=['age', 'NH inso.'])
inso_summer_65N.set_index('age', inplace=True)

inso_summer_65N.plot(label='65° N insolation', ax=axes[0], color='C5')
# axes[0].yaxis.set_label_position("right")
# axes[0].yaxis.label.set_color('C5')
# axes[0].spines['right'].set_color('C5')
# axes[0].tick_params(axis='y', colors='C5')
axes[0].legend(loc='upper right')

#%% SH inso
inso_summer_65S = pd.read_table('../../../../../Work/McManus/Milankovitch/python/inso_summer_65S.txt',
                                delimiter=' ',
                                names=['age', 'SH inso.'])
inso_summer_65S.set_index('age', inplace=True)

inso_summer_65S.plot(label='SH inso.', ax=axes[2], color='C4')
# axes[2].yaxis.set_label_position("right")
# axes[2].yaxis.label.set_color('C4')
# axes[2].spines['right'].set_color('C4')
# axes[2].tick_params(axis='y', colors='C4')
axes[2].legend(loc='lower right')

#%% plot stacks

axes[1].plot(Pacific_stack['age(kyr)'], Pacific_stack['mean(permil)'],
             label='Pacific, target: 677', color='C4')
axes[1].plot(Atlantic_stack['age(kyr)'], Atlantic_stack['mean(permil)'],
             label='Atlantic, target: 1308', color='C5')
axes[1].yaxis.set_label_position("right")
axes[1].yaxis.label.set_color('k')
axes[1].spines['right'].set_color('k')
axes[1].tick_params(axis='y', colors='k')
axes[1].legend(loc='lower right')
# axes.fill_between(stack['age(kyr)'],
#                   stack['mean(permil)']+2*stack['sigma(permil)'],
#                   stack['mean(permil)']-2*stack['sigma(permil)'],
#                   alpha=0.3,
#                   label='BIGMACS 2sigma')

#%% beautification
# axes.plot(LR04.index/1000, LR04, label='LRO4', color='k')
axes[0].set_xlabel('')
axes[1].set_xlabel('')

axes[2].set_xlim((1500, 2100))
axes[1].invert_yaxis()

# axes.axvspan(1800, 1900, color='lightgray')

axes[1].legend(loc='lower right')

axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[2].set_xlabel('Age (ka BP)')

sns.despine(ax=axes[0], top=True,right=True, left=False, bottom=True)
sns.despine(ax=axes[1], top=True,right=False, left=True, bottom=True)
sns.despine(ax=axes[2], top=True,right=True, left=False, bottom=False)

for i in range(2):
    axes[i].xaxis.set_ticks_position('none')

shade(fig,axes,1800,1900, 'lightgray')
# shade(fig,axes,1828,1838, 'lightblue')
# shade(fig,axes,1858,1870, 'lightblue')
# axes[2].axvspan(1828,1838, color='lightblue')
# axes[2].axvspan(1858,1870, color='lightblue')

# axes[0].axvspan(1832,1842, color='lightblue')
# axes[3].axvspan(1832,1842, color='lightblue')

# axes[0].axvspan(1862,1874, color='lightblue')
# axes[3].axvspan(1862,1874, color='lightblue')
    
for ax in axes:
    ax.set_zorder(10)
    ax.set_facecolor('none')

fig.set_size_inches(6,8)

# plt.savefig('Stack_inso_comparison.pdf')