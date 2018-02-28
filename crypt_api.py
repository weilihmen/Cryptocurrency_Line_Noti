import requests
import json

index01=200
index02=['BTC','RLC','TEL','PPP','WRONGTEST']

def rank_200():
	req = requests.request('GET', 'https://api.coinmarketcap.com/v1/ticker/')
	req2 = requests.request('GET', 'https://api.coinmarketcap.com/v1/ticker/?start=100&limit=100')
	new_data = json.loads(req.text)
	for a_coin in json.loads(req2.text):
		new_data.append(a_coin)
	return new_data

def group_rising_and_falling(data,num,group_size):
	group_data=data[:(group_size-1)]
	newlist = sorted(group_data, key=lambda x: (float(x["percent_change_1h"]) >= 0, (float(x["percent_change_1h"])))) 
	return newlist[-(num):],newlist[:num]

data=rank_200()
top,last=group_rising_and_falling(data, 3, 100)
print(top,last)

def selected_group(data,filter):
	#字串判斷

#https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=TWD
#BTC、ETH、LTC、





