import sqlite3
import os


class DBController:
    def __init__(self, name="resources/ModernTanksDB"):
        self.name = name
        self.check_db()

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

    # Проверка на существование БД и её создание если нету
    def check_db(self):
        if not os.path.exists(self.name):
            print(1)
            query_table_posts1 = '''

CREATE TABLE d_table (
    low  TEXT DEFAULT (False),
    mid  TEXT DEFAULT (True),
    high TEXT DEFAULT (False) 
            );'''
            self.query(query_table_posts1)

            query_table_posts2 = '''
        CREATE TABLE graph_table (
    low  TEXT DEFAULT (False),
    mid  TEXT DEFAULT (True),
    high TEXT DEFAULT (False) 
            );'''
            self.query(query_table_posts2)

            query_table_posts3 = '''
        CREATE TABLE FPS_table (
    low  TEXT DEFAULT (False),
    mid  TEXT DEFAULT (True),
    high TEXT DEFAULT (False) 
            );'''
            self.query(query_table_posts3)

            query_table_posts4 = '''
CREATE TABLE volume_table (
    volume_music   INTEGER DEFAULT (50),
    volume_sound   INTEGER DEFAULT (50),
    volume_general INTEGER DEFAULT (50) 
);'''
            self.query(query_table_posts4)

            self.clear()


    # Функция для изменения таблицы доходов
    def update_graph(self, values):
        query = f"""
                    DELETE FROM graph_table
            """
        query2 = f'''INSERT INTO graph_table (low, mid, high) VALUES {values};'''
        self.query(query)
        return self.query(query2)

    def update_d(self, values):
        query = f"""
                    DELETE FROM d_table
            """
        query2 = f'''INSERT INTO d_table (low, mid, high) VALUES {values};'''
        self.query(query)
        return self.query(query2)

    def update_fps(self, values):
        query = f"""
                    DELETE FROM FPS_table
            """
        query2 = f'''INSERT INTO FPS_table (low, mid, high) VALUES {values};'''
        self.query(query)
        return self.query(query2)
    def update_volume(self, titles, values, where_title, where_value):
        query = f"""
                    UPDATE volume_table
            SET {titles} = {values}
            WHERE {where_title} = {where_value}
            """
        return self.query(query)

    # Функция для очистки БД
    def clear(self):
        query = f"""
        DELETE FROM d_table
        """
        query_1 = f"""
        DELETE FROM graph_table
        """
        query_2 = f"""
        DELETE FROM FPS_table
        """

        query2 = '''INSERT INTO d_table (low, mid, high) VALUES (False, True, False);'''
        query3 = '''INSERT INTO graph_table (low, mid, high) VALUES (False, True, False);'''
        query4 = '''INSERT INTO FPS_table (low, mid, high) VALUES (False, True, False);'''
        self.query(query)
        self.query(query_2)
        self.query(query_1)
        self.query(query2)
        self.query(query3)
        self.query(query4)

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




