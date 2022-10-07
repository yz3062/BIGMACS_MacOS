#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 15:16:55 2022

@author: zhou
"""


import pandas as pd
import sys
import matplotlib.pyplot as plt

ODP929_aligned_file_path = '../Outputs/Test_run_2my_2000_particle_d18O_OU_heteroscedastic/ages/ODP929.txt'
ODP929_aligned = pd.read_table(ODP929_aligned_file_path, delimiter=' ',)
ODP929_aligned.set_index('depth(m)',inplace=True)

ODP929_original_file_path = '../../Stacking/Stack/LR04/929_LR04age.txt'
ODP929_original = pd.read_table(ODP929_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])
ODP929_original.set_index('Depth (mcd)',inplace=True)

ODP846_aligned_file_path = '../Outputs/Test_run_2my_2000_particle_d18O_OU_heteroscedastic/ages/ODP846.txt'
ODP846_aligned = pd.read_table(ODP846_aligned_file_path, delimiter=' ',)
ODP846_aligned.set_index('depth(m)',inplace=True)

ODP846_original_file_path = '../../Stacking/Stack/LR04/846_LR04age.txt'
ODP846_original = pd.read_table(ODP846_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])
ODP846_original.set_index('Depth (mcd)',inplace=True)

ODP1146_aligned_file_path = '../Outputs/Test_run_2my_2000_particle_d18O_OU_heteroscedastic/ages/ODP1146.txt'
ODP1146_aligned = pd.read_table(ODP1146_aligned_file_path, delimiter=' ',)
ODP1146_aligned.set_index('depth(m)',inplace=True)

ODP1146_original_file_path = '../../Stacking/Stack/NewRecords/ODP1146.txt'
ODP1146_original = pd.read_table(ODP1146_original_file_path, delimiter='\t',
                                names=['Depth (mcd)', 'Age (ka)', 'd18O'])
ODP1146_original.set_index('Depth (mcd)',inplace=True)

#%% calculate diff
ODP929_age_diff = ODP929_aligned['median(kyr)'] - ODP929_original['Age (ka)']
ODP846_age_diff = ODP846_aligned['median(kyr)'] - ODP846_original['Age (ka)']
ODP1146_age_diff = ODP1146_aligned['median(kyr)'] - ODP1146_original['Age (ka)']

#%% plot
fig, axes = plt.subplots(1,1, sharex=True)

axes.plot(ODP929_age_diff.index,ODP929_age_diff,'-o',label='ODP 929')
axes.plot(ODP846_age_diff.index,ODP846_age_diff,'-o',label='ODP 846')
axes.plot(ODP1146_age_diff.index,ODP1146_age_diff,'-o', label='ODP 1146')
axes.set_xlabel('Depth (mcd)')
axes.set_ylabel('Age (kyr)')
plt.title('Difference between LR04 and new stack age')
fig.set_size_inches(6,4)
