setwd('E:\\OneDrive\\Documents\\_Sufelearning\\Bigdata\\tianchi_O2Oprediction')
data<-read.table('aaa.txt',header=T,sep = ',')
dist<-log(data$distance+0.37598)
rate<-log(data$rate_level+13.06200)
y<-data$pab
lmsummary<-summary(lm(log(y)~cbind(dist,rate)))
lmsummary
hist(lmsummary$residuals,50)
var(lmsummary$residuals)
length(y)
cor(lmsummary$residuals,cbind(rep(1,length(y)),dist,rate)%*%lmsummary$coefficients[,1])
cov(X)

X1<-data$distance
X2<-data$rate_level
n<-length(y)
X<-cbind(rep(1,n),log(X1+0.37),log(X2+14))
loglikefun<-function(p)  {
  sigma<-p[4];
  mu<-p[1:3]
  X<-cbind(rep(1,n),log(X1+p[5]),log(X2+p[6]))
  -n*log(2*pi)-n*log(sigma^2)-(1/(2*sigma^2))*t(log(y)-X%*%mu)%*%(log(y)-X%*%mu)
}
#install.packages('maxLik')
#library(maxLik)
mle<-maxLik(logLik=loglikefun, start=c(1,-0.43,-0.91,0.3,0.37598,13.06208))

(a<-summary(mle))
cor(y,y-X%*%a$estimate[1:3,1])
M<-function(X){
  X<-as.matrix(X)
  diag(rep(1,nrow(X)))-X%*%solve(t(X)%*%X)%*%t(X)
}
Mi<-M(rep(1,nrow(X)))
R2<-1-t(y)%*%M(X)%*%y/t(y)%*%Mi%*%y

summary(lm(log(y)~cbind(log(dist),log(rate))))

y>0.1

glm(as.numeric(y>0.1)~cbind(X1,X2),family=binomial(link="logit"))
