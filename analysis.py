import pandas as pd
import statsmodels.api as sm
from pandas import DataFrame, Series
from datetime import timedelta, datetime
import sys, os

sentfile='C:\Users\Anna\Projects\honors\data\\' + sys.argv[1]
sentiment=pd.read_csv(sentfile, sep='\t', parse_dates=['date'])
s=sentiment.set_index('date', drop=False)
polls=pd.read_csv('C:\Users\Anna\Projects\honors\data\\favorable_data.csv', sep='\t', parse_dates=['enddate'])
polls=polls.set_index('enddate', drop=False)
vote=pd.read_csv('C:\Users\Anna\Projects\honors\data\\vote_data.csv', sep='\t', parse_dates=['enddate'])
vote=vote.set_index('enddate', drop=False)
approval=pd.read_csv('C:\Users\Anna\Projects\honors\data\\approval_data.csv', sep='\t', parse_dates=['enddate'])
approval=approval.set_index('enddate', drop=False)
#functions for computing time based moving-average
def daily_estimate(ts, ctr, win):
	win=timedelta(win/2)
	ser=ts[(ts.index>=ctr-win) & (ts.index<=ctr+win)]	
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
ma_fav=moving_average(polls.favorable, 5)
ma_unfav=moving_average(polls.unfavorable, 5)
ma_other=moving_average(polls.other, 5)
ma_ovote=moving_average(vote.obama,5)
ma_rvote=moving_average(vote.romney,5)
ma_oapprov=moving_average(approval.approve, 5)
ma_disapprov=moving_average(approval.disapprove, 5)

#join er'ry thing together, apply different smoothing to sentiment. 
lglist=[]
for k in [7, 15, 30]:
	ma_sent=moving_average(s.sentiment, k)
	data=DataFrame({'favorable': ma_fav, 'unfavorable': ma_unfav, 'other': ma_other,'difference': ma_fav-ma_unfav, 
					'positive': s.positive, 'negative': s.negative, 'sentiment': s.sentiment, 'ma_sentiment': ma_sent,
					'ovote': ma_ovote, 'rvote': ma_rvote, 'votediff': ma_ovote-ma_rvote, 
					'approval': ma_oapprov, 'disapprove': ma_disapprov, 'appdiff': ma_oapprov - ma_disapprov})

	#try different lags
	favcorrs=[]
	unfavcorrs=[]
	diffcorrs=[]
	approvcorrs=[]
	disappcorrs=[]
	appdiffcorrs=[]
	ovotecorrs=[]
	rvotecorrs=[]
	votediffcorrs=[]
	lags=[]

	for x in xrange(-90, 90): 
		data['lag']=data.ma_sentiment.shift(x)
		lags.append(x) 
		favcorrs.append(data.corr()['lag']['favorable'])
		diffcorrs.append(data.corr()['lag']['difference'])
		unfavcorrs.append(data.corr()['lag']['unfavorable'])

	favcorrs=Series(favcorrs, index=lags)
	unfavcorrs=Series(unfavcorrs, index=lags)
	diffcorrs=Series(diffcorrs, index=lags)

	lagged_corrs=DataFrame({'favorable': favcorrs, 'unfavorable': unfavcorrs, 'difference': diffcorrs})
	lagged_corrs.to_csv(os.path.join('data', 'lexicon_lagged_corrs' + str(k) + '.csv'), sep='\t')
	lglist.append(lagged_corrs)

sm7_laggedcorrs=lglist[0]
sm15_laggedcorrs=lglist[1]
sm30_laggedcorrs=lglist[2]

y=data.ma_sent.dropna()
armodel=sm.tsa.ar_model.AR().fit(y)