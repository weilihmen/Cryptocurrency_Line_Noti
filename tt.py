import schedule
import datetime

def job():
    print("I'm working...")
    print(datetime.datetime.now())

schedule.every(2).minutes.do(job)

while True:
    schedule.run_pending()


#http://neven.me/python/2017/04/25/Python%E5%AE%9E%E7%8E%B0%E4%B8%80%E4%B8%AA%E7%AE%80%E5%8D%95%E7%9A%84%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1(sched%E5%AE%9E%E7%8E%B0%E5%88%86%E6%9E%90)/
#https://github.com/dbader/schedule
