from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import config
import os


class SeleniumWebDriver(object):

    def __init__(self, url=config.MAIN_PARSE_URL):
        self.driver = webdriver.PhantomJS(**self.phantomjs_config())
        self.url = url

    @staticmethod
    def phantomjs_config():
        conf = dict(service_args=['--ssl-protocol=any'])
        if os.environ.get('OPENSHIFT_DATA_DIR'):
            conf['service_log_path'] = os.environ.get('OPENSHIFT_PYTHON_LOG_DIR')+'/ghostdriver.log'
            conf['executable_path'] = os.environ.get('OPENSHIFT_DATA_DIR') + '/phantomjs'
        return conf

    def run(self):
        self.driver.get(self.url)
        self.driver.set_window_size(1920, 1080)
        page_height = 0
        scroll_height_script = """ return window.innerHeight + window.scrollY """

        while page_height != self.driver.execute_script(scroll_height_script):
            page_height = self.driver.execute_script(scroll_height_script)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            for a in self.driver.find_elements_by_class_name('tv-channel-title__link'):
                print(a.text)
            time.sleep(5)
        channels_title_div = self.driver.find_elements_by_class_name('tv-channel-title__link')
        channels_url = map(lambda div: div.get_attribute('href'), filter(lambda href: href.get_attribute('href'),
                           channels_title_div))
