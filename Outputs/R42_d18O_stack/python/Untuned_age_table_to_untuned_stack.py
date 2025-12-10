#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 01:54:09 2025

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

# read untuned ages
untuned_df = pd.read_excel('Untuned_results_mean_exclusion_expanded_1172_removed_ArAr_Reunion.xlsx')
# ignore reversals
untuned_df = untuned_df[untuned_df['Reversal']!='y']

stack_untuned_age = age_model_interp(untuned_df['Old age'],
                               untuned_df['New age'],
                               stack.index)

#%% If noninterp version is desired, use the following section
# sigma doesn't represent the untuned uncertainty
# but it'll be used for the BIGSTACK_mixed uncertainty (also not true but will be noted)
# stack_untuned_df = pd.DataFrame(data={'Age': stack_untuned_age,
#                                       'd18O': stack['mean(permil)'],
#                                       'sigma': stack['sigma(permil)']})
# stack_untuned_df.to_csv('../R/Stack_untuned_uniform_age_exclusion_expanded_1172_removed_ArAr_Reunion.csv', index=False)

#%% If interp for auto tuning, use the following section
d18O_interp = age_model_interp(stack_untuned_age,
                                stack['mean(permil)'],
                                stack.index)

d18O_sigma_interp = age_model_interp(stack_untuned_age,
                                stack['sigma(permil)'],
                                stack.index)

stack_untuned_df = pd.DataFrame(data={'Age': stack.index,
                                      'd18O': d18O_interp})
                                      # 'sigma': d18O_sigma_interp})
stack_untuned_df.to_csv('../R/Stack_untuned_uniform_age_exclusion_expanded_1172_removed_ArAr_Reunion.csv', index=False)