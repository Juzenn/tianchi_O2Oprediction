# jisuan auc 
# input unique(data0$coupon),data0
# output auc for every coipon: array 

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

# prediction for py 2 r
# input address 'testoff_result_logistic.txt', lmsummary
# output datatestpred

prediction<-function(address,lmsummary){
  datatest<-read.table(address,header=T,sep=',')
  #y~notdist+notrate+log(ratelevel+65)+log(distance+0.4)
  Xtest<-cbind(1,log(datatest$rate_level+13.06200),log(datatest$X4+0.37598))
  ytestpred<-exp(Xtest%*%lmsummary$coefficients[,1])
  # try1<-datatest[ytestpred>1.29,]
  # hist(ytestpred,50)
  data.frame(User_id=datatest$X0,Coupon_id=datatest$X2,Date_received=datatest$X5,Probability=ytestpred)
}

# write.csv(datatestpred,'datatestpred.csv',row.names =F)



ccfdatarepo<-'C:\\Users\\Administrator\\Desktop\\o2o coupon'
py2rdatarepo<-'C:\\Users\\Administrator\\Desktop'

setwd(py2rdatarepo)
dataols<-read.table('trainoff_result_logistic.txt',sep=',',stringsAsFactors = F,header=T)
yols<-dataols$X_y
Xols<-cbind(dataols$X4,dataols$rate_level,dataols$rate_change,dataols$X_nfindr,dataols$X_nfindd)
summary(lm(yols~Xols))

