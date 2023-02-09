import sqlite3


class DB:

    def __init__(self, rows_check=False):
        self.rows_check = rows_check
        print(rows_check)

    def __enter__(self):
        self.conn = sqlite3.connect('vacancy.db')
        if self.rows_check:
            self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        return self

    def query(self, qry):
        self.c.execute(qry)
        result = self.c.fetchall()
        return result

    def update(self, qry):
        self.c.execute(qry)
        self.conn.commit()

    def insert(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ':' + ', :'.join(data.keys())
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name, columns, placeholders)
        self.c.execute(query, data)
        self.conn.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.c.close()
        self.conn.close()


def select_info(query):
    conn = sqlite3.connect('vacancy.db')
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result


def insert_info(table_name, data):
    columns = ', '.join(data.keys())
    placeholders = ':' + ', :'.join(data.keys())
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name, columns, placeholders)
    conn = sqlite3.connect('vacancy.db')
    c = conn.cursor()
    c.execute(query, data)
    conn.commit()
    conn.close()
