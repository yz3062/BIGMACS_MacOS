#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 13:07:13 2024

@author: zhou
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set(font='Arial',palette='husl',style='whitegrid',context='notebook')

stack_df = pd.read_table('../stack.txt',delimiter=' ')
stack_target_df = pd.read_table('../stack_target.txt',delimiter='\t')
old_stack_df = pd.read_table('../../R98_d18O_stack/stack.txt', delimiter=' ')

fig, ax = plt.subplots(1,1)
stack_df.plot(x='age(kyr)', y='mean(permil)', ax=ax, label='BIGMACS stack')
stack_target_df.plot(x='Time (ka)', y='Benthic d18O (per mil)', ax=ax, label='New target')
old_stack_df.plot(x='age(kyr)', y='mean(permil)', ax=ax, label='old BIGMACS stack')
ax.invert_yaxis()
ax.set_xlim(0, 150)

plt.savefig('Quick_plot.png', dpi=700)