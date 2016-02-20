from apscheduler.schedulers.background import BackgroundScheduler
import time
from parser_app.parser import SeleniumWebDriver
from utils.send_email import SendEmail
import schedule

# successfull = True
# try:
#     driver.parse_url_channels()
# except Exception as e:
#     successfull = False
#     send_email(exception=e)
# finally:
#     print(successfull)
#     template, msg = message_for_email(successfull=successfull)
#     return render_template(template, **msg)

driver = SeleniumWebDriver()
send_email = SendEmail().send_email


def run_scheduler():
    schedule.every(1).hours.do(driver.parse_url_channels)
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(driver.parse_url_channels, trigger='cron', id=str(time.time()),
    #                   args=('*/1 * * * *',))
    # scheduler.add_job(driver.parse_tv_programs, 'interval', seconds=10, id=str(time.time()))
    # try:
    #     scheduler.start()
    # except Exception as e:
    #     send_email(exception=e)
    # try:
    #     while True:
    #         time.sleep(2)
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()
    while True:
        schedule.run_pending()
        time.sleep(2)

if __name__ == '__main__':
    run_scheduler()
