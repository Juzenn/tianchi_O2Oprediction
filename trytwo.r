setwd('E:\\OneDrive\\Documents\\_Sufelearning\\Bigdata\\tianchi_O2Oprediction')
dataols<-read.table('aaa.txt',header=T,sep = ',')
dist<-log(dataols$distance+0.37598)
rate<-log(dataols$rate_level+13.06200)
y<-dataols$pab
lmsummary<-summary(lm(log(y)~cbind(dist,rate)))
lmsummary
qqnorm(lmsummary$residuals)
qqline(lmsummary$residuals)

hist(lmsummary$residuals,50)
var(lmsummary$residuals)
length(y)
cor(lmsummary$residuals,cbind(rep(1,length(y)),dist,rate)%*%lmsummary$coefficients[,1])

X1<-dataols$distance
X2<-dataols$rate_level
n<-length(y)
X<-cbind(rep(1,n),log(X1+0.37598),log(X2+13.06200))
loglikefun<-function(p)  {
  sigma<-p[4];
  mu<-p[1:3]
  #X<-cbind(rep(1,n),log(X1+p[5]),log(X2+p[6]))
  -n*log(2*pi)-n*log(sigma^2)-(1/(2*sigma^2))*t(log(y)-X%*%mu)%*%(log(y)-X%*%mu)
}
#install.packages('maxLik')
library(maxLik)
mle<-maxLik(logLik=loglikefun, start=c(1,-0.43,-0.91,0.3))#,0.37598,13.06208))

(a<-summary(mle))
#cor(y,y-X%*%a$estimate[1:3,1])
#M<-function(X){
#  X<-as.matrix(X)
#  diag(rep(1,nrow(X)))-X%*%solve(t(X)%*%X)%*%t(X)
#}
#Mi<-M(rep(1,nrow(X)))
#R2<-1-t(y)%*%M(X)%*%y/t(y)%*%Mi%*%y

#summary(lm(log(y)~cbind(log(dist),log(rate))))

#y>0.1

#glm(as.numeric(y>0.1)~cbind(X1,X2),family=binomial(link="logit"))

# AUC from trythree.r
#%*%lmsummary$coefficients

AB<-(data$X2>1)*(data$X6>1)
dataAB<-data.frame(data,AB)
datardAB<-dataAB[(dataAB$X_nfindr+dataAB$X_nfindd)<1,]
rdrate<-log(datardAB$rate_level+13.06200)
rddist<-log(datardAB$X4+0.37598)
rdX<-cbind(1,rddist,rdrate)
rdyp<-exp(rdX%*%lmsummary$coefficients[,1])
rdy<-datardAB$AB

hist(rdyp,50)

datardAB0<-data.frame(yp=rdyp,datardAB[,1:(length(datardAB)-2)],X_y=rdy)
rdcoupon<-unique(datardAB0$X2)

mean(couponauc(rdcoupon,datardAB0))


setwd('C:\\Users\\yanpan\\Desktop')
datatest<-read.table('testoff_result_logistic.txt',header=T,sep=',')
#y~notdist+notrate+log(ratelevel+65)+log(distance+0.4)
Xtest<-cbind(1,log(datatest$rate_level+13.06200),log(datatest$X4+0.37598))
ytestpred<-exp(Xtest%*%lmsummary$coefficients[,1])
# try1<-datatest[ytestpred>1.29,]
# hist(ytestpred,50)
datatestpred<-data.frame(User_id=datatest$X0,Coupon_id=datatest$X2,Date_received=datatest$X5,Probability=ytestpred)

write.csv(datatestpred,'datatestpred.csv',row.names =F)
