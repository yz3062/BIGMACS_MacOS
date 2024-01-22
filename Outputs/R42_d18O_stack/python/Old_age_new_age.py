#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 01:33:09 2023

@author: zhou
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font='Arial',palette='husl',style='whitegrid',context='notebook')

# read untuned ages
untuned_df = pd.read_excel('Untuned_results_mean_exclusion.xlsx')
# # ignore reversals
# untuned_df = untuned_df[untuned_df['Reversal']!='y']

#%% plot
plt.plot(untuned_df['Old age'], untuned_df['New age'], 'o',
         markersize=1)
plt.subplots_adjust(left=0.2)
plt.xlabel('Untuned age (ka)')
plt.ylabel('LR04 age (ka)')
plt.gcf().set_size_inches(5,5)

# plt.savefig('Old_age_new_age.png', dpi=700)
plt.savefig('Old_age_new_age.pdf')