import sqlite3
from typing import List


class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.schema = """CREATE TABLE IF NOT EXISTS entries
        (ranking INTEGER, album TEXT, artist TEXT, album_units INTEGER, album_sales INTEGER, song_sales INTEGER, song_streams INTEGER, peak_position INTEGER, weeks_in_chart INTEGER, label TEXT, date TEXT)"""

    def set_up_db(self):
        c = self.conn.cursor()
        c.execute(self.schema)
        self.conn.commit()

    def insert_entry(self, table: str, values: List, fields: List[str]):
        c = self.conn.cursor()
        fields_str = ", ".join(fields)
        placeholders = ", ".join(["?" for _ in fields])
        c.execute(
            f"""INSERT INTO {table}
        ({fields_str})
        VALUES ({placeholders})""",
            values,
        )
        self.conn.commit()


db_manager = DBManager("rollingstones_charts.db")
