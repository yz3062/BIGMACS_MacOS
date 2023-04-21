#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:31:12 2023

@author: zhou
"""

import pandas as pd

df = pd.read_table('stack.txt')
df = df.groupby('Time (ka)').mean()