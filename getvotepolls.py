import requests
import csv

baseurl='http://elections.huffingtonpost.com/pollster/api/polls.json'
payload=dict()
payload['state']='US'
payload['chart']='2012-general-election-romney-vs-obama'
payload['page']=1
payload['before']='2012-11-07'
payload['after']='2012-06-01'

def process_favorable_responses(responses):
  resdict={'favorable':0, 'unfavorable':0, 'other':0}
  for response in responses:
    if 'unfavorable' in response['choice'].lower() or 'negative' in response['choice'].lower():
      resdict['unfavorable']+=response['value']/100.0
    elif 'favorable' in response['choice'].lower() or 'positive' in response['choice'].lower():
      resdict['favorable']+=response['value']/100.0
    else:
      resdict['other']+=response['value']/100.0
      print response['choice']
  return resdict

def process_vote_responses(responses):
  resdict={'other':0}
  for response in responses:
      if 'obama' in response['choice'].lower():
        resdict['obama']=response['value']/100.0
      elif 'romney' in response['choice'].lower():
        resdict['romney']=response['value']/100.0
      else:
          resdict['other']+=response['value']/100.0
  return resdict

if __name__=='__main__':
  rows=[]
  r=requests.get(baseurl, params=payload)
  data=r.json()
  while data!=[]:
    for poll in data:
      for question in poll['questions']:
        if question['chart']!='2012-general-election-romney-vs-obama':
          continue
        for subpopulation in question['subpopulations']:
          resdict=process_vote_responses(subpopulation['responses'])
          rows.append(
            [poll['start_date'], poll['end_date'], poll['pollster'], poll['method'], poll['source'], 
            subpopulation['name'], resdict['obama'], resdict['romney'], resdict['other']]
            )
    payload['page']+=1
    r=requests.get(baseurl, params=payload)
    data=r.json()

  with open('vote_data.csv', 'wb') as csvfile:
    writer=csv.writer(csvfile, delimiter='\t')
    writer.writerow('start_date', 'end_date', 'pollster', 'method', 'source', 'subpopulation', 'obama', 'romney', 'other')
    for row in rows:
      writer.writerow(row)