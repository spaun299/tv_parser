# -*- coding: ascii -*-
from db_init import db, sql_connection


class SaveRecordsToDb:
    def __init__(self):
        pass

    def save_to_db(self, dict_of_elements):
        self.insert_icons_into_files([link['icon'] for link in dict_of_elements.values()])
        self.insert_channels(dict_of_elements)

    @staticmethod
    def insert_icons_into_files(list_of_links):
        db.execute(""" SELECT file_link FROM files WHERE file_link IN {list_of_links}; """.format(
            list_of_links=tuple(list_of_links)))
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
    def get_channel_id_and_link():
        db.execute(""" SELECT id, link FROM channels; """)
        return [{'id': channel_id, 'link': link} for channel_id, link in db.fetchall()]
