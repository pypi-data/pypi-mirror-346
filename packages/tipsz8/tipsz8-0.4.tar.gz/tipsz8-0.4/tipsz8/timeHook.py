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

def timeDay(cb,start,start1,start2):
    scheduler = BlockingScheduler()
    s = start.split(':')
    s1 = start1.split(':')
    s2 = start2.split(':')
    scheduler.add_job(cb, 'cron', hour=s[0], minute=s[1],second=s[2])  # 每天凌晨2点执行三次
    scheduler.add_job(cb, 'cron', hour=s1[0], minute=s1[1],second=s1[2])  # 每天凌晨2点执行三次
    scheduler.add_job(cb, 'cron', hour=s2[0], minute=s2[1],second=s2[2])  # 每天凌晨2点执行三次
    # scheduler.add_job(start_scraping, 'interval', minutes=1)  # 每30分钟执行一次
    print(f"Scraping started {start}...")
    print(f"Scraping started {start1}...")
    print(f"Scraping started {start2}...")
    scheduler.start()
    