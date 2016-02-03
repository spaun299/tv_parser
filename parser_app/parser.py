#!/usr/bin/env python
# -*- coding: ascii -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import config
import os
from db_init import db, sql_connection
from .models import SaveRecordsToDb


class SeleniumWebDriver(object):

    def __init__(self, url=config.MAIN_PARSE_URL):
        self.driver = self.get_phantomjs_driver()
        self.url = url

    @staticmethod
    def get_channel_xpath():
        return "//div/div[@class='tv-grid__items']/div[@class='tv-grid__page']/div" \
               "[@class='tv-grid__item tv-grid__item_is-now_no']/div[@class='tv-channel']/" \
               "div[@class='tv-channel__title']/div/div[@class='tv-channel-title__link']/a"

    @staticmethod
    def get_channel_css_selector():
        return 'div.tv-channel__title > div[class$="tv-channel-title_js_inited"] > div.tv-channel-title__link > a'

    def get_background_image(self, selector):
        return self.driver.execute_script("""
                var element = arguments[0],
                style = element.currentStyle || window.getComputedStyle(element, false);
                return style.backgroundImage.slice(4, -1);
                """, selector)

    @staticmethod
    def get_phantomjs_driver():
        conf = dict(service_args=['--ssl-protocol=any'])
        if os.environ.get('OPENSHIFT_DATA_DIR'):
            # conf['service_log_path'] = os.environ.get('OPENSHIFT_PYTHON_LOG_DIR')+'/ghostdriver.log'
            # conf['executable_path'] = os.environ.get('OPENSHIFT_DATA_DIR') + '/phantomjs/bin/phantomjs'
            # conf['service_args'].append('--webdriver={ip}:15002'.format(ip=os.environ.get('OPENSHIFT_PYTHON_IP')))
            capabilities = dict(browserName='phantomjs', acceptSslCerts=True, javascriptEnabled=True)
            driver = webdriver.Remote(command_executor='http://'+os.environ.get('OPENSHIFT_PYTHON_IP')+':15005',
                                      desired_capabilities=capabilities)
            return driver
        driver = webdriver.PhantomJS(**conf)
        return driver

    def run(self):
        self.driver.get(self.url)
        self.driver.set_window_size(1920, 1080)
        page_height = 0
        elements = {}
        scroll_height_script = """ return window.innerHeight + window.scrollY """
        count = 0
        SaveRecordsToDb.get_channel_id_and_url()
        while (page_height != self.driver.execute_script(scroll_height_script)) and count!=1:
            page_height = self.driver.execute_script(scroll_height_script)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            for a in self.driver.find_elements_by_css_selector(self.get_channel_css_selector()):
                name = a.find_element_by_css_selector('span.tv-channel-title__text').text
                href = a.get_attribute('href').encode('ascii', 'ignore')
                icon = self.get_background_image(a.find_element_by_css_selector('div.tv-channel-title__icon > '
                                                 'span[class$="image_type_channel"] > span')).encode('ascii', 'ignore')
                if (href is not None) and (href not in elements.keys()):
                    elements[href] = {'name': name, 'icon': icon}
            time.sleep(1)
            count = 1
        save_records = SaveRecordsToDb()
        save_records.save_to_db(elements)

