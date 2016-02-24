# -*- coding: ascii -*-
from db_init import db, sql_connection
import time
import datetime


class SaveRecordsToDb(object):
    def __init__(self):
        pass

    def save_channels_to_db(self, dict_of_elements):
        elements_count = 0
        self.insert_icons_into_files([link['icon'] for link in dict_of_elements.values()
                                      if link['icon']])
        for element in dict_of_elements.keys():
            db.execute(""" SELECT COUNT(id) FROM channels WHERE link='{link}'
                           OR name='{name}' """.format(
                link=element, name=dict_of_elements[element]['name']))
            if db.fetchone()[0] == 0:
                db.execute(""" INSERT INTO channels(name, link, icon_id)
                              VALUES ('{name}', '{link}',
                              (SELECT id FROM files WHERE file_link='{file_link}')); """.
                           format(name=dict_of_elements[element]['name'],
                                  link=element, file_link=dict_of_elements[element]['icon']))
                elements_count += 1
        sql_connection.commit()
        return elements_count

    @staticmethod
    def save_programs(channel_id, list_of_programs_classes):
        db.executemany(""" INSERT INTO tv_programs(name, genre, show_date, show_time,
                           channel_id) VALUES(%(name)s, %(genre)s, %(show_date)s, %(show_time)s,
                            %(channel_id)s); """,
                       [{'name': cls.name, 'genre': cls.genre,
                         'show_date': cls.show_date, 'show_time': cls.show_time,
                         'channel_id': channel_id} for cls in list_of_programs_classes])
        sql_connection.commit()

    @staticmethod
    def insert_icons_into_files(list_of_links):
        db.execute(""" SELECT file_link FROM files WHERE file_link IN %(list_of_links)s; """ %
                   {'list_of_links': tuple(list_of_links)})
        links = [link['file_link'] for link in db.fetchall()]
        db.executemany(""" INSERT INTO files(file_link) VALUES(%(link)s); """,
                       [{'link': elem} for elem in list_of_links if elem not in links])
        sql_connection.commit()

    @staticmethod
    def update_table(table_name, item_id, key, value):
        db.execute(""" UPDATE %(table_name)s SET %(key)s='%(value)s' WHERE id=%(item_id)s;""" %
                   {'table_name': table_name, 'key': key, 'value': value, 'item_id': item_id})
        sql_connection.commit()

    def save(self, table_name):
        items = {key: value for key, value in self.__dict__.items() if (
            key in getattr(self, 'db_fields')) and value}
        fields_name = ",".join(items.keys())
        fields_value = "','".join(items.values())
        db.execute(""" INSERT INTO %(table_name)s(%(keys)s) VALUES ('%(values)s');""" %
                   {'table_name': table_name, 'keys': fields_name, 'values': fields_value})
        sql_connection.commit()


class GetRecordsFromDb:
    def __init__(self, channel_id=None, name=None):
        self.channel_id = channel_id
        self.name = name

    @staticmethod
    def get_channels_id_and_link():
        db.execute(""" SELECT id, link FROM channels; """)
        return [{'id': channel_id, 'link': link}
                for channel_id, link in db.fetchall()]

    @staticmethod
    def get_channel(channel_id):
        db.execute(""" SELECT * FROM channels WHERE id='{channel_id}'; """.format(
            channel_id=channel_id))
        return db.fetchone()

    def check_channel_exists(self):
        db.execute(""" SELECT COUNT(id) FROM channels WHERE name='{name}';""".format(
            name=self.name))
        return db.fetchone()[0]

    @staticmethod
    def get_full_channels_info():
        db.execute(""" SELECT c.name, c.cr_tm, c.link, c.web_site, c.description, f.file_link as icon_link
                      FROM channels c LEFT JOIN files f ON c.icon_id=f.id; """)
        db_elements = []
        for elem in db.fetchall():
            db_elements.append({'name': elem['name'].decode('utf-8'), 'cr_tm': elem['cr_tm'],
                                'link': elem['link'], 'web_site': elem['web_site'], 'description': elem['description'],
                                'icon_link': elem['icon_link']})
        return db_elements


class Channel(SaveRecordsToDb):
    name = dict(length=200)
    link = dict(length=500)
    channel_language = dict(length=2)
    description = dict(length=1000)
    web_site = dict(length=200)

    def __init__(self, channel_id=None, name=None, link=None, icon_id=None, language=None,
                 description=None, web_site=None):
        super(Channel, self).__init__()
        self.channel_id = channel_id
        self.name = name
        self.link = link
        self.icon_id = icon_id
        self.channel_language = language
        self.description = description
        self.web_site = web_site
        self.db_fields = ['name', 'link', 'icon_id', 'channel_language', 'description', 'web_site']

    def check_channel_field_exists(self, key):
        db.execute(""" SELECT COUNT(%(key)s) FROM channels WHERE id='%(channel_id)s' """ %
                   {'key': key, 'channel_id': self.channel_id})

    def update(self):
        channel_from_db = GetRecordsFromDb.get_channel(self.channel_id)
        for key, value in channel_from_db.items():
            if key != 'id':
                cls_field = getattr(self, key, None)
                if value:
                    if value != cls_field and cls_field:
                        self.update_table('channels', self.channel_id, key, cls_field)
                    if not cls_field:
                        setattr(self, key, value)
                else:
                    if cls_field:
                        self.update_table('channels', self.channel_id, key, cls_field)


class TvProgram(SaveRecordsToDb):
    name = dict(length=200)
    genre = dict(length=50)

    def __init__(self, name=None, genre=None, show_date=None, show_time=None, channel_id=None):
        super(TvProgram, self).__init__()
        self.name = name
        self.genre = genre
        self.show_date = show_date
        self.show_time = show_time
        self.channel_id = channel_id
        self.db_fields = ['name', 'genre', 'show_date', 'show_time', 'channel_id']
