#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 20:59:53 2022

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../../Work/McManus/HMM-Stack-master/python")
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

ProbStack = Probstack_fetching_func.fetch_d18O_std()

# limit data temporal range
stack = stack[stack.index<2700]
ProbStack = ProbStack[ProbStack.index<2700000]

#%% calculate average sigma
print(stack['sigma(permil)'].mean())
print(ProbStack.mean())