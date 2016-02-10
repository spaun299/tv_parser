#!/usr/bin/env python
# -*- coding: ascii -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import config
import os
import datetime
from db_init import db, sql_connection
import json
from utils.send_email import SendEmail
from .models import SaveRecordsToDb, GetRecordsFromDb, Channel
from utils.decorators import send_email_decorator
send_email = SendEmail().send_email


class SeleniumWebDriver(object):

    def __init__(self, url=config.MAIN_PARSE_URL):
        self.driver = self.get_phantomjs_driver()
        self.url = url
        self.driver.get(self.url)
        self.driver.set_window_size(1920, 1080)
        assert url in self.driver.current_url, "Can't open url: %s" % url

    @staticmethod
    def get_channel_xpath():
        return "//div/div[@class='tv-grid__items']/div[@class='tv-grid__page']/div" \
               "[@class='tv-grid__item tv-grid__item_is-now_no']/div[@class='tv-channel']/" \
               "div[@class='tv-channel__title']/div/div[@class='tv-channel-title__link']/a"

    @staticmethod
    def get_channel_css_selector():
        return 'div.tv-channel > div.tv-channel__title > div > div.tv-channel-title__link > a'

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

    @send_email_decorator
    def parse_url_channels(self):

        page_height = 0
        elements = {}
        scroll_height_script = """ return window.innerHeight + window.scrollY """
        count = 0
        while (page_height != self.driver.execute_script(scroll_height_script)) and count != 1:
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
        elements_count = save_records.save_channels_to_db(elements)
        return 'Parser notification', \
               'Url channels parsed successfully.{elements_count} new channels'.format(elements_count=elements_count)

    @send_email_decorator
    def parse_tv_programs(self):
        ids_and_links = GetRecordsFromDb().get_channels_id_and_link()
        for id_and_link in ids_and_links:
            channel = Channel(channel_id=id_and_link['id'])
            channel.update()
            self.driver.get(id_and_link['link'])
            time.sleep(2)
            if '404' not in self.driver.title:
                if not channel.description or not channel.web_site:
                    channel_description = self.driver.find_elements_by_css_selector(
                                         "tr.b-row div.b-tv-channel-content__text")
                    channel_description = channel_description[0].text if channel_description else \
                        "This channel does not have description"
                    channel_web_site = self.driver.find_elements_by_css_selector(
                                         "div.b-tv-channel-content__channel-info > "
                                         "div.b-tv-channel-content__links > a")
                    channel_web_site = channel_web_site[0].get_attribute('href') if channel_web_site else \
                        "This channel does not have web site"
                    if len(channel_description) > Channel.description['length']:
                        channel_description = channel_description[:Channel.description['length']]
                    if len(channel_web_site) > Channel.web_site['length']:
                        channel_web_site = channel_web_site[:Channel.web_site['length']]
                    channel.description, channel.web_site = channel_description, channel_web_site
                    channel.update()
                dates = set()
                for date in self.driver.find_elements_by_css_selector('div.tv-filter-days__viewport > '
                                                                      'div.tv-filter-days__items > '
                                                                      'div.tv-filter-days__item'):
                    date_time = json.loads(date.get_attribute('data-bem'))['tv-filter-days__item']['value'].split(
                        'T')[0]
                    dates.add(date_time)
                print(dates)

            else:
                send_email(subject='Page not found',
                           text='Page {page} not found'.format(page=self.driver.current_url))
        return 'Parser notification', 'Tv programs parsed successfully.'
