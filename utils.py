# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 09:25:46 2020

@author: Adam.Comelio
"""

import time

def time_me(func):
    def inner1(*args, **kwargs):
        st = time.process_time_ns()
        pst = time.perf_counter_ns()
        r = func(*args, **kwargs)
        print('Function done in {} nanoseconds process time'.format((time.process_time_ns()-st)))
        print('Function done in {} seconds real time'.format((time.perf_counter_ns()-pst)/1e9))
        return r
    return inner1
