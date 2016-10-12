setwd('C:\\Users\\yanpan\\Downloads\\ccf_data')
trainoff<-read.csv('ccf_offline_stage1_train.csv',header=F,stringsAsFactors=F)
names(trainoff)<-c('User_id','Merchant_id','Coupon_id','Discount_rate','Distance','Date_received','Date')

a0<-strsplit(trainoff$Discount_rate,':')
a<-sapply(a0,function(x){ifelse(length(x)>1,1-as.numeric(x[2])/as.numeric(x[1]),as.numeric(x))})
trainoff$Discount_rate<-a
trainoff$Distance<-as.numeric(trainoff$Distance)
trainoff$Coupon_id<-as.numeric(trainoff$Coupon_id)
trainoff$Date_received<-as.Date(as.character(as.numeric(trainoff$Date_received)),format='%Y%m%d')
trainoff$Date<-as.Date(as.character(as.numeric(trainoff$Date)),format='%Y%m%d')
trainoffcal0<-na.omit(trainoff)
trainoffcal<-unique(trainoffcal0)

y<-as.numeric(trainoffcal$Date-trainoffcal$Date_received)
x1<-trainoffcal$Discount_rate
x2<-trainoffcal$Distance
summary(lm(y~cbind(x1,x2)))
#length(unique(trainoffcal$User_id))
#table1<-aggregate(trainoffcal,by=list(trainoffcal$User_id),FUN=mean)

#################################ROC
library(ROCR)
ypred <- c(1.1, 0.2, 3.4, 5.1, 2.1, 0.4, 2.4)
y     <- c(0,   0,   1,   0,   1,   0,   0  )
pred <- prediction(ypred,y)
auc <- performance(pred,'auc')
auc <- unlist(slot(auc,'y.values'))
print(auc)


pred0= runif(100)
pred1= pred0+(runif(100)-0.5)*2
y1   = as.numeric(pred0>0.5)
glm.fit=glm(y1~pred1,family=binomial(link="logit"))
#coef(summary(glm.fit))[2,4]
summary(glm.fit)

mroclog<-function(i,k){
  a<-NULL
# b<-NULL
  for(j in 1:k){
    pred0= runif(100)
    pred1= pred0+(runif(100)-0.5)*i
    y1   = as.numeric(pred0>0.5)
    pred <- prediction(pred1,y1)
    auc <- performance(pred,'auc')
    auc <- unlist(slot(auc,'y.values'))
#   glm.fit<-glm(y1~pred1,family=binomial(link="logit"))
#   pv<-1-coef(summary(glm.fit))[2,4]
    a<-c(a,auc)
#   b<-c(b,pv)
    }
# c(mean(a),mean(b))
  mean(a)
}

mroclog(0.6,200)

