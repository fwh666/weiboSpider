import schedule
import time
import subprocess

def job():
    # print("I'm working...")
    # print("I'm working...")
    # command="sh /Users/fwh/fuwenhao/Github/weiboSpider/weibo_spider/test.sh"
    command="sh /Users/fwh/fuwenhao/Github/weiboSpider/fwh_start.sh"
    subprocess.call(command, shell=True)
    


def schedule_job():
    # schedule.every(1).seconds.do(job)
    # schedule.every(10).minutes.do(job)
    schedule.every(1).hours.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    print('[程序启动...]')
    # 调用定时任务函数
    schedule_job()