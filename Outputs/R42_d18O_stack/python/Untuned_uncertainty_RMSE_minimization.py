#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 15:34:05 2025

@author: zhou
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set(font='Arial',palette='husl',style='ticks',context='notebook')

df = pd.read_excel('../R/untuned_intermediate_tuned_ages_uncertainty_RMSE_minimization_untuned_ArAr.xlsx')
df.plot(x='depth', y='tsd', color='k', legend=False,
        xlabel='Age (ka BP)', ylabel='Age uncertainty 1σ (kyr)',
        xlim=(0,2700), ylim=(0,3.5))
# plt.savefig('Untuned_uncertainty_RMSE_minimization_untuned_ArAr.png', dpi=700)