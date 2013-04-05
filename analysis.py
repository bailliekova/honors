import pandas as pd
from pandas import DataFrame, Series
from datetime import timedelta, datetime

sentfile='C:\Users\Anna\Projects\honors\data\obamatweets_daily.csv'
sentiment=pd.read_csv(sentfile, sep='\t', parse_dates=['date'])
s=sentiment.set_index('date', drop=False)
polls=pd.read_csv('C:\Users\Anna\Projects\honors\data\\favorable_data.csv', sep='\t', parse_dates=['enddate'])
polls=polls.set_index('enddate', drop=False)

#functions for computing time based moving-average
def daily_estimate(ts, ctr, win):
	win=timedelta(win/2)
	ser=ts[(ts.index>=ctr-win) & (ts.index<=ctr+win)]
	print ser	
	return ser.mean()

def moving_average(ts, win): 
	start=min(ts.index)
	end=max(ts.index)
	dates=pd.date_range(start, end)
	mas=[]
	for date in dates:
		mas.append(daily_estimate(ts, date, win))
	return Series(mas, index=dates)

#getting point estimates for polls
ma_fav=moving_average(polls.favorable, 3)
ma_unfav=moving_average(polls.unfavorable, 3)
ma_other=moving_average(polls.other, 3)

#join er'ry thing together
data=DataFrame({'favorable': ma_fav, 'unfavorable': ma_unfav, 'other': ma_other,'difference': ma_fav-ma_unfav, 'positive': s.positive, 'negative': s.negative, 'neutral': s.neutral, 'sentiment': s.sentiment})

#try different lags
favcorrs=[]
unfavcorrs=[]
diffcorrs=[]
lags=[]

for x in xrange(-90, 90): 
	data['lag']=data.sentiment.shift(x)
	lags.append(x) 
	favcorrs.append(data.corr()['lag']['favorable'])
	diffcorrs.append(data.corr()['lag']['difference'])
	unfavcorrs.append(data.corr()['lag']['unfavorable'])

favcorrs=Series(favcorrs, index=lags)
unfavcorrs=Series(unfavcorrs, index=lags)
diffcorrs=Series(diffcorrs, index=lags)

lagged_corrs=DataFrame({'favorable': favcorrs, 'unfavorable': unfavcorrs, 'difference': diffcorrs})
lagged_corrs.to_csv('data\lexicon_lagged_corrs.csv', sep='\t')