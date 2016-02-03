from db_init import db, sql_connection


class SaveRecordsToDb:
    def __init__(self):
        pass

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
            db.execute(""" INSERT INTO channels(name, link, icon_id)
                          VALUES ('{name}', '{link}', (SELECT id FROM files WHERE file_link='{file_link}')); """.format(
                name='test', link=element, file_link=dict_of_elements[element]['icon']))
        sql_connection.commit()

    def save_to_db(self, dict_of_elements):
        self.insert_icons_into_files([link['icon'] for link in dict_of_elements.values()])
        self.insert_channels(dict_of_elements)
