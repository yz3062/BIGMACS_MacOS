#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:48:09 2022

@author: zhou
"""

import scipy.io
import matplotlib.pyplot as plt

mat = scipy.io.loadmat('../results.mat')

# summary is where detailed data is stored
mat_summary = mat['summary']
# Find ODP928 age samples
ODP928_age_samples = mat_summary['age_samples'][mat_summary['name']==['ODP928']][0]
ODP928_depths = mat_summary['depth'][mat_summary['name']==['ODP928']][0]

for i in range(1000):
    plt.plot(ODP928_age_samples[:,i], ODP928_depths, color='k', alpha=0.1)

# plt.savefig('ODP928_age_model_distribution.png', dpi=500)

#%% histogram for 60 m
import numpy as np
import matplotlib.pyplot as plt

n, bins, patches = plt.hist(ODP928_age_samples[(ODP928_depths==57.99).flatten(), :].flatten(),
          bins=50,
          density=True,
          stacked=True,
          facecolor='gray',
          alpha=0.75)

plt.xlabel('Age (ka)')
plt.ylabel('Frequency')
plt.title('Age estimate distribution. ODP 928. Depth = 57.99 m')
plt.savefig('ODP928_5799m_age_distribution.png', dpi=500)