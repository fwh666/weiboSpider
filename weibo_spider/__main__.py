import os
import sys
import schedule
import time
from absl import app
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
from weibo_spider.spider import main
# def schedule_job():
#     # schedule.every(10).minutes.do(job)
#     schedule.every(1).hours.do(job)
#     # schedule.every(1).seconds.do(job)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)
# def job():
#     # print("开始采集")
#     app.run(main)
# print('[程序启动...微博每一小时采集]')
# schedule_job()

print('[程序启动...微博开始采集一次]')
app.run(main)
