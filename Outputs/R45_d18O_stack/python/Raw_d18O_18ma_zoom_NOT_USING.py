#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 22:30:25 2023

@author: zhou

"""

import pandas as pd
import sys
sys.path.append("../../../../../Work/Lorraine/LR04/python")
import LR04_fetching_func
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

from scipy import interpolate

def age_model_interp(dated_depths, dated_ages, all_depths):
    f = interpolate.interp1d(dated_depths, dated_ages, fill_value='extrapolate')
    all_ages = f(all_depths)
    return all_ages

sns.set(font='Arial',palette='husl',style='ticks',context='paper')

# The folder where new alignment by BIGMACS is made
aligned_path = '../ages/'
txtFilenamesList = glob.glob(aligned_path + '*.txt')

# Original age path
original_path = '../../../../../Work/Lorraine/Stacking/Stack/Merged'

for file in txtFilenamesList:
    aligned_df = pd.read_table(file, delimiter=' ')
    
    # find the open the original file
    head_tail = os.path.split(file) # tail [1] is the file name without path

    # open original file
    original_file = os.path.join(original_path, head_tail[1])
    original_df = pd.read_table(original_file, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])  

    # trim original to temporal range of alighed
    original_df = original_df[(original_df['Depth (mcd)'] >= aligned_df['depth(m)'].iloc[0])
                              & (original_df['Depth (mcd)'] <= aligned_df['depth(m)'].iloc[-1])]

    # set BIGMACS ages as index of record
    aligned_age_df = original_df.set_index(aligned_df['mean(kyr)'])
    
    # plot
    plt.plot(aligned_age_df.index, aligned_age_df['d18O'])

plt.ylabel('d18O')
plt.xlabel('Age (ka)')

# plt.savefig('aligned_LR04_age_diff_only.png', dpi=500)