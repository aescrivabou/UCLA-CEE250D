#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 16:58:10 2024

@author: alvar
"""

#Import packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Read or import files
df = pd.read_csv('DonPedroData.csv')

#Convert cfs to acre-feet/day
df['inf_af'] = df.INFLOW_cfs * 1.98346
df['out_af'] = df.OUTFLOW_cfs * 1.98346

#Remove zeros
df.loc[df.inf_af < 0, "inf_af"] = np.nan
df.loc[df.out_af < 0, "out_af"] = np.nan

#Processing
df['DATE'] = pd.to_datetime(df.DATE, format = 'mixed')

#Use only last 15 years
df15 = df.loc[df.DATE>='10-1-2009'].reset_index()

#Visualization or outputs
f1 = plt.figure(1)
plt.plot(df15.DATE, df15.inf_af ,label = "Inflow")
plt.plot(df15.DATE, df15.out_af, label = "Outflow")
plt.legend()

#A nicer 3-panel plot
f2 = plt.subplots(3,1)
#Inflows
plt.subplot(3,1,1)
plt.plot(df15.DATE, df15.inf_af ,label = "Inflow")
#Outflows
plt.subplot(3,1,2)
plt.plot(df15.DATE, df15.out_af, label = "Outflow")
#Storage
plt.subplot(3,1,3)
plt.plot(df15.DATE, df15.STORAGE_af, label = "Outflow")

#SLOP

#parameters
K = 2030000
D = 3500

T = len(df15)

Q =  df15['inf_af'].interpolate()

#Decision variable
R = np.zeros(T)

#Variables
S = np.zeros(T)
shortage = np.zeros(T)
spill = np.zeros(T)

#Let's start at the beginning of the first period
S[0] = K/2
R[0] = D

for t in range(1, T):
    #Storage at the beginning of next period, obtained as a mass balance
    S[t] = S[t-1] + Q[t-1] - R[t-1]
    #First condition
    if S[t] + Q[t]<D:
        R[t] = S[t] + Q[t]
    #Second condition
    elif S[t] + Q[t] < K + D:
        R[t] = D
    #Third condition
    else:
        R[t] = S[t] + Q[t] - K


df15['inflows'] = Q
df15['storage'] = S
df15['release'] = R


#A nicer 3-panel plot


#LECTURE 4
#Reliability
df15['demand']=D
df15['shortage']= df15.demand - df15.release
df15.loc[df15.shortage<0, "shortage"] = 0
df15['shortage_cost'] = (df15.shortage**2)/1000000


f3 = plt.subplots(4,1)
#Inflows
plt.subplot(4,1,1)
plt.plot(df15.DATE, df15.inf_af )
#Outflows
plt.subplot(4,1,2)
plt.plot(df15.DATE, df15.release)
#Storage
plt.subplot(4,1,3)
plt.plot(df15.DATE, df15.storage)
#Shortage
plt.subplot(4,1,4)
plt.bar(df15.DATE, df15.shortage_cost)

#Comparing storage
f4 = plt.figure(4)
plt.plot(df15.DATE, df15.STORAGE_af)
plt.plot(df15.DATE, df15.storage)

df15['demand_not_met']=0
df15.loc[df15.shortage>0,"demand_not_met"]=1
print("The reliability is " + str(100*(1- (df15.demand_not_met.sum()/len(df15))))+ "%")

#Firm yield
print(df15.release.min())

#Exceedance plot
df15['percentile_release'] = 1 - df15['release'].rank(pct=True)

plt.figure(5)
plt.scatter(df15.percentile_release, df15.release)

#Hedging

#Decision variable
R_h = np.zeros(T)

#Variables
S_h = np.zeros(T)
shortage = np.zeros(T)
spill = np.zeros(T)

#Let's start at the beginning of the first period
S_h[0] = K/2
R_h[0] = D

#hedging parameter
ho = 1000
hf = 750000
m = (D-ho)/(hf-ho)

for t in range(1, T):
    #Storage at the beginning of next period, obtained as a mass balance
    S_h[t] = S_h[t-1] + Q[t-1] - R_h[t-1]
    #First condition
    if S_h[t] + Q[t]<ho:
        R_h[t] = S_h[t] + Q[t]
    elif S_h[t] + Q[t] < hf:
        R_h[t] = m*(S_h[t] + Q[t] - ho) +ho
    #Third condition
    #Second condition
    elif S_h[t] + Q[t] < K + D:
        R_h[t] = D
    #Third condition
    else:
        R_h[t] = S_h[t] + Q[t] - K

df15['inflows'] = Q
df15['storage_h'] = S_h
df15['release_h'] = R_h
        
df15['shortage_h']= df15.demand - df15.release_h
df15.loc[df15.shortage_h<0, "shortage_h"] = 0

df15['shortage_cost_h'] = (df15.shortage_h**2)/1000000

f5 = plt.subplots(4,1)
#Inflows
plt.subplot(4,1,1)
plt.plot(df15.DATE, df15.inf_af )
#Outflows
plt.subplot(4,1,2)
plt.plot(df15.DATE, df15.release_h)
#Storage
plt.subplot(4,1,3)
plt.plot(df15.DATE, df15.storage_h)
#Shortage
plt.subplot(4,1,4)
plt.bar(df15.DATE, df15.shortage_cost_h)

print(df15.shortage_cost.sum())
print(df15.shortage_cost_h.sum())

