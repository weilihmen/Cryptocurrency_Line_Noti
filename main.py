import json
import requests
import schedule
import time
import datetime

from linebot import LineBotApi
from linebot.models import TextSendMessage

import crypt_api

with open('data/setting.txt', 'r') as json_file:  
    setting = json.load(json_file)

mode=setting[0]['MODE']
params=setting[1]['params']
print(params)
#with open('data/secret.txt', 'r') as json_file:
#  secret = json.load(json_file)



line_bot_api = LineBotApi('')
def notification(content):
  line_bot_api.push_message('to', TextSendMessage(text=content))
  return True

def mode1_job():
  new_fetch=crypt_api.rank_200()
  filters=[]
  for key in params:
    filters.append(key)
  #先篩出要的幣種資訊 如果有讀取失敗就print警告
  selected,unrecognized=crypt_api.selected_group(new_fetch,filters)
  if len(unrecognized)>0:
    print("警告: 有未知幣種",unrecognized)
  raised=crypt_api.price_zone(selected,params)
  print('raised:',raised)
  #讀取mode1的push紀錄(避免重複push)
  with open('data/mode1_data.txt', 'r') as json_file:
    data = json.load(json_file)
    print(type(data))
    updates,sends=crypt_api.check_updates(data, raised)
    print('updates:',updates,'\n,send:',sends)
  with open('data/mode1_data.txt', 'w') as json_file:
    json_file.write(json.dumps(updates))


if mode==1:
  #mode1到價通知: params給定追蹤的貨幣及上下界區間，每分鐘更新，如果超出界線會push訊息
  #請注意，雖然程式是每分鐘更新，但資料api來源「coinmarketcap」每種貨幣更新速率不一
  print('start!!')
  mode1_job()
elif mode==2:
  print("2")
elif mode==3:
  print("3")
else:
  print("wrong params")

