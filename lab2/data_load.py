# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:47:37 2019

@author: Administrator
"""

import json

filename = 'resources/names.json'

with open(filename, 'r') as f:
    data = json.load(f)
    
#print(type(data))
#print(len(data))
print('Marie Cruz ID: ',data['Marie Cruz'])

for i in data:
    if data[i] == 16097:
        print(i)
    
    
######
    
    
    
    
    
    
    
    