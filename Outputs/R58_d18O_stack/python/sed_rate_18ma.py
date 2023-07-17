#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 12:04:03 2023

@author: zhou
"""

import pandas as pd
from scipy import interpolate
import numpy as np

def age_model_interp(dated_ages, dated_depths, all_ages):
    f = interpolate.interp1d(dated_ages, dated_depths, fill_value='extrapolate')
    all_depths = f(all_ages)
    return all_depths

# U1308
U1308_df = pd.read_table('../ages/U1308.txt',
                         delimiter=' ')

U1308_all_depths = age_model_interp(U1308_df['median(kyr)'], U1308_df['depth(m)'], np.linspace(1500, 2200, 8))

U1308_sed_rates = (U1308_all_depths[1:] - U1308_all_depths[:-1])/100

# ODP982
ODP982_df = pd.read_table('../ages/982_LR04age.txt',
                         delimiter=' ')

ODP982_all_depths = age_model_interp(ODP982_df['median(kyr)'], ODP982_df['depth(m)'], np.linspace(1500, 2200, 8))

ODP982_sed_rates = (ODP982_all_depths[1:] - ODP982_all_depths[:-1])/100

# ODP926
ODP926_df = pd.read_table('../ages/ODP926.txt',
                         delimiter=' ')

ODP926_all_depths = age_model_interp(ODP926_df['median(kyr)'], ODP926_df['depth(m)'], np.linspace(1500, 2200, 8))

ODP926_sed_rates = (ODP926_all_depths[1:] - ODP926_all_depths[:-1])/100

# ODP928
ODP928_df = pd.read_table('../ages/ODP928.txt',
                         delimiter=' ')

ODP928_all_depths = age_model_interp(ODP928_df['median(kyr)'], ODP928_df['depth(m)'], np.linspace(1500, 2200, 8))

ODP928_sed_rates = (ODP928_all_depths[1:] - ODP928_all_depths[:-1])/100

# ODP929
ODP929_df = pd.read_table('../ages/929_LR04age.txt',
                         delimiter=' ')

ODP929_all_depths = age_model_interp(ODP929_df['median(kyr)'], ODP929_df['depth(m)'], np.linspace(1500, 2200, 8))

ODP929_sed_rates = (ODP929_all_depths[1:] - ODP929_all_depths[:-1])/100

# DSDP607
DSDP607_df = pd.read_table('../ages/607_LR04age.txt',
                         delimiter=' ')

DSDP607_all_depths = age_model_interp(DSDP607_df['median(kyr)'], DSDP607_df['depth(m)'], np.linspace(1500, 2200, 8))

DSDP607_sed_rates = (DSDP607_all_depths[1:] - DSDP607_all_depths[:-1])/100

# ODP659
ODP659_df = pd.read_table('../ages/659_LR04age.txt',
                         delimiter=' ')

ODP659_all_depths = age_model_interp(ODP659_df['median(kyr)'], ODP659_df['depth(m)'], np.linspace(1500, 2200, 8))

ODP659_sed_rates = (ODP659_all_depths[1:] - ODP659_all_depths[:-1])/100

# ODP1267
ODP1267_df = pd.read_table('../ages/ODP1267.txt',
                         delimiter=' ')

ODP1267_all_depths = age_model_interp(ODP1267_df['median(kyr)'], ODP1267_df['depth(m)'], np.linspace(1500, 2200, 8))

ODP1267_sed_rates = (ODP1267_all_depths[1:] - ODP1267_all_depths[:-1])/100













