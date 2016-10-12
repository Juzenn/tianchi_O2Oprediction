setwd('C:\\Users\\yanpan\\Desktop')
data<-read.table('trainoff_result_logistic.txt',header=T,sep=',')

y<-data$X_y
notdist<-data$X_nfindd
notrate<-data$X_nfindr
ratechange<-data$rate_change
ratelevel<-data$rate_level
rateminus<-data$rate_minus
distance<-data$X4
X<-cbind(notdist,notrate,ratelevel,distance)

lmrude<-lm(y~X)
summary(lmrude)
hist(lmrude$residuals,50)
cor(X)
#install.packages('car')
library(car)
vif(lm(y~notdist+notrate+ratelevel+distance))

#glmlogit0<-glm(y~X,family=binomial(link="logit"))
#summary(glmlogit0)

glmlogit<-glm(y~notdist+notrate+log(ratelevel+65)+log(distance+0.4),family=binomial(link="logit"))
summary(glmlogit)

X1<-cbind(1,notdist,notrate,log(ratelevel+65),log(distance+0.4))
yp<-1/(1+exp(-X1%*%glmlogit$coefficients))

data0<-cbind(yp,data)
coupon<-unique(data0$X2)

#install.packages('ROCR')
library(ROCR)



couponauc<-function(coupon,data0){
  auc0<-NULL
  for(i in 1:length(coupon)){ # 1:1000
    index1<-data0$X2==coupon[i]
    yp1<-data0$yp[index1]
    y1<-data0$X_y[index1]
    if(sum(y1==0)==0){
      y1<-c(y1,0)
      yp1<-c(yp1,0)
    }
    if(sum(y1==1)==0){
      y1<-c(y1,1)
      yp1<-c(yp1,1)
    }
    pred <- prediction(yp1,y1)
    auc <- performance(pred,'auc')
    auc <- unlist(slot(auc,'y.values'))
    auc0<-c(auc0,auc)
  }
  auc0
}


auc0<-couponauc(coupon,data0)
mean(auc0)
auc0index<-which(auc0==0)
coupon[auc0index[1]]
auc0index3396<-data0$X2==coupon[auc0index[1]]
yp13396<-data0$yp[auc0index3396]
y13396<-data0$X_y[auc0index3396]


data0goodrate<-data0[data0$X_nfindr==0,]
coupongoodrate<-unique(data0goodrate$X2)
auc0goodrate<-couponauc(coupongoodrate,data0goodrate)
mean(auc0goodrate)


datatest<-read.table('testoff_result_logistic.txt',header=T,sep=',')
#y~notdist+notrate+log(ratelevel+65)+log(distance+0.4)
Xtest<-cbind(1,datatest$X_nfindd,datatest$X_nfindr,log(datatest$rate_level+65),log(datatest$X4+0.4))
ytestpred<-1/(1+exp(-Xtest%*%glmlogit$coefficients))
datatestpred<-data.frame(User_id=datatest$X0,Coupon_id=datatest$X2,Date_received=datatest$X5,Probability=ytestpred)

write.csv(datatestpred,'datatestpred.csv',row.names =F)
