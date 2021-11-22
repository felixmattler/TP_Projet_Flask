# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 13:17:27 2021

@author: user
"""

import json

data = {}
data['equipements'] = []
data['equipements'].append({
    'name': 'Scott',
    'ip': '192.168.10.254',
    'oids': '3.1.2.1.1'
})

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
