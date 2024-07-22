#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 17:20:44 2024

@author: zhou
"""

import numpy as np
import pandas as pd

# read in data
df = pd.read_excel('../R/untuned_intermediate_tuned_ages.xlsx')

# add to tuned ages from -10 to 10 at 0.1 increment, record rmse
rmse = []
for i in np.arange(-10, 10.1, 0.1):
    rmse_i = (df[df['V2']==781]['V1'] + i - 781).values[0]**2 + (df[df['V2']==990]['V1'] + i - 990).values[0]**2\
        + (df[df['V2']==1070]['V1'] + i - 1070).values[0]**2 + (df[df['V2']==1180]['V1'] + i - 1180).values[0]**2\
            + (df[df['V2']==1775]['V1'] + i - 1775).values[0]**2 + (df[df['V2']==1934]['V1'] + i - 1934).values[0]**2\
                + (df[df['V2']==2116]['V1'] + i - 2116).values[0]**2 + (df[df['V2']==2140]['V1'] + i - 2140).values[0]**2
    rmse.append(rmse_i)
    
# result
# rmse minimal when i = 2.2
result = np.arange(-10, 10.1, 0.1)[np.argmin(rmse)]
