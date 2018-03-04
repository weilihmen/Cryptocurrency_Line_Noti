# Cryptocurrency_Line_Noti

## [medium 詳細說明 連結](https://medium.com/@weilihmen/line-bot-%E5%8A%A0%E5%AF%86%E8%B2%A8%E5%B9%A3%E5%88%B0%E5%83%B9%E9%80%9A%E7%9F%A5-5f112c0c3231)

### 功能說明
（即時或定時推送加密貨幣資訊，金額採新台幣TWD計算）  
1. 到價通知：可以設定多種幣種，個別幣種指定價格上界與下界，每分鐘刷新資訊，如果該幣種價格超過上界與下界之間的區間，就會push訊息。  
![!missing picture!](https://cdn-images-1.medium.com/max/800/1*z7klqYV-pBvlPmwuHqHAdw.png)  
  
2. 特定幣種監控：設定多種幣種，定時(每小時)push最新的幣種價格。  
![!missing picture!](https://cdn-images-1.medium.com/max/800/1*Ix1fzG1Fb1XMYOhfLyzEDQ.png)  
  
3. 最大漲幅幣種：以設定的Rank(市值排行*)內，定時(每小時)push最大漲幅與最大跌幅的幣種資訊。  
![!missing picture!](https://cdn-images-1.medium.com/max/800/1*UcQYPj_cO5GtcxpUuUFh-g.png)  
*市值排行採”幣值”乘以”流通數量”  
------

### 使用說明
#### 設定line-bot token&id
在data/line_bot_secrets.txt 設定參數  
![!missing picture!](https://cdn-images-1.medium.com/max/800/1*ZatlMJt0SMHAF0fQtP3PNg.png)  
Secret 這邊寫入在Line Developer Console拿到的“channel access token”  
ID 這邊寫入在Line Developer Console拿到的“your user id”
  
#### 設定要使用的模式
在data/setting.txt 設定參數  
![!missing picture!](https://cdn-images-1.medium.com/max/800/1*GfKrUbXcWk-s2GsV5jO7GQ.png)  
MODE 1~3 依序分別是上面所提到的三種功能  
在MODE裡面依照選擇填入數字  
(目前只提供同時執行一個功能)  
  
params_1~3 依序則為三種模式的參數設定  
#請注意到，幣種的名稱一率採縮寫、大寫  
  
params_1 填入的內容為”監控幣種”:[”到價通知的上界與下界”]  
`#舉例而言`  
`"BTC":["320000","310000"]`  
`#=> 代表監控比特幣，價格會在大於320K及小於310K時push line message`  
`#請按照格式增添自己需要監控的幣種及價格區間`  
  
params_2 填入的內容為”監控幣種”  
`#舉例而言`  
`"BTC","ETH"`  
`#代表每小時會推送比特幣與乙太幣的價格資訊`  
  
params_3 填入的內容為“漲幅排名數量”,”監控的rank區間”  
`#舉例而言`  
`5,50`  
`#代表的是每小時會推送rank(市值)前"五十"名中，漲幅及跌幅最大各"五"名`  
  
#### 設定完成，執行main.py  
![!missing picture!](https://cdn-images-1.medium.com/max/800/1*iXyuZNmYsgXrKAP02vN4mw.png)  
  
------
  
####歡迎fork、歡迎打賞  
  
*BTC: 1EdY4v8mLupyjbJMZdxqN1rzLut2h44xxu*  
*ETH: 0xec241cfc97232781d753e471f68e65b360f0bfcf*  
*LTC: LWPGtcHbjNTGnzTkMjy5yKMqeqQpu4pPxu*  
  
  

