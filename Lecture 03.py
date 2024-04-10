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
D = 5000

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
f3 = plt.subplots(3,1)
#Inflows
plt.subplot(3,1,1)
plt.plot(df15.DATE, df15.inf_af ,label = "Inflow")
#Outflows
plt.subplot(3,1,2)
plt.plot(df15.DATE, df15.release, label = "Outflow")
#Storage
plt.subplot(3,1,3)
plt.plot(df15.DATE, df15.storage, label = "Outflow")





