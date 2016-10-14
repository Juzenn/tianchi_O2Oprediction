# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
import pandas as pd

<<<<<<< HEAD
trainOn = pd.read_csv(r'C:\Users\Administrator\Desktop\o2o coupon\ccf_online_stage1_train.csv',sep=',',header=None)
trainOff = pd.read_csv(r'C:\Users\Administrator\Desktop\o2o coupon\ccf_offline_stage1_train.csv',sep=',',header=None)
testOff = pd.read_csv(r'C:\Users\Administrator\Desktop\o2o coupon\ccf_offline_stage1_test_revised.csv',sep=',',header=None)
=======
path0='E:\Downloads\ccf_data'
# path0= 'C:\Users\Administrator\Desktop\o2o coupon'

trainOn = pd.read_csv(path0+r'\ccf_online_stage1_train.csv',sep=',',header=None)
trainOff = pd.read_csv(path0+r'\ccf_offline_stage1_train.csv',sep=',',header=None)
testOff = pd.read_csv(path0+r'\ccf_offline_stage1_test.csv',sep=',',header=None)
>>>>>>> 922ce2be6e1bbb04f8a1dd984c2d5150862dac6b

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
#%% 1/(distance+c) c=0.5
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
    a=i.split(':')
    if len(a)==2:
        return 1-float(a[1])/float(a[0])
    else:
        return float(a[0])
        
def rate_level(i):
<<<<<<< HEAD
    a=array(i.split(':'))
=======
    a=i.split(':')
    if len(a)==2:
        return int(a[0])
    else:
        return 0
        
def rate_minus(i):
    a=i.split(':')
>>>>>>> 922ce2be6e1bbb04f8a1dd984c2d5150862dac6b
    if len(a)==2:
        return int(a[1])
    else:
        return 0

trainOff_rate['rate_change']=trainOff_rate[3].apply(rate_change)
trainOff_rate['rate_level']=trainOff_rate[3].apply(rate_level)
trainOff_rate['rate_minus']=trainOff_rate[3].apply(rate_minus)

#%% 1/(+c) c=0.5
import pandas as pd
from numpy import *
import math
u=pd.merge(trainOff_rate,pd.DataFrame({'index':A_B.index,'A_B':A_B}),left_on=0,right_on='index')


D = u.groupby('rate_level').size()
uu = u[u[6] != 'null']
C = uu.groupby('rate_level').size()

def exp(i):
    a=[]
    for j in i:
        a.append(math.exp(j))
    return pd.Series(a)

def log(i):
    a=[]
    for j in i:
        a.append(math.log(j))
    return pd.Series(a)


a1=pd.DataFrame({'A':D.index,'B':C/D})
a2=a1.iloc[1:len(a1),:]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(list(log(1/(a2.A-5))),list(a2.B))
plt.show()
aaaa=u[u['rate_level'] == 300]

#%% 去掉dist rate为空的：
trainOff_rate_dist=trainOff_rate[trainOff_rate[4]!='null']
trainOff_rate_dist[4]=trainOff_rate_dist[4].astype('int')
grouped_rate_dist=trainOff_rate_dist.groupby([4,'rate_level'])
count_grouped=grouped_rate_dist.size()
aaa=pd.DataFrame(count_grouped.index)[0]
def tupleout(x):
    a=[]
    b=[]
    for i in x:
        a.append(i[0])
        b.append(i[1])
    c=pd.DataFrame({'distance':a,'rate_level':b})
    return c



uu1=trainOff_rate_dist[trainOff_rate_dist[6]!='null']
count_grouped_1=uu1.groupby([4,'rate_level']).size()
pab_grouped=count_grouped_1/count_grouped

oooo=tupleout(aaa)
oooo['aaa']=aaa
result_dist_rate=pd.merge(oooo,pd.DataFrame({'pab':pab_grouped,'aaa':pab_grouped.index}),on='aaa')
del result_dist_rate['aaa']
result_dist_rate.to_csv('aaa.txt',index=False)

#%%

#%%没用
from numpy import *
trainOff_havecoupon = trainOff[trainOff[2] != 'null']
trainOff_havecoupon[3] = trainOff_havecoupon[3].apply(rate_level)
trainOff_havecoupon = trainOff_havecoupon[trainOff_havecoupon[3] != 0]
trainOff_havecoupon_hdist = trainOff_havecoupon[trainOff_havecoupon[4] != 'null']
del trainOff_havecoupon_hdist[0]
del trainOff_havecoupon_hdist[1]
del trainOff_havecoupon_hdist[2]
del trainOff_havecoupon_hdist[5]
l = []
for i in trainOff_havecoupon_hdist[6]:
    if i == 'null':
        l.append(0)
    else:
        l.append(1)
trainOff_havecoupon_hdist[7] = l
del trainOff_havecoupon_hdist[6]



#%%很没劲啊
grouped = trainOn[trainOn[2] == 1].groupby(0)
count_user = grouped.size()
count_user1 = pd.DataFrame(count_user)
count_user1[1] = count_user.index
look = pd.merge(trainOff,count_user1,left_on=0,right_on=1)
pd.Series('null' in trainOn[6][trainOn[0]==2914311]).astype('int').cumsum()
look = look.replace('null',NaN)
look1 = look.groupby(0).count()
look1['user']=look1.index

a = pd.merge(look1,count_user1,left_on='user',right_on=1)
b = pd.DataFrame({'huhuiqi':a[6],'py':a[0]})
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(1/a[6],(a[0]))
plt.show()