# -*- coding: ascii -*-
from db_init import db, sql_connection


class SaveRecordsToDb(object):
    def __init__(self):
        pass

    def save_to_db(self, dict_of_elements):
        self.insert_icons_into_files([link['icon'] for link in dict_of_elements.values()])
        self.insert_channels(dict_of_elements)

    @staticmethod
    def insert_icons_into_files(list_of_links):
        print(list_of_links)
        db.execute(""" SELECT file_link FROM files WHERE file_link IN %(list_of_links)s); """ %
                   {'list_of_links': tuple(list_of_links)})
        links = [link['file_link'] for link in db.fetchall()]
        db.executemany(""" INSERT INTO files(file_link) VALUES(%(link)s); """,
                       [{'link': elem} for elem in list_of_links if elem not in links])
        sql_connection.commit()

    @staticmethod
    def insert_channels(dict_of_elements):
        for element in dict_of_elements.keys():
            print(dict_of_elements[element]['name'])
            db.execute(""" SELECT COUNT(id) FROM channels WHERE link='{link}' OR name='{name}' """.format(
                link=element, name=dict_of_elements[element]['name'].encode('utf-8')))
            if db.fetchone()[0] == 0:
                db.execute(""" INSERT INTO channels(name, link, icon_id)
                              VALUES ('{name}', '{link}', (SELECT id FROM files WHERE file_link='{file_link}')); """.
                           format(name=dict_of_elements[element]['name'].encode('utf-8'), link=element,
                                  file_link=dict_of_elements[element]['icon']))
        sql_connection.commit()

    @staticmethod
    def update_channel(channel_id, key, value):
        db.execute(""" UPDATE channels SET %(key)s='%(value)s' WHERE id='%(channel_id)s';""" %
                   {'key': key, 'value': value, 'channel_id': channel_id})

    def save_channel(self):
        keys, values = [(','.join(keys), ','.join(values)) for keys, values in self.__dict__]
        print(keys)
        print(values)


class GetRecordsFromDb:
    def __init__(self, channel_id=None, name=None):
        self.channel_id = channel_id
        self.name = name

    @staticmethod
    def get_channels_id_link_and_bool_description():
        db.execute(""" SELECT id, link, COUNT(description) FROM channels; """)
        return [{'id': channel_id, 'link': link, 'description': bool(description)}
                for channel_id, link, description in db.fetchall()]

    def get_channel(self):
        db.execute(""" SELECT * FROM channels WHERE id='{channel_id}'; """.format(channel_id=self.channel_id))
        return db.fetchone()


class Channel(SaveRecordsToDb):
    def __init__(self, channel_id=None, name=None, link=None, icon_id=None, language=None, description=None):
        super(Channel, self).__init__()
        self.channel_id = channel_id
        self.name = name
        self.link = link
        self.icon_id = icon_id
        self.language = language
        self.description = description

    def check_channel_exists(self):
        db.execute(""" SELECT COUNT(id) FROM channels WHERE name='{name}';""".format(name=self.name))
        return db.fetchone()[0]

    def check_channel_field_exists(self, key):
        db.execute(""" SELECT COUNT(%(key)s) FROM channels WHERE id='%(channel_id)s' """ %
                   {'key': key, 'channel_id': self.channel_id})

    def update_fields_if_empty(self):
        print(self.__dict__)
