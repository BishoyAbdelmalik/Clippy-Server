import sqlite3
import logging
from datetime import datetime

class SQLiteHandler(logging.Handler):
    def __init__(self,
                 file_name : str = "logs.db",
                 table_name : str = "logs") -> None:
       logging.Handler.__init__(self)
       self.connection = sqlite3.connect(file_name)
       self.file_name = file_name
       self.table_name = table_name

       cursor = self.connection.cursor()
       cursor.execute("""
       CREATE TABLE IF NOT EXISTS ? (
           date text,
           time text,
           desc text
       )
       """, (self.table_name, ))
       self.connection.commit()

    def emit(self, record) -> None:
        cursor = self.connection.cursor()

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H-%M-%S")

        cursor.execute("""
        INSERT INTO ? VALUES (?, ?, ?)
        """, (self.table_name,
              date,
              time,
              record))

        self.connection.commit()
