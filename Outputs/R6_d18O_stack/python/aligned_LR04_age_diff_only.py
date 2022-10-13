#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 18:26:10 2022

@author: zhou
"""

import pandas as pd
import sys
sys.path.append("../../../../LR04/python")
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
original_path = '../../../../../Work/Lorraine/Stacking/Stack/LR04'

for file in txtFilenamesList:
    aligned_df = pd.read_table(file, delimiter=' ')
    aligned_df.set_index('depth(m)',inplace=True)
    
    # find the open the original file
    head_tail = os.path.split(file) # tail [1] is the file name without path
    original_file = os.path.join(original_path, head_tail[1])
    original_df = pd.read_table(original_file, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])

    # calculate diff
    diff = aligned_df['median(kyr)'] - original_df.set_index('Depth (mcd)')['Age (ka)']
    diff.dropna(inplace=True)
    
    # interp from depth to age
    diff_LR04_age = age_model_interp(original_df['Depth (mcd)'],
                                     original_df['Age (ka)'],
                                     diff.index)
    
    if diff.abs().max() > 70:
        plt.plot(diff_LR04_age, diff, '-',
                 label=head_tail[1])
    else:
        plt.plot(diff_LR04_age, diff, '-',color='k')

plt.legend()
plt.ylabel('LR04 and new stack age difference (kyr)')
plt.xlabel('Age (ka)')

plt.savefig('aligned_LR04_age_diff_only.png', dpi=500)