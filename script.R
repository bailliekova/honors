#TODO: Learn R
#set working directory
setwd("C:\\Users\\Anna\\Projects\\honors")
#get zoo library for working with time series data
require(zoo)

#import sentiment data into a data frame
sentimentdata=read.csv("data/obamatweets_daily.csv", sep='\t', header=TRUE)

#import poll data
polldata=read.csv("data/favorable_data.csv", sep='\t', header=TRUE)

#convert dates to dates
polldata[,1]=as.Date(polldata[,1], format='%Y-%m-%d')
polldata[,2]=as.Date(polldata[,2], format='%Y-%m-%d')

#order polldata
attach(polldata)
polldata=polldata[order(enddate,startdate),]
detach(polldata)

#smooth poll data
polldata$sm_favorable=smooth(polldata$favorable)
polldata$sm_unfavorable=smooth(polldata$unfavorable)

# #plot poll data
# pdf(file="favorability_o.pdf")
# plot(polldata$enddate, polldata$unfavorable, col="red", ylim=c(0,1), ylab="% respondents", xlab="Date")
# par(new=T)
# plot(polldata$enddate, polldata$favorable, col="blue", ylim=c(0,1), ylab="", xlab="", axes=FALSE)
# par(new=T)
# plot(polldata$sm_unfavorable, type='l', col='red', ylim=c(0,1), lwd=3, ylab="", xlab="", axes=FALSE)
# par(new=T)
# plot(polldata$sm_favorable, type='l', col='blue', ylim=c(0,1), ylab="", xlab="", axes=FALSE, lwd=3)
# dev.off()

#order sentiment data
sentimentdata[1]=as.Date(sentimentdata[,1], format='%Y-%m-%d')
attach(sentimentdata)
sentimentdata=sentimentdata[order(date),]
detach(sentimentdata)

#get rolling averages: 
sentimentdata$sentiment_ma=rollmean(sentimentdata$sentiment, 3, na.pad=True)

#merge into one data set, matching poll enddate with sentiment date, keeping all values from sentiment
m=merge(polldata, sentimentdata, by.x="enddate", by.y="date", all.y=TRUE)
cor(m$sentiment, m$positive-m$negative)
cor(m$favorable, m$positive)
cor(m$unfavorable, m$negative)

#compute moving average of sentiment data
m$sentiment_ma=rollmean(m$sentiment, 3, na.pad=TRUE)

#create columns with lag

for (i in 1:15){
	lag_num=i
	lag(m$sentiment_ma, k=lag_num)
	#assign(paste("m$sentiment_ma_lagged_", as.character(lag_num)), lag(m$sentiment_ma, k=lag_num))
	#str(m)
	#cor(get(paste("m$sentiment_ma_lagged_", as.character(lag_num))), m$positive-m$negative)
}


#iterate through lags, calculating correlation coefficient, storing in a new dataframe to plot later.

