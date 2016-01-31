import config
from parser_app.parser import SeleniumWebDriver
from apscheduler.schedulers.background import BackgroundScheduler
import time
driver = SeleniumWebDriver()


def run_app():
    scheduler = BackgroundScheduler()
    scheduler.add_job(driver.run, 'interval', seconds=10, id=str(time.time()))
    scheduler.start()
    driver.run()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()

if __name__ == '__main__':
    run_app()
