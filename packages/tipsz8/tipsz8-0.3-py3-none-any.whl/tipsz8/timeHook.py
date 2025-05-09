from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# def start_scraping(task,):
#     print(1)
    # 在这里调用你的爬虫函数
    # your_scraper_module.start_scraping()print

def timeStart(cb,startToend,h=2):
    current_date = datetime.now().date().strftime("%Y-%m-%d") 
    t = startToend.split('-')
    start = current_date + " " + t[0]
    end = current_date + " " + t[1]
    scheduler = BlockingScheduler()
    
    scheduler.add_job(cb, 'cron', 'interval', hour='*/{}'.format(h), start_date=start, end_date=end)  # 每天凌晨2点执行三次
    # scheduler.add_job(start_scraping, 'interval', minutes=1)  # 每30分钟执行一次
    print("Scraping started...")
    scheduler.start()
    