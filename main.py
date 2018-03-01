#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import schedule

from linebot import LineBotApi
from linebot.models import TextSendMessage

import crypt_api

with open("data/setting.txt", "r") as json_file:  
  setting = json.load(json_file)

mode=setting[0]["MODE"]
params_1=setting[1]["params_1"]
params_2=setting[2]["params_2"]
params_3=setting[3]["params_3"]

line_bot_api = LineBotApi('')
def notification(content):
  line_bot_api.push_message('to', TextSendMessage(text=content))
  return True

def parse(data):
  parsed=[]
  for d in data:
    parsed.append({"Coin":d["symbol"],"Price":d["price_twd"],"Change_1H(%)":d["percent_change_1h"]})
  return parsed

def mode1_job():
  new_fetch=crypt_api.rank_200()
  filters=[]
  for key in params_1:
    filters.append(key)
  #先篩出要的幣種資訊
  selected=crypt_api.selected_group(new_fetch,filters)
  raised=crypt_api.price_zone(selected,params_1)
  #如果有到價通知，再做下一步
  if raised!=False:
    #讀取mode1的push紀錄(避免重複push)
    with open('data/mode1_data.txt', 'r') as json_file:
      data = json.load(json_file)
      updates,sends=crypt_api.check_updates(data, raised)
      sends=parse(sends)
      print("Push:",sends)#noti
    with open('data/mode1_data.txt', 'w') as json_file:
      json_file.write(json.dumps(updates))

def mode2_job():
  new_fetch=crypt_api.rank_200()
  filters=params_2
  data=crypt_api.selected_group(new_fetch,filters)
  data=parse(data)
  print("Push",data)

def mode3_job():
  new_fetch=crypt_api.rank_200()
  filters=params_3
  tops,lasts=crypt_api.rising_and_falling(new_fetch,filters[0],filters[1])

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

