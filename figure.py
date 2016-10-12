# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
import pandas as pd

trainOn = pd.read_csv(r'C:\Users\Administrator\Desktop\o2o coupon\ccf_online_stage1_train.csv',sep=',',header=None)
trainOff = pd.read_csv(r'C:\Users\Administrator\Desktop\o2o coupon\ccf_offline_stage1_train.csv',sep=',',header=None)
testOff = pd.read_csv(r'C:\Users\Administrator\Desktop\o2o coupon\ccf_offline_stage1_test.csv',sep=',',header=None)

#%%
trainOff = trainOff[trainOff[2] != 'null']
grouped_by_userid = trainOff.groupby(trainOff[0])
B = grouped_by_userid.size()
trainOff_buy = trainOff[trainOff[6] != 'null']
grouped = trainOff_buy.groupby(trainOff_buy[0])
A = grouped.size()
A_B = (A/B).replace('NaN',0)

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(A_B,bins=50)
plt.show()

#%%
A_B_not0 = A_B[A_B > 0]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(A_B_not0,bins=50)
plt.show()


#%%
trainOff_buy_havedistance = trainOff_buy[trainOff_buy[4] != 'null']
grouped_by_distance = trainOff_buy_havedistance.groupby(trainOff_buy_havedistance[4])
relation_on_distance = grouped_by_distance.size()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(list(relation_on_distance.index),list(relation_on_distance.values))
plt.show()

#%%
trainOff_havedistance = trainOff[trainOff[4] != 'null']
grouped_by_distance2 = trainOff_havedistance.groupby(trainOff_havedistance[4])
relation_on_distance2 = grouped_by_distance2.size()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(list(relation_on_distance2.index),list(relation_on_distance2.values))
plt.show()

#%%
from numpy import *
prob_on_distance = list(array(relation_on_distance.values)/array(relation_on_distance2.values).astype('float'))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(list(relation_on_distance2.index),prob_on_distance)
plt.show()
#%% 1/(distance+c) c=1
a = 1/(array(relation_on_distance2.index).astype('float')+0.5)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(a,prob_on_distance)
plt.show()

#%%
result1 = pd.DataFrame()
result1[0] = A_B.index
result1[6] = A_B.values
del testOff[2]
del testOff[3]
del testOff[4]
result = pd.merge(result1,testOff,how='right')
result = result.replace('NaN',0)
a = result[6]
del result[6]
result[7] = a
result[0] = result[0].astype('int')
result.to_csv(r'c:\huhuiqi.csv')




#%%
trainOff_rate =trainOff[trainOff[3] != 'null']
trainOff_rate =trainOff_rate[trainOff_rate[3] != 'fixed']

def rate_change(i):
    a=pd.Series(i.split(':')).astype('float')
    if len(a)==2:
        return 1-a[1]/a[0]
    else:
        return a[0]
        
def rate_level(i):
    a=pd.Series(i.split(':')).astype('float')
    if len(a)==2:
        return a[0]
    else:
        return 0

trainOff_rate['rate_change']=trainOff_rate[3].apply(rate_change)
trainOff_rate['rate_level']=trainOff_rate[3].apply(rate_level)

