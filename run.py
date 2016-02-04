import datetime
from parser_app.parser import SeleniumWebDriver
from apscheduler.schedulers.background import BackgroundScheduler
import time
from utils.decorators import function_time
driver = SeleniumWebDriver()


@function_time
def run(*args):
    driver.run()
    # print(args)
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(driver.run, 'interval', seconds=10, id=str(time.time()))
    # scheduler.start()
    # driver.run()
    # try:
    #         This is here to simulate application activity (which keeps the main thread alive).
        # while True:
        #     time.sleep(2)
    # except (KeyboardInterrupt, SystemExit):
    #         Not strictly necessary if daemonic mode is enabled but should be done if possible
        # scheduler.shutdown()
if __name__ == '__main__':
    run()
