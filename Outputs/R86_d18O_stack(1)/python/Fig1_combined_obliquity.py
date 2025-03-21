#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 19:00:13 2024

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../../Work/Lorraine/LR04/python")
sys.path.append("../../../../../Work/Lorraine/CENOGRID")
sys.path.append("../../../../../Work/McManus/HMM-Stack-master/python")
import LR04_fetching_func
import Probstack_fetching_func
import CENOGRID_fetching_func
import matplotlib.pyplot as plt
import seaborn as sns
# import pyleoclim as pyleo
import matplotlib

sns.set(font='Helvetica',palette='husl',style='ticks',context='paper')

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

Pacific_stack_path = '../../R86_d18O_stack/stack.txt'
# stack = scipy.io.loadmat(stack_path)
Pacific_stack = pd.read_table(Pacific_stack_path, delimiter=' ')

Atlantic_stack_path = '../../R87_d18O_stack/stack.txt'
# stack = scipy.io.loadmat(stack_path)
Atlantic_stack = pd.read_table(Atlantic_stack_path, delimiter=' ')

LR04 = LR04_fetching_func.fetch_d18O()

ProbStack = Probstack_fetching_func.fetch_d18O()
ProbStack_upper = Probstack_fetching_func.fetch_d18O_upper()
ProbStack_lower = Probstack_fetching_func.fetch_d18O_lower()

CENOGRID = CENOGRID_fetching_func.fetch_d18O()

#%% figure set up
fig, axes = plt.subplots(7,1, sharex=True)
plt.subplots_adjust(hspace=-0.2)

#%% NH inso
inso_summer_65N = pd.read_table('../../../../../Work/McManus/Milankovitch/python/inso_summer_65N.txt',
                                delimiter=' ',
                                names=['age', 'NH inso.'])
inso_summer_65N.set_index('age', inplace=True)

inso_summer_65N.plot(label='65° N insolation', ax=axes[4], color='C5', legend=False)

#%% SH inso
inso_summer_65S = pd.read_table('../../../../../Work/McManus/Milankovitch/python/inso_summer_65S.txt',
                                delimiter=' ',
                                names=['age', 'SH inso.'])
inso_summer_65S.set_index('age', inplace=True)

inso_summer_65S.plot(label='65° S insolation', ax=axes[6], color='C4', legend=False)

#%% obliquity
obl = pd.read_excel('../../../../../Work/McManus/Milankovitch/Insolation calculation_LR04.xlsx',
                    sheet_name='Sheet1')
obl.set_index('time', inplace=True)
# axes[4].plot(obl.index, obl['obliquity'], color='k')
# axes[4].set_ylabel('Obliquity (°)')
axes[5].plot(obl.index, obl['obliquity'], color='k')

#%% plot CENOGRID
axes[0].plot(CENOGRID.index*1000, CENOGRID, color='k', label='CENOGRID')

#%% plot LR04
axes[1].plot(LR04.index/1000, LR04, color='k', label='LR04')

#%% plot ProbStack
axes[2].plot(ProbStack.index/1000, ProbStack, color='C3', alpha=0.3,
             label='ProbStack')
axes[2].fill_between(ProbStack.index/1000,
                     ProbStack_upper,
                     ProbStack_lower,
                     alpha=0.3,
                     color='C3')

#%% plot stacks

axes[3].plot(Pacific_stack['age(kyr)'], Pacific_stack['mean(permil)'],
             label='Pacific stack', color='C4')
axes[3].fill_between(Pacific_stack['age(kyr)'],
                  Pacific_stack['mean(permil)']+Pacific_stack['sigma(permil)'],
                  Pacific_stack['mean(permil)']-Pacific_stack['sigma(permil)'],
                  alpha=0.3,
                  color='C4')
axes[3].plot(Atlantic_stack['age(kyr)'], Atlantic_stack['mean(permil)'],
             label='Atlantic stack', color='C5')
axes[3].fill_between(Atlantic_stack['age(kyr)'],
                  Atlantic_stack['mean(permil)']+Atlantic_stack['sigma(permil)'],
                  Atlantic_stack['mean(permil)']-Atlantic_stack['sigma(permil)'],
                  alpha=0.3,
                  color='C5')
axes[3].set_ylim(3.15, 4.4)
# axes[2].plot(LR04.index/1000, LR04, color='k', alpha=0.3)

# axes.fill_between(stack['age(kyr)'],
#                   stack['mean(permil)']+2*stack['sigma(permil)'],
#                   stack['mean(permil)']-2*stack['sigma(permil)'],
#                   alpha=0.3,
#                   label='BIGMACS 2sigma')

#%% beautification

axes[0].set_xlim((1500, 2100))
axes[0].set_ylim(3, 5)
axes[0].invert_yaxis()
axes[0].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')

