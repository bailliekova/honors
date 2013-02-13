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
polldata[1]=as.Date(polldata[,1], format='%Y-%m-%d')
polldata[2]=as.Date(polldata[,2], format='%Y-%m-%d')
sentimentdata[1]=as.Date(sentimentdata[,1], format='%Y-%m-%d')

#merge into one data set, matching poll enddate with sentiment date, keeping all values from sentiment
m=merge(polldata, sentimentdata, by.x="enddate", by.y="date", all.y=TRUE)
cor(m$sentiment, m$positive-m$negative)
cor(m$favorable, m$positive)
cor(m$unfavorable, m$negative)

#compute moving average of sentiment data
m$sentiment_ma=rollmean(m$sentiment, 3)

#create columns with lag
lag_num=2
assign(paste("m$sentiment_ma_lagged_", as.character(lag_num)), lag(m$sentiment_ma, k=lag_num))

#TODO: using zoo and lag functions(?) 
#iterate through lags, calculating correlation coefficient, storing in a new dataframe to plot later.

