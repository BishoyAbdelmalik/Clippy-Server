import sqlite3
import logging

class SQLiteHandler(logging.Handler):
    def __init__(self,
                 file_name : str = "logs.db",
                 table_name : str = "logs") -> None:
       logging.Handler.__init__(self)
       

    def emit(self, record) -> None:
        pass
        
