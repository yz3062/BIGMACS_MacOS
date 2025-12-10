#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 17:20:44 2024

@author: zhou
"""

import numpy as np
import pandas as pd

# read in data
df = pd.read_excel('../R/untuned_intermediate_tuned_ages_win500.xlsx')

# add to tuned ages from -10 to 10 at 0.1 increment, record rmse
rmse = []
for i in np.arange(-20, 20.1, 0.1):
    rmse_i = (df[df['V2']==773]['V1'] + i - 773).values[0]**2 + (df[df['V2']==990]['V1'] + i - 990).values[0]**2\
        + (df[df['V2']==1070]['V1'] + i - 1070).values[0]**2 + (df[df['V2']==1180]['V1'] + i - 1180).values[0]**2\
            + (df[df['V2']==1215]['V1'] + i - 1215).values[0]**2 + (df[df['V2']==1775]['V1'] + i - 1775).values[0]**2\
                + (df[df['V2']==1934]['V1'] + i - 1934).values[0]**2 + (df[df['V2']==2116]['V1'] + i - 2116).values[0]**2\
                    # + (df[df['V2']==2595]['V1'] + i - 2595).values[0]**2 # only use for win size < 200
    rmse.append(rmse_i)
    
# result
# rmse minimal when i = 2.2
# rmse minimal for untuned global is i = 13
result = np.arange(-20, 20.1, 0.1)[np.argmin(rmse)]

print(result)