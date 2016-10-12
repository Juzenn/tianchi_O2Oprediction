# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 16:26:01 2016

@author: yanpan
@user: huhuiqi
"""
#%%
import pandas as pd
trainoff = pd.read_csv("E:/Downloads/ccf_data/ccf_offline_stage1_train.csv",header=None,sep=',')
trainoff.columns = ['User_id','Merchant_id','Coupon_id','Discount_rate','Distance','Date_received','Date']

trainon = pd.read_csv("E:/Downloads/ccf_data/ccf_online_stage1_train.csv",header=None,sep=',')
trainon.columns=['User_id','Merchant_id','Action','Coupon_id','Discount_rate','Date_received','Date']

testoff = pd.read_csv("E:/Downloads/ccf_data/ccf_offline_stage1_test.csv",header=None,sep=',')
testoff.columns = ['User_id','Merchant_id','Coupon_id','Discount_rate','Distance','Date_received']

'''
traindatanew=pd.merge(pd.DataFrame(testdata['uid']),traindata)

traindatanew.to_csv('weibo_train_data.txt',header=None,sep='\t',index=False,encoding='utf-8')

for i in trainoff['Discount_rate']:
    if ':' in i:
        j=i.split(':')
        i=1-int(j[1])/int(j[0])
'''
#%%
import numpy as np
def change(i):
    if ':' in i:
        j=i.split(':')
        return 1-int(j[1])/int(j[0])
    else:
        return i
        
def applychange(i):
    i['Discount_rate']=i['Discount_rate'].apply(change)

def null2none(x):
    applychange(x)
    t=x.dtypes[x.dtypes==object].index
    for j in t:
        x[j][x[j]=='null']=None
        x[j][x[j]=='fixed']=0
        x[j]=x[j].astype(float)
    
#%%
null2none(testoff)
null2none(trainoff)
null2none(trainon)

#%%

a0=trainon[trainon['Action']==0]
a1=trainon[trainon['Action']==1]
a2=trainon[trainon['Action']==2]

uu=pd.DataFrame(list(set(trainon['User_id'])))#762858
u2=pd.DataFrame(list(set(a2['User_id'])))#214768
u1=pd.DataFrame(list(set(a1['User_id'])))#412182
u0=pd.DataFrame(list(set(a0['User_id'])))#585710
x01=pd.merge(u0,u1)#262216
x02=pd.merge(u0,u2)#134972
x12=pd.merge(u1,u2)#144005
x012=pd.merge(pd.merge(u0,u1),u2)#91391

len(uu)==len(u0)+len(u1)+len(u2)-len(x01)-len(x02)-len(x12)+len(x012)
#%%
def g(x):
    guu=x.groupby(['User_id','Coupon_id'])
    return pd.DataFrame(list(set(guu.mean().index)))
#%%
guu=g(trainon)#1380151
gu0=g(a0)#585710
gu1=g(a1)#509410
gu2=g(a2)#537307
gx01=pd.merge(gu0,gu1)#241805z
gx02=pd.merge(gu0,gu2)#0
gx12=pd.merge(gu1,gu2)#10471
gx012=pd.merge(pd.merge(gu0,gu1),gu2)#0

len(guu)==len(gu0)+len(gu1)+len(gu2)-len(gx01)-len(gx02)-len(gx12)+len(gx012)
pd.merge(pd.DataFrame(list(set(gu1[gu1.columns[1]]))),pd.DataFrame(list(set(gu2[gu2.columns[1]]))))
pd.DataFrame(list(set(gu1[gu1.columns[1]])))
pd.DataFrame(list(set(gu2[gu2.columns[1]])))
pd.DataFrame(list(set(gx12[gx12.columns[1]])))
#%%
grouped=trainon.groupby(['User_id','Action'])

groupedc=grouped.count()

#gc=pd.pivot_table(trainon, values='Date', index=['User_id','Action'], aggfunc='count')
#%%
import numpy as np
trainon0=trainon.copy()
trainon=trainon0.replace({'null':np.nan,'fixed':0})
trainon['Ubak']=trainon['User_id']

trainon['AB']=trainon.Coupon_id.astype(float)+trainon.Date.astype(float)
#trainonpivot=pd.pivot_table(trainon, columns=['Ubak','Date','Coupon_id','AB'], index=['User_id'], aggfunc='count')
grouped=trainon.groupby('User_id')
gtrainon=grouped.count()
probAonB=gtrainon.AB/gtrainon.Coupon_id
gtrainon['probAonB']=probAonB
#%%
import matplotlib.pyplot as plt

plt.plot(gtrainon.AB,gtrainon.Ubak,'ro')
plt.plot(gtrainon.AB,gtrainon.Coupon_id,'ro')

prob1=gtrainon[gtrainon.AB>0]
#prob6=prob5.probAonB[np.isnan(prob5.probAonB)==False]
plt.hist(prob1.probAonB,200)
# solow residual! 
# regress probAonB on otherthings and figure out a individual effect
# maybe only have to consider Action==1 


#%%
from sklearn import metrics
import sklearn as sk
import numpy as np
pred = [0.9, 0.8, 0.4, 0.3, 0.1, 1.0, 0.2]
y    = [1,   1,   0,   0,   0,   1,   0  ]
print('AUC:',sk.metrics.roc_auc_score(y,pred))
pred2=(np.array(pred)>0).astype(int)
pred1=1-np.array(pred)
y1=np.array(y)
print('AUC:',sk.metrics.roc_auc_score(y1,pred2))
sk.metrics.roc_curve(y1,pred1)


#%% AUC trick
y0=np.random.rand(1000)

def pred(y0,a1,b1):
    return np.random.rand(1000)*(1-(y0>b1).astype(int)-(y0<a1).astype(int))+(y0>b1).astype(int)
#    a=[]
#    for i in list(y0):
#        if i<a1:
#            a.append(0)
#        elif i>b1:
#            a.append(1)
#        else:
#            a.append(np.random.rand())
#    return a

y1=(y0>0.5).astype(int)
pred1=pred(y0,0.1,0.9)

print('AUC:',sk.metrics.roc_auc_score(y1,pred1))


#%%
import sklearn as sk
def mroc(i,k):
    a=[]
    for j in range(0,k):
        pred0= np.random.rand(100)
        pred1= pred0+(np.random.rand(100)-0.5)*i
        y1   = (pred0>0.5).astype(int)
        a.append(sk.metrics.roc_auc_score(y1,pred1))
    return pd.Series(a).mean()

mroc(3,100)

#%%
user_id_testoff_trainoff=pd.DataFrame(list(set(testoff.User_id)-set(trainoff.User_id)))
user_id_trainoff_testoff=pd.DataFrame(list(set(trainoff.User_id)-set(testoff.User_id)))

user_id_trainoff_trainon=pd.DataFrame(list(set(trainoff.User_id)-set(trainon.User_id)))
user_id_trainon_trainoff=pd.DataFrame(list(set(trainon.User_id)-set(trainoff.User_id)))

user_id_trainon=pd.DataFrame(list(set(trainon.User_id)))
user_id_trainoff=pd.DataFrame(list(set(trainoff.User_id)))
user_id_testoff=pd.DataFrame(list(set(testoff.User_id)))

user_id_testoff_trainon=pd.DataFrame(list(set(testoff.User_id)-set(trainon.User_id)))

user_id_testoff_trainon.columns=['User_id']
trainoff_bad=pd.merge(trainoff,user_id_testoff_trainon)
trainoff_bad_Date_null=trainoff_bad[trainoff_bad.Date=='null']

#%%
from sklearn import linear_model
import sklearn as sk
sk.linear_model.LogisticRegression

#%%
from numpy import * 
from sklearn.datasets import load_iris     # import datasets

# load the dataset: iris
iris = load_iris() 
samples = iris.data
#print samples 
target = iris.target 

# import the LogisticRegression
from sklearn.linear_model import LogisticRegression 

classifier = LogisticRegression()  # 使用类，参数全是默认的
classifier.fit(samples, target)  # 训练数据来学习，不需要返回值

x = classifier.predict([5, 3, 5, 2.5])  # 测试数据，分类返回标记

print(x)

#其实导入的是sklearn.linear_model的一个类：LogisticRegression， 它里面有许多方法
#常用的方法是fit（训练分类模型）、predict（预测测试样本的标记）

#不过里面没有返回LR模型中学习到的权重向量w，感觉这是一个缺陷

#%%~