import requests
import json

#抓Rank200內的資料
def rank_200():
	req = requests.request('GET', 'https://api.coinmarketcap.com/v1/ticker/?convert=TWD')
	req2 = requests.request('GET', 'https://api.coinmarketcap.com/v1/ticker/?convert=TWD&start=100&limit=100')
	data = json.loads(req.text)
	for coin in json.loads(req2.text):
		data.append(coin)
	return data

#取得一小時內漲與跌最大的幣種(以Rank為範圍)
#num取排行的數量、group_size為rank的範圍
def rising_and_falling(data,top_size,rank_size):
	new_data=data[:(rank_size-1)]
	newlist = sorted(new_data, key=lambda x: (float(x["percent_change_1h"]) >= 0, (float(x["percent_change_1h"])))) 
	return list(reversed(newlist[-(top_size):])),list(reversed(newlist[:top_size]))

#取得特定幣種資訊 filters放入幣種簡稱
def selected_group(data,sets):
	selected=[]
	recognized=[]
	for coin in data:
		for name in sets:
			if coin['symbol']==name:
				selected.append(coin)
				recognized.append(name)
	for name in sets:
		if name not in recognized:
			print("Alert: Unknown",name)
	return selected

#到價通知
#condition是dict，格式->{"幣種1名稱":["上界數字","下界數字""], "第二幣種":["上界數字","下界數字"]...以此類推}
#return符合條件的到價資訊，如果沒有的話return false
def price_zone(data,condition):
	raised=[]
	for data_coin in data:
		if float(data_coin['price_twd']) > float(condition[data_coin['symbol']][0]) or float(data_coin['price_twd']) < float(condition[data_coin['symbol']][1]):
			raised.append(data_coin)
	if len(raised)>0:
		return raised
	else:
		return False

#到價通知後 讀入前一次push紀錄(避免重複push)
#比對資訊，return:更新的push紀錄 與 需要傳送的資料
def check_updates(data,new_data):
	deletes_a=[]
	deletes_b=[]
	for l in data:
		for r in new_data:
			if l['symbol']==r['symbol']:
				if int(l['last_updated'])==int(r['last_updated']):
					deletes_b.append(r)
					pass
				else:
					deletes_a.append(l)
					pass
			pass
	for d in deletes_a:
		data.remove(d)
	for d in deletes_b:
		new_data.remove(d)
	for r in new_data:
		data.append(r)
	return data,new_data

