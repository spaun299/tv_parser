from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import config


class SeleniumWebDriver(object):
    def __init__(self,
                 driver=webdriver.PhantomJS(service_args=['--ssl-protocol=any']),
                 url=config.MAIN_PARSE_URL):
        self.driver = driver
        self.url = url

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
