import schedule
import time

def job():
    print("I'm working...")

def schedule_job():
    # schedule.every(1).hours.do(job)
    schedule.every(1).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

# 调用定时任务函数
schedule_job()