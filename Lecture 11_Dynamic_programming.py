#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 18:58:34 2023

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

data = pd.read_csv('dyn_prom_reservoir_example_data.csv')

#Calculating penalizations

#Flood control on period 1
data['es_t'] = (data.stor_init - 15)
data.loc[data.es_t<0,"es_t"] = 0
data['es_tplusone'] = data.stor_fin - 15
data.loc[data.es_tplusone<0,"es_tplusone"] = 0
data['flood_cost'] = (data.es_t**2) + (data.es_tplusone**2)
data.loc[data.period>1,"flood_cost"] = 0

#Recreation objective
data['rec_cost'] = (data.stor_init - 20)**2 + (data.stor_fin-20)**2
data.loc[data.period<2,"rec_cost"] = 0
data.loc[data.period>3,"rec_cost"] = 0

#Release cost
data['release_deficit'] = data.release_target - data.releases
data.loc[data.release_deficit<0,"release_deficit"] = 0
data['release_cost'] = data.release_deficit**2

#Total costs
data['costs'] = data.flood_cost + data.rec_cost + data.release_cost

states = [0,5,10,15,20]


result = pd.DataFrame()

for stage in np.arange(40, 0, -1):
    b = stage/4 - int(stage/4)
    if b == 0:
        period = 4
    else:
        period = int(b * 4)
    if stage == 40:
        for state in states:
            result_state = data.loc[data.period==period]
            result_state = result_state.loc[result_state.stor_init == state].reset_index(drop=True)
            result_state['stage'] = stage
            result_state = result_state.iloc[result_state['costs'].idxmin()]
            result = result.append(result_state)
    else:
        for state in states:
            result_state = data.loc[data.period==period]
            result_state = result_state.loc[result_state.stor_init == state].reset_index(drop=True)
            result_state['stage'] = stage
            result_state['costs'] = result_state['costs'] + result.loc[(result.stage==stage+1), "costs"].reset_index(drop=True)
            result_state = result_state.iloc[result_state['costs'].idxmin()]
            result = result.append(result_state)
        
result = result.reset_index(drop=True)

data_sel = pd.DataFrame()
for stage in np.arange(1,41):
    if stage==1:
        stor_init = 20
        data_sel = data_sel.append(result.loc[(result.stage==stage) & (result.stor_init==stor_init)]).reset_index(drop=True)
        stor_fin = data_sel.stor_fin
    else:
        stor_init = int(data_sel.loc[(data_sel.stage==stage-1), "stor_fin"])
        data_sel = data_sel.append(result.loc[(result.stage==stage) & (result.stor_init==stor_init)])
        
plt.plot(data_sel.stage, data_sel.stor_init)
plt.plot(data_sel.stage, data_sel.releases)


        
        
        
        
        
    
    
    
    


# =============================================================================
# from pyomo.environ import *
# from pyomo.opt import SolverStatus, TerminationCondition, SolverFactory
# =============================================================================

# =============================================================================
# Qt = [2,1,3,2]
# 
# Br = [-100, 50, 320, 480, 520, 510, 410, 120]
# 
# #f4(S4)=max(B4(R4))
# # r4<=S4+Q4 (max release is water available)
# # S4+Q4-R4<= 4 (max capacity reservoir)
# 
# df = pd.DataFrame(columns=['stage', 'storage_init', 'qt','release', 'storage_final', 'benefits', 'benefits_stage'])
# 
# 
# counter = 0 
# for t in np.arange(3,2,-1):
#     for s in np.arange(0,5):
#         S4 = s
#         ben = -1000
#         for r4 in np.arange(max(S4+Qt[t]-4, 0), S4+Qt[t]+1):
#             if Br[r4]>= ben:
#                 r4record = r4
#                 ben = Br[r4]
#         df.loc[counter, 'stage'] = t
#         df.loc[counter, 'storage_init'] = s
#         df.loc[counter, 'qt'] = Qt[t]
#         df.loc[counter, 'release'] = r4record
#         df.loc[counter, 'storage_final'] = s + Qt[t] - r4record
#         df.loc[counter, 'benefits'] = Br[r4record]
#         df.loc[counter, 'benefits_stage'] = Br[r4record]
#         counter = counter + 1
# 
# for t in np.arange(2,-1,-1):
#     for s in np.arange(0,5):
#         S4 = s
#         ben = -1000
#         for r4 in np.arange(max(S4+Qt[t]-4, 0), S4+Qt[t]+1):
#             if Br[r4]>= ben:
#                 r4record = r4
#                 ben = Br[r4] + df.loc[(df.stage==t+1) & (df.storage_init==s),"benefits"].reset_index(drop=True)[0]
#         df.loc[counter, 'stage'] = t
#         df.loc[counter, 'storage_init'] = s
#         df.loc[counter, 'qt'] = Qt[t]
#         df.loc[counter, 'release'] = r4record
#         df.loc[counter, 'storage_final'] = s + Qt[t] - r4record
#         df.loc[counter, 'benefits'] =  Br[r4record] + df.loc[(df.stage==t+1) & (df.storage_init==s),"benefits"].reset_index(drop=True)[0]   
#         df.loc[counter, 'benefits_stage'] =  Br[r4record]   
#         counter = counter + 1
# 
# =============================================================================
        
        
        

# =============================================================================
# 
# def nb0(x1):
#     p1 = 0.4*(x1)**0.9
#     result = (12-p1)*p1-3*(p1)**1.3
#     return result
# 
# def nb1(x2):
#     p2 = 0.5*(x2)**0.8
#     result = (20-1.5*p2)*p2-5*(p2)**1.2
#     return result
# 
# def nb2(x3):
#     p3 = 0.6*(x3)**0.7
#     result = (28-2.5*p3)*p3-6*(p3)**1.15
#     return result
# 
# benefits = []
# for stage in np.arange(2, -1,-1):
#     for x1 in np.arange(0,11):
#         for x2 in np.arange(0,11):
#             for x3 in np.arange(0,11):
# =============================================================================
                
                
    
        
    


# =============================================================================
# for x in np.arange(0, 5, 0.05):
#     plt.scatter(x, nb1(x), color = 'blue')
#     plt.scatter(x, nb2(x), color = 'orange')
#     plt.scatter(x, nb3(x), color = 'green')
# =============================================================================