axes[1].set_ylim(3, 4.7)
axes[1].invert_yaxis()
axes[1].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[1].yaxis.set_label_position("right")

axes[2].set_ylim(3, 4.7)
axes[2].invert_yaxis()
axes[2].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')

axes[3].set_ylim(3.15, 4.4)
axes[3].invert_yaxis()
axes[3].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
axes[3].yaxis.set_label_position("right")

axes[4].set_xlabel('')
axes[4].set_ylabel(r'Insolation $W/{m^2}$')
# axes[4].yaxis.set_label_position("right")
axes[4].yaxis.label.set_color('C5')
axes[4].spines['left'].set_color('C5')
axes[4].tick_params(axis='y', colors='C5')
# axes[4].legend(loc='upper right', bbox_to_anchor=(1, 1))

axes[5].set_ylabel('Obliquity (°)')
axes[5].yaxis.set_label_position("right")

axes[6].set_xlabel('')
axes[6].set_ylabel(r'Insolation $W/{m^2}$')
# axes[6].yaxis.set_label_position("right")
axes[6].yaxis.label.set_color('C4')
axes[6].spines['left'].set_color('C4')
axes[6].tick_params(axis='y', colors='C4')
# axes[6].legend(loc='lower right', bbox_to_anchor=(1, 0))
axes[6].set_xlabel('Age (ka BP)')

# axes.axvspan(1800, 1900, color='lightgray')

sns.despine(ax=axes[0], top=True,right=True, left=False, bottom=True)
sns.despine(ax=axes[1], top=True,right=False, left=True, bottom=True)
sns.despine(ax=axes[2], top=True,right=True, left=False, bottom=True)
sns.despine(ax=axes[3], top=True,right=False, left=True, bottom=True)
sns.despine(ax=axes[4], top=True,right=True, left=False, bottom=True)
sns.despine(ax=axes[5], top=True,right=False, left=True, bottom=True)
sns.despine(ax=axes[6], top=True,right=True, left=False, bottom=False)

for i in range(6):
    axes[i].xaxis.set_ticks_position('none')

for i in range(7):
    axes[i].grid(axis='x', zorder=0)
    
pos = axes[2].get_position()
pos.y0 += 0.005
pos.y1 += 0.005
axes[2].set_position(pos)

pos = axes[5].get_position()
pos.y0 += 0.03
pos.y1 += 0.03
axes[5].set_position(pos)

pos = axes[6].get_position()
pos.y0 += 0.06
pos.y1 += 0.06
axes[6].set_position(pos)

shade(fig,axes,1863,1878, 'lightgray')
shade(fig,axes,1837,1842, 'lightgray')
# shade(fig,axes,1828,1838, 'lightblue')
# shade(fig,axes,1858,1870, 'lightblue')
# axes[2].axvspan(1828,1838, color='lightblue')
# axes[2].axvspan(1858,1870, color='lightblue')

# axes[0].axvspan(1832,1842, color='lightblue')
# axes[3].axvspan(1832,1842, color='lightblue')

# axes[0].axvspan(1862,1874, color='lightblue')
# axes[3].axvspan(1862,1874, color='lightblue')

# letters
axes[0].text(0.01, 0.8, 'A', transform=axes[0].transAxes, fontweight='bold', color='k')
axes[1].text(0.01, 0.7, 'B', transform=axes[1].transAxes, fontweight='bold', color='k')
axes[2].text(0.01, 0.8, 'C', transform=axes[2].transAxes, fontweight='bold', color='k')
axes[3].text(0.01, 0.8, 'D', transform=axes[3].transAxes, fontweight='bold', color='k')
axes[4].text(0.01, 0.6, 'E', transform=axes[4].transAxes, fontweight='bold', color='k')
axes[5].text(0.01, 0.7, 'F', transform=axes[5].transAxes, fontweight='bold', color='k')
axes[6].text(0.01, 0.6, 'G', transform=axes[6].transAxes, fontweight='bold', color='k')

# for ax in axes:
    # ax.axvline(1793, linestyle='dashed', color='gray', zorder=0)
    # ax.axvline(1837, linestyle='dashed', color='gray', zorder=0)
    # ax.axvline(1878, linestyle='dashed', color='gray', zorder=0)
    # ax.axvline(1958, linestyle='dashed', color='gray', zorder=0)
    # ax.axvline(2050, linestyle='dashed', color='gray', zorder=0)
    
for ax in axes:
    ax.set_zorder(10)
    ax.set_facecolor('none')

fig.set_size_inches(6,8)

plt.savefig('Fig1_combined_obliquity.pdf')
# plt.savefig('Stack_inso_comparison_shade.png', dpi=700)
# plt.savefig('Stack_inso_comparison_shade_poster.pdf')