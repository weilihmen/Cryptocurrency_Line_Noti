import json
import schedule
import time
import datetime

from linebot import LineBotApi
from linebot.models import TextSendMessage

import crypt_api

#讀入設定參數
with open("data/setting.txt", "r") as json_file:  
  setting = json.load(json_file)
  mode=setting[0]["MODE"]
  params_1=setting[1]["params_1"]
  params_2=setting[2]["params_2"]
  params_3=setting[3]["params_3"]

#讀入LINE BOT序號
with open("data/line_bot_secrets.txt", "r") as json_file:
  secrets = json.load(json_file)
  channel_access_token =secrets[0]["Secret"]
  your_id=secrets[0]["ID"]

#Line bot參數設定，及傳遞訊息涵式
line_bot_api = LineBotApi(channel_access_token)
def noti(data):
  for i in data:
    srt=""
    for l in i:
      srt+=l+":"+i[l]+","
    print("send:",srt.rstrip(",")) 
    line_bot_api.push_message(your_id, TextSendMessage(text=srt.rstrip(",")))
  return True

#轉換成要傳送的資料(dict格式)
def parse(title,data):
  new_data=[]
  new_data.append({title:time.strftime("%Y/%m/%d %H:%M")})
  for d in data:
    if "symbol" in d:
      new_data.append({"幣種":d["symbol"],"價格(TWD)":d["price_twd"],"一小時內變動(%)":d["percent_change_1h"]})
    else:
      new_data.append(d)
  return new_data

#模式一
def mode1_job():
  fetch=crypt_api.rank_200()
  sets=[]
  for key in params_1:
    sets.append(key)
  #先篩出要的幣種資訊
  selected=crypt_api.selected_group(fetch,sets)
  raised=crypt_api.price_zone(selected,params_1)
  #如果有到價通知，再做下一步
  if raised:
    #讀取mode1的push紀錄(避免重複push)
    with open('data/mode1_data.txt', 'r') as json_file:
      data = json.load(json_file)
      updates,sends=crypt_api.check_updates(data, raised)
      if sends:
        message=parse("到價通知",sends)
        noti(message)
        print("完成到價通知(",time.strftime("%Y/%m/%d %H:%M"),")")
      else:
        print("無到價通知(",time.strftime("%Y/%m/%d %H:%M"),")")
    with open('data/mode1_data.txt', 'w') as json_file:
      json_file.write(json.dumps(updates))
  else:
    print("無到價通知(",time.strftime("%Y/%m/%d %H:%M"),")")

#模式二
def mode2_job():
  fetch=crypt_api.rank_200()
  selected=crypt_api.selected_group(fetch,params_2)
  message=parse("幣種定時通知",selected)
  noti(message)
  print("下一次通知:",datetime.datetime.now()+datetime.timedelta(hours = 1))

#模式三
def mode3_job():
  fetch=crypt_api.rank_200()
  tops,lasts=crypt_api.rising_and_falling(fetch,params_3[0],params_3[1])
  raw_message=tops+[{"Rank區間":("前"+str(params_3[1])+"幣種...")}]+lasts
  message=parse("最大漲跌通報",raw_message)
  noti(message)
  print("下一次通知:",datetime.datetime.now()+datetime.timedelta(hours = 1))

if mode==1:
  #mode1到價通知: params給定追蹤的貨幣及上下界區間，每分鐘更新，如果超出界線會push訊息
  #請注意，雖然程式是每分鐘更新，但資料api來源「coinmarketcap」每種貨幣更新速率不一
  print('start_mode_1')
  mode1_job()
  schedule.every().minutes.do(mode1_job)
elif mode==2:
  #mode2幣種通知: 給定幣種、每小時更新
  print('start_mode_2')
  mode2_job()
  schedule.every().hours.do(mode2_job)
elif mode==3:
  #mode3最大漲跌通報: 給定Rank的範圍(x)及排行數量(y)
  #則每小時會回報 在Rank 0~x範圍內，最大漲幅共y名、最大跌幅共y名
  print('start_mode_3')
  mode3_job()
  schedule.every().hours.do(mode3_job)
else:
  print("wrong params")

while True:
    schedule.run_pending()
    time.sleep(1)