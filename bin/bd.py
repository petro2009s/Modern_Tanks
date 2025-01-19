import sqlite3
import os
import screeninfo


class DBController:
    def __init__(self, name="resources/ModernTanksDB"):
        self.name = name
        self.check_db()

    def check_db(self):
        if not os.path.exists(self.name):
            query_table_posts1 = '''
CREATE TABLE minimap_table (
    [on] INTEGER DEFAULT (True),
    off  INTEGER DEFAULT (False) 
);'''
            self.query(query_table_posts1)

            query_table_posts2 = '''
        CREATE TABLE graph_table (
    low  INTEGER DEFAULT (False),
    mid  INTEGER DEFAULT (True),
    high INTEGER DEFAULT (False) 
            );'''
            self.query(query_table_posts2)

            query_table_posts3 = '''
        CREATE TABLE FPS_table (
    low  INTEGER DEFAULT (False),
    mid  INTEGER DEFAULT (True),
    high INTEGER DEFAULT (False) 
            );'''
            self.query(query_table_posts3)

            query_table_posts4 = '''
CREATE TABLE volume_table (
    volume_music   INTEGER DEFAULT (50),
    volume_sound   INTEGER DEFAULT (50),
    volume_general INTEGER DEFAULT (50) 
);'''
            self.query(query_table_posts4)

            query_table_posts5 = '''
CREATE TABLE full_table (
    [on] INTEGER DEFAULT (True),
    off  INTEGER DEFAULT (False)
);'''
            self.query(query_table_posts5)

            query_table_posts6 = f'''
CREATE TABLE size_table (
    width  INTEGER DEFAULT ({screeninfo.get_monitors()[0].width}),
    height INTEGER DEFAULT ({screeninfo.get_monitors()[0].height})
);'''
            self.query(query_table_posts6)

            query_table_posts7 = f'''
CREATE TABLE monitor_table (
    id  INTEGER DEFAULT (0)
);'''
            self.query(query_table_posts7)

            self.clear()

    # Функция исполнения запросов
    def query(self, query):
        result = None
        try:
            connection = sqlite3.connect(self.name)
            cur = connection.cursor()
            result = cur.execute(query).fetchall()
            connection.commit()
            connection.close()
        except Exception as e:
            print(e)
        return result


    def update_to_db(self, table, title, value, where_title="", where_value=""):
        query = f"""
                UPDATE {table}
                SET {title} = {value}
                """
        if where_title != "":
            query += f"\nWHERE {where_title} = {where_value}"
        return self.query(query)

    def insert_to_db(self, table, value, title=""):
        query = f"""
                INSERT INTO {table}{title} VALUES {value}
                """
        return self.query(query)

    # Функция для очистки БД
    def clear(self):
        query = f"""
        DELETE FROM minimap_table
        """
        query_1 = f"""
        DELETE FROM graph_table
        """
        query_2 = f"""
        DELETE FROM FPS_table
        """
        query_3 = f"""
        DELETE FROM full_table
        """
        query_4 = f"""
        DELETE FROM size_table
        """
        query_5 = f"""
        DELETE FROM monito_table
        """

        query2 = '''INSERT INTO minimap_table ([on], off) VALUES (True, False);'''
        query3 = '''INSERT INTO graph_table (low, mid, high) VALUES (False, True, False);'''
        query4 = '''INSERT INTO FPS_table (low, mid, high) VALUES (False, True, False);'''
        query5 = '''INSERT INTO full_table ([on], off) VALUES (True, False);'''
        query6 = f'''INSERT INTO size_table (width, height) VALUES ({screeninfo.get_monitors()[0].width}, {screeninfo.get_monitors()[0].height});'''
        query7 = '''INSERT INTO monitor_table (id) VALUES (0);'''

        self.query(query)
        self.query(query_2)
        self.query(query_1)
        self.query(query_5)
        self.query(query7)
        self.query(query2)
        self.query(query3)
        self.query(query4)
        self.query(query_3)
        self.query(query5)
        self.query(query_4)
        self.query(query6)

        query = f"""
        DELETE FROM volume_table
        """
        query2 = '''INSERT INTO volume_table (volume_music, volume_sound, volume_general) VALUES (50, 50, 50);'''
        self.query(query)
        self.query(query2)


    # Функция для отбора из БД
    def select(self, table, titles="*", where=None):
        query = f"""
        SELECT {titles} FROM {table}
        """
        if where:
            query += f"\nWHERE {where}"
        return self.query(query)




