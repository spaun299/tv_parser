from utils.log import write_to_log
import time
from parser_app.parser import SeleniumWebDriver
from utils.send_email import SendEmail
import schedule
import subprocess

driver = SeleniumWebDriver()
send_email = SendEmail().send_email


def run_scheduler():
    try:
        write_to_log('Run scheduler')
        driver.parse_url_channels()
        driver.parse_tv_programs()
        schedule.every().monday.at('"06:00"').do(driver.parse_tv_programs)
        schedule.every().sunday.at("'12:00'").do(driver.parse_url_channels)
        while True:
            schedule.run_pending()
            time.sleep(2)
    except Exception as e:
        write_to_log(error=e)
        send_email(subject='Parse error. Exception', exception=e)
        bash_command = "ps -eaf | grep -v grep | grep run_scheduler.py " \
                       "| grep -v $$ | awk '{ print $2 }'"
        output = subprocess.check_output(['bash', '-c', bash_command])
        bash_command = "kill -SIGKILL %s" % int(output)
        write_to_log('Kill scheduler after error')
        subprocess.Popen(bash_command.split())


if __name__ == '__main__':
    run_scheduler()
