# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 09:25:46 2020

@author: Adam.Comelio
"""

import time

def time_me(func):
    def inner1(*args, **kwargs):
        st = time.perf_counter_ns()
        r = func(*args, **kwargs)
        print('Function done in {} seconds real time'.format(
                                            (time.perf_counter_ns()-st)/1e9))
        return r
    return inner1

def tokenise_input_file(filepath, seperator='\n'):
    with open(filepath, 'r') as f:
        text = f.read()
    return text.split(seperator)
