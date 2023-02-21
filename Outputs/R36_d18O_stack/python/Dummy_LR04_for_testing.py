#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 23:12:54 2023

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../../Work/Lorraine/LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
# import scipy.io
from matplotlib import gridspec
import numpy as np

sns.set(font='Arial',palette='husl',style='whitegrid',context='paper')

input_1_path = '../../../Inputs/R34/Records/Record 1/d18O_data.txt'
input_1 = pd.read_table(input_1_path, delimiter='\t')
input_1.set_index('Depth', inplace=True)

input_2_path = '../../../Inputs/R34/Records/Record 2/d18O_data.txt'
input_2 = pd.read_table(input_2_path, delimiter='\t')
input_2.set_index('Depth', inplace=True)

input_3_path = '../../../Inputs/R34/Records/Record 3/d18O_data.txt'
input_3 = pd.read_table(input_3_path, delimiter='\t')
input_3.set_index('Depth', inplace=True)

input_4_path = '../../../Inputs/R34/Records/Record 4/d18O_data.txt'
input_4 = pd.read_table(input_4_path, delimiter='\t')
input_4.set_index('Depth', inplace=True)

input_5_path = '../../../Inputs/R34/Records/Record 5/d18O_data.txt'
input_5 = pd.read_table(input_5_path, delimiter='\t')
input_5.set_index('Depth', inplace=True)

stack_1_path = '../../R34_d18O_stack/stack.txt'
stack_1 = pd.read_table(stack_1_path, delimiter=' ')
stack_1.set_index('age(kyr)', inplace=True)

stack_2_path = '../../R35_d18O_stack/stack.txt'
stack_2 = pd.read_table(stack_2_path, delimiter=' ')
stack_2.set_index('age(kyr)', inplace=True)

stack_3_path = '../../R36_d18O_stack/stack.txt'
stack_3 = pd.read_table(stack_3_path, delimiter=' ')
stack_3.set_index('age(kyr)', inplace=True)

LR04 = LR04_fetching_func.fetch_d18O()

#%% plot
fig, axes = plt.subplots(4, 1, sharex=True)
# plot input
axes[0].plot(input_1.index, input_1['d18O'])
axes[0].plot(input_2.index, input_2['d18O'])
axes[0].plot(input_3.index, input_3['d18O'])
axes[0].plot(input_4.index, input_4['d18O'])
axes[0].plot(input_5.index, input_5['d18O'])
# plot input average
axes[1].plot(input_1.index, np.repeat(input_1['d18O'].mean(), len(input_1)))
axes[1].plot(input_2.index, np.repeat(input_2['d18O'].mean(), len(input_2)))
axes[1].plot(input_3.index, np.repeat(input_3['d18O'].mean(), len(input_3)))
axes[1].plot(input_4.index, np.repeat(input_4['d18O'].mean(), len(input_4)))
axes[1].plot(input_5.index, np.repeat(input_5['d18O'].mean(), len(input_5)))

# plot stacks
axes[2].plot(stack_1.index, stack_1['mean(permil)'], label='', linestyle='--', color='r')
axes[2].plot(stack_2.index, stack_2['mean(permil)'], label='', linestyle='dotted', color='g')
axes[2].plot(stack_3.index, stack_3['mean(permil)'], label='', linestyle='dashdot', color='b')
axes[2].plot(LR04.index/1000, LR04, label='LRO4', color='k', zorder=1)
# plot stack average
axes[3].plot(stack_1.index, np.repeat(stack_1['mean(permil)'].mean(), len(stack_1)), label='', linestyle='--', color='r')
axes[3].plot(stack_2.index, np.repeat(stack_2['mean(permil)'].mean(), len(stack_2)), label='', linestyle='dotted', color='g')
axes[3].plot(stack_3.index, np.repeat(stack_3['mean(permil)'].mean(), len(stack_3)), label='', linestyle='dashdot', color='b')
axes[3].plot(LR04[0:400].index/1000, np.repeat(LR04[0:400].mean(), len(LR04[0:400])), label='LRO4', color='k', zorder=1)

#%% beautification
axes[2].set_xlim((0, 400))
axes[3].set_xlabel('Age (ka)')
for i in range(4):
    axes[i].invert_yaxis()
    axes[i].set_ylabel(u'$\mathrm{\delta}^\mathrm{18}$O (‰)')
    
axes[0].text(0.1,0.8,'Raw input', transform=axes[0].transAxes)
axes[1].text(0.1,0.8,'Input average', transform=axes[1].transAxes)
axes[2].text(0.1,0.8,'Raw output', transform=axes[2].transAxes)
axes[3].text(0.1,0.8,'Output average', transform=axes[3].transAxes)
# plt.ylim(bottom=5.7)

plt.savefig('Dummy_LR04_for_testing.png', dpi=500)
# plt.savefig('Dummy_LR04_for_testing.pdf')
