#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 00:38:59 2022

@author: zhou
"""

import pandas as pd
import os

input_path = '../R17/Records/'
folders = os.listdir(input_path)

folders.remove('.DS_Store')

for folder in folders:
    ## Per Taehee email, checking if the core is too long and shouldn't have
    # noninformative depths at the specific intervals
    # ages = pd.read_csv(input_path+folder+'/additional_ages.txt', delimiter='\t')
    # if ages['depth'].iloc[-1] > 100:
    #     print(folder)
    #     print(ages['depth'].iloc[-1])
    ## Per Taehee email, checking if smoothness_bandwidth is too large
    settings = pd.read_csv(input_path+folder+'/setting_core.txt',
                           delimiter=' ',
                           header=None)
    if settings.iloc[1][1] > 90:
        print(folder)
        print(settings.iloc[1][1])