# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 00:09:44 2016

@author: yanpan
"""
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
'''
Table 1: ## trainOff ## 用户线下消费和优惠券领取行为 
0        User_id
1    Merchant_id
2      Coupon_id
3  Discount_rate
4       Distance
5  Date_received
6           Date

Table 2: ## trainon ## 用户线上点击/消费和优惠券领取行为
0        User_id
1    Merchant_id
2         Action
3      Coupon_id
4  Discount_rate
5  Date_received
6           Date

Table 3：## testoff ## 用户O2O线下优惠券使用预测样本
0        User_id
1    Merchant_id
2      Coupon_id
3  Discount_rate
4       Distance
5  Date_received

Table 4：选手提交文件字段，其中user_id,coupon_id和date_received均来自Table 3,而Probability为预测值
0        User_id
1      Coupon_id
2  Date_received
3    Probability
'''
path0='C:\Users\Administrator\Desktop\o2o coupon'
#'E:\Downloads\ccf_data'
# path0= 'C:\Users\Administrator\Desktop\o2o coupon'

trainoff = pd.read_csv(path0+r'\ccf_offline_stage1_train.csv',sep=',',header=None)
trainon  = pd.read_csv(path0+r'\ccf_online_stage1_train.csv', sep=',',header=None)
testoff = pd.read_csv(path0+r'\ccf_offline_stage1_test_revised.csv', sep=',',header=None)


#%%
import re
pattern=re.compile(':|\.')
trainoff['_nfindr']=1-pd.Series([len(pattern.findall(x)) for x in trainoff[3]])
testoff['_nfindr']=1-pd.Series([len(pattern.findall(x)) for x in testoff[3]])

# testoff[testoff[3]=='null']

def rate_change(i):
    a=i.split(':')
    if len(a)>1:
        return 1-float(a[1])/float(a[0])
    else:
        return float(a[0])
       
def rate_level(i):
    a=i.split(':')
    if len(a)>1:
        return int(a[0])
    else:
        return 0
        
def rate_minus(i):
    a=i.split(':')
    if len(a)>1:
        return int(a[1])
    else:
        return 0

trainoff['rate_change']=trainoff[3][trainoff['_nfindr']==0].apply(rate_change)
trainoff['rate_level'] =trainoff[3][trainoff['_nfindr']==0].apply(rate_level)
trainoff['rate_minus'] =trainoff[3][trainoff['_nfindr']==0].apply(rate_minus)

testoff['rate_change']=testoff[3][testoff['_nfindr']==0].apply(rate_change)
testoff['rate_level'] =testoff[3][testoff['_nfindr']==0].apply(rate_level)
testoff['rate_minus'] =testoff[3][testoff['_nfindr']==0].apply(rate_minus)

#%%
trainoff['_nfindd']=(trainoff[4]=='null').astype('int')
trainoff['_y']=1-(trainoff[6]=='null').astype('int')

testoff['_nfindd']=(testoff[4]=='null').astype('int')

#%%
trainoff_result=trainoff.replace('nan',0).replace('null',0)
trainoff_result.to_csv(r'C:\Users\Administrator\Desktop\trainoff_result_logistic.txt',index=False)

testoff_result=testoff.replace('nan',0).replace('null',0)
testoff_result.to_csv(r'C:\Users\Administrator\Desktop\testoff_result_logistic.txt',index=False)
#%%
from sklearn.linear_model import LogisticRegression 
import numpy as np
classifier = LogisticRegression()
target=np.array(trainoff_result['_y'])
one=pd.DataFrame(np.array(list('1'*1754884)).astype('int'))#,trainoff_result.index)

samples=np.matrix(one.join(trainoff_result[['_nfindd',4,'_nfindr','rate_level']]))
classifier.fit(samples, target) 

classifier.coef_

#%%



