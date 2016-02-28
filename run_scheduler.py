from utils.log import write_to_log
import time
from parser_app.parser import SeleniumWebDriver
from utils.send_email import SendEmail
import schedule
import subprocess
from utils.bash_scripts import get_pid_by_name, kill_process

driver = SeleniumWebDriver()
send_email = SendEmail().send_email


def run_scheduler():
    try:
        write_to_log('Run scheduler')
        # if type_of_parser == 'channels':
        #     write_to_log('Preparing to parse channels')
        driver.parse_url_channels()
        # elif type_of_parser == 'programs':
        #     write_to_log('Preparing to parse programs')
        #     driver.parse_tv_programs()
        schedule.every().day.at("14:23").do(driver.parse_url_channels)
        schedule.every().day.at("14:55").do(driver.parse_tv_programs)
        # schedule.every().monday.at('"06:00"').do(driver.parse_tv_programs)
        # schedule.every().sunday.at("'12:00'").do(driver.parse_url_channels)
        while True:
            schedule.run_pending()
            time.sleep(2)
        # else:
        #     subprocess.Popen("echo Unknown argument for parser."
        #                      "Type --help for more information".split())
    except Exception as e:
        write_to_log(error=e)
        send_email(subject='Parse error. Exception', exception=e)
        write_to_log('Kill scheduler after error')
        kill_process(get_pid_by_name('run_scheduler.py'))

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('type', help='Parser type: channels or programs')
    # args = parser.parse_args()
    # type_of_parser = args.type.split("=")[-1]
    run_scheduler()
