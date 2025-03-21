#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:43:58 2024

@author: zhou
"""

import pandas as pd
import matplotlib.pyplot as plt

amp_putput = pd.read_excel('../R/amp_output.xlsx')
plt.imshow(amp_putput.T, vmax=0.007)#, extent=(0, 50, 0, 100)