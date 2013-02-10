# my script
setwd("C:\\Users\\Anna\\Projects\\honors")
require(zoo)

#import sentiment data into a data frame
sentimentdata=read.csv("data/obamatweets_daily.csv", sep='\t', header=TRUE)

#import poll data
polldata=read.csv("data/favorable_data.csv", sep='\t', header=TRUE)

#convert dates to dates
polldata[1]=as.Date(polldata[,1], format='%Y-%m-%d')
polldata[2]=as.Date(polldata[,2], format='%Y-%m-%d')
sentimentdata[1]=as.Date(sentimentdata[,1], format='%Y-%m-%d')

#TODO: join data and find correlations, perhaps using zoo and lag functions(?) 
#TODO: Learn R