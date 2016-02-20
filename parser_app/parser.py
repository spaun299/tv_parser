#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import config
import os
import datetime
from utils.date_and_time import get_date_time
import re
import json
from utils.send_email import SendEmail
from .models import SaveRecordsToDb, GetRecordsFromDb, Channel, TvProgram
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
            capabilities = dict(browserName='phantomjs', acceptSslCerts=True,
                                javascriptEnabled=True)
            driver = webdriver.Remote(command_executor='http://'+os.environ.get(
                'OPENSHIFT_PYTHON_IP')+':15005', desired_capabilities=capabilities)
            return driver
        driver = webdriver.PhantomJS(**conf)
        return driver

    def parse_url_channels(self):

        page_height = 0
        elements = {}
        count = 0
        count1 = 0
        scroll_height_script = """ return window.innerHeight + window.scrollY """
        while page_height != self.driver.execute_script(scroll_height_script):
            page_height = self.driver.execute_script(scroll_height_script)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            count += 1
        print('page height', str(count))
        for a in self.driver.find_elements_by_css_selector(self.get_channel_css_selector()):
            name = a.find_element_by_css_selector('span.tv-channel-title__text').text
            href = a.get_attribute('href').encode('ascii', 'ignore')
            icon = self.get_background_image(a.find_element_by_css_selector(
                    'div.tv-channel-title__icon > span[class$="image_type_channel"] > span')).\
                    encode('ascii', 'ignore')
            if (href is not None) and (href not in elements.keys()):
                elements[href] = {'name': name, 'icon': icon}
            count1 += 1
        print('elements', str(count1))
        save_records = SaveRecordsToDb()
        elements_count = save_records.save_channels_to_db(elements)
        send_email(subject='Parser notification',
                   text='Url channels parsed successfully.{elements_count} new channels'.format(
                       elements_count=elements_count))

    def parse_tv_programs(self):
        ids_and_links = GetRecordsFromDb().get_channels_id_and_link()
        date_today = get_date_time()
        for id_and_link in ids_and_links:
            channel = Channel(channel_id=id_and_link['id'])
            channel.update()
            self.driver.get(id_and_link['link'])
            time.sleep(5)
            if '404' not in self.driver.title:
                if not channel.description or not channel.web_site:
                    channel_description = self.driver.find_elements_by_css_selector(
                        "tr.b-row div.b-tv-channel-content__text")
                    channel_description = channel_description[0].text if channel_description else \
                        "This channel does not have description"
                    channel_web_site = self.driver.find_elements_by_css_selector(
                        "div.b-tv-channel-content__channel-info > "
                        "div.b-tv-channel-content__links > a")
                    channel_web_site = channel_web_site[0].get_attribute('href') \
                        if channel_web_site else "This channel does not have web site"
                    if len(channel_description) > Channel.description['length']:
                        channel_description = channel_description[:Channel.description['length']]
                    if len(channel_web_site) > Channel.web_site['length']:
                        channel_web_site = channel_web_site[:Channel.web_site['length']]
                    channel.description, channel.web_site = channel_description, channel_web_site
                    channel.update()
                dates_of_week = list()
                for date in self.driver.find_elements_by_css_selector(
                        'div.tv-filter-days__viewport > div.tv-filter-days__items > '
                        'div.tv-filter-days__item'):
                    date_of_week = re.findall(r'(\d{4}-\d{2}-\d{2})T',
                                              date.get_attribute('data-bem'))[0]
                    if datetime.datetime.strptime(date_today, '%Y-%m-%d') <= \
                            datetime.datetime.strptime(date_of_week, '%Y-%m-%d'):
                        dates_of_week.append(date_of_week)
                dates_of_week = dates_of_week[:7] if len(dates_of_week) > 7 else dates_of_week
                for day in dates_of_week:
                    self.driver.get("%(channel_link)s?date=%(date)s" %
                                    {'channel_link': id_and_link['link'], 'date': day})
                    time.sleep(1)
                    channels_tags = self.driver.find_elements_by_css_selector(
                        'div.b-tv-channel-schedule__items > div.b-tv-channel-schedule__item > a')
                    tv_channels = []
                    for channel in channels_tags:
                        program_name = channel.find_element_by_class_name(
                            'tv-event__title-inner').text
                        show_time = channel.find_element_by_class_name('tv-event__time-text').text + ':00'
                        show_date = datetime.datetime.strptime(day, '%Y-%m-%d')
                        # genre = re.findall(ur'genre\W+(\w+)', channel.get_attribute('data-bem'))
                        genre = json.loads(channel.get_attribute('data-bem'))['tv-event']['genre']
                        tv_channels.append(TvProgram(name=program_name, genre=genre,
                                                     show_date=show_date, show_time=show_time))
                    SaveRecordsToDb.save_programs(id_and_link['id'], tv_channels)
                    send_email(subject='Parser notification',
                               text='Tv programs parsed successfully.')

            else:
                send_email(subject='Page not found',
                           text='Page {page} not found'.format(page=self.driver.current_url))
