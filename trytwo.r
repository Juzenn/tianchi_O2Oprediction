setwd('E:\\OneDrive\\Documents\\_Sufelearning\\Bigdata\\tianchi_O2Oprediction')
data<-read.table('aaa.txt',header=T,sep = ',')
dist<-1/(data$distance+0.666962)
rate<-1/(data$rate_level+32.801582)
y<-data$pab
lmsummary<-summary(lm(y~cbind(dist,rate)))
lmsummary
hist(lmsummary$residuals,50)
density(lmsummary$residuals)
length(y)
cor(lmsummary$residuals,cbind(rep(1,length(y)),dist,rate)%*%lmsummary$coefficients[,1])

X1<-data$distance
X2<-data$rate_level
n<-length(y)
X<-cbind(rep(1,n),1/(X1+0.666962),1/(X2+32.801582))
loglikefun<-function(p)  {
  sigma<-p[4];
  mu<-p[1:3]
  # X<-cbind(rep(1,n),1/(X1+0.666962),1/(X2+32.801582))
  -n*log(2*pi)-n*log(sigma^2)-(1/(2*sigma^2))*t(y-X%*%mu)%*%(y-X%*%mu)
}
#install.packages('maxLik')
#library(maxLik)
mle<-maxLik(logLik=loglikefun, start=c(0.01,0.04,0.62,0.02))

a<-summary(mle)
cor(y,y-X%*%a$estimate[1:3,1])
M<-function(X){
  X<-as.matrix(X)
  diag(rep(1,nrow(X)))-X%*%solve(t(X)%*%X)%*%t(X)
}
Mi<-M(rep(1,nrow(X)))
R2<-1-t(y)%*%M(X)%*%y/t(y)%*%Mi%*%y

