#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 23:30:40 2022

@author: abhijeet
"""

import pandas
from k_id_functions import k_id_generator

data = pandas.read_csv("~/Downloads/aod_interpolated.csv")

print(data.columns)
print(data.head())

columns = data.columns

data.drop(labels=['Unnamed: 0', 
                  'blh', 
                  'r',
                  'u10',
                  'v10',
                  'sp',
                  't2m',
                  'tcrw'],
                  axis=1,inplace=True)

data["k_id"] = k_id_generator(data["longitude"], data["latitude"])

data.to_csv("/Ranjan/Data/")