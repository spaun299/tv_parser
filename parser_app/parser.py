from selenium import webdriver
from flask import g
from selenium.webdriver.common.keys import Keys
import time

class SeleniumWebDriwer(object):
    def __init__(self,
                 driver=webdriver.PhantomJS(service_args=['--ssl-protocol=any']),
                 url='https://tv.yandex.ru'):
        self.driver = driver
        self.url = url

    def run(self):
        self.driver.get(self.url)
        self.driver.set_window_size(1920, 1080)
        # c = self.driver.find_elements_by_xpath("//div[@class='tv-grid__item']/div[@class='tv-channel']")
        page_height = 0

        scroll_height_script = """ return window.innerHeight + window.scrollY """
        print(self.driver.get(self.url))
        while page_height != self.driver.execute_script(scroll_height_script):
            page_height = self.driver.execute_script(scroll_height_script)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
