# -*- coding: ascii -*-
from db_init import db, sql_connection


class SaveRecordsToDb(object):
    def __init__(self):
        pass

    def save_channels_to_db(self, dict_of_elements):
        elements_count = 0
        self.insert_icons_into_files([link['icon'] for link in dict_of_elements.values()])
        for element in dict_of_elements.keys():
            db.execute(""" SELECT COUNT(id) FROM channels WHERE link='{link}' OR name='{name}' """.format(
                link=element, name=dict_of_elements[element]['name'].encode('utf-8')))
            if db.fetchone()[0] == 0:
                db.execute(""" INSERT INTO channels(name, link, icon_id)
                              VALUES ('{name}', '{link}', (SELECT id FROM files WHERE file_link='{file_link}')); """.
                           format(name=dict_of_elements[element]['name'].encode('utf-8'), link=element,
                                  file_link=dict_of_elements[element]['icon']))
                elements_count += 1
        sql_connection.commit()
        return elements_count

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
        items = {key: value for key, value in self.__dict__.items() if (key in getattr(self, 'db_fields')) and value}
        fields_name = ",".join(items.keys())
        fields_value = "','".join(items.values())
        db.execute(""" INSERT INTO %(table_name)s(%(keys)s) VALUES ('%(values)s');""" % {'table_name': table_name,
                                                                                         'keys': fields_name,
                                                                                         'values': fields_value})
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
        db.execute(""" SELECT * FROM channels WHERE id='{channel_id}'; """.format(channel_id=channel_id))
        return db.fetchone()

    def check_channel_exists(self):
        db.execute(""" SELECT COUNT(id) FROM channels WHERE name='{name}';""".format(name=self.name))
        return db.fetchone()[0]


class Channel(SaveRecordsToDb):
    def __init__(self, channel_id=None, name=None, link=None, icon_id=None, language=None, description=None):
        super(Channel, self).__init__()
        self.channel_id = channel_id
        self.name = name
        self.link = link
        self.icon_id = icon_id
        self.channel_language = language
        self.description = description
        self.db_fields = ['name', 'link', 'icon_id', 'channel_language', 'description']

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
    pass
