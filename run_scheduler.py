from apscheduler.schedulers.background import BackgroundScheduler
import time
from parser_app.parser import SeleniumWebDriver
from utils.send_email import SendEmail
import schedule

driver = SeleniumWebDriver()
send_email = SendEmail().send_email


def run_scheduler():
    try:
        # driver.parse_url_channels()
        driver.parse_tv_programs()
        schedule.every(1).monday.at('"06:00"').do(driver.parse_tv_programs)
        schedule.every(20).days.do(driver.parse_url_channels)
        while True:
            schedule.run_pending()
            time.sleep(2)
    except Exception as e:
        send_email(subject='Parse error. Exception' , exception=e)

if __name__ == '__main__':
    run_scheduler()
