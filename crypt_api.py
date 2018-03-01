import requests
import json

index01=200
index02=['BTC','RLC','TEL','PPP','WRONGTEST']

def rank_200():
	req = requests.request('GET', 'https://api.coinmarketcap.com/v1/ticker/?convert=TWD')
	req2 = requests.request('GET', 'https://api.coinmarketcap.com/v1/ticker/?convert=TWD&start=100&limit=100')
	new_data = json.loads(req.text)
	for coin in json.loads(req2.text):
		new_data.append(coin)
	return new_data

def group_rising_and_falling(data,num,group_size):
	group_data=data[:(group_size-1)]
	newlist = sorted(group_data, key=lambda x: (float(x["percent_change_1h"]) >= 0, (float(x["percent_change_1h"])))) 
	return newlist[-(num):],newlist[:num]

def selected_group(data,filters):
	selected=[]
	recognized=[]
	unrecognized=[]
	for coin in data:
		for name in filters:
			if coin['symbol']==name:
				selected.append(coin)
				recognized.append(name)
	for name in filters:
		if name not in recognized:
			unrecognized.append(name)
	return selected,unrecognized

data=rank_200()
#top,last=group_rising_and_falling(data, 3, 100)
#print(top,last)

#condition是dict，格式->{'幣種1名稱':['上界數字','下界數字'], '第二幣種':['上界數字','下界數字']...以此類推}
#return符合條件的到價資訊，如果沒有的話return false
def price_zone(data,condition):
	raised=[]
	for data_coin in data:
		if float(data_coin['price_twd']) > float(condition[data_coin['symbol']][0]) or float(data_coin['price_twd']) < float(condition[data_coin['symbol']][1]):
			raised.append(data_coin)
	if len(raised)>0:
		return raised
	else:
		return false

#讀入前一次push紀錄(避免重複push)
#比對資訊，return:更新的push紀錄 與 需要傳送的資料
def check_updates(last_updates,raised):
	i=0
	while i<len(last_updates)-1:
		for r in raised:
			if last_updates[i]['symbol']==r['symbol']:
				last_updates.append(r)
				if r['last_updated']>last_updates[i]['last_updated']:
					last_updates.pop(i)
					print('replace')
				else:
					raised.pop(r)
					print('send')
		i=i+1
	return last_updates,raised










#https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=TWD
#BTC、ETH、LTC、
