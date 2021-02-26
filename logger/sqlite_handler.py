from logging import LogRecord, Handler
import sqlite3
from datetime import datetime

class SQLiteHandler(Handler):
    """
    Class that holds the logging handler that feeds to SQLite.
    """
    def __init__(self,
                 file_name : str = "logs.db",
                 table_name : str = "logs") -> None:
        """
        The Constrctor of the SQLite handler. Instantiating this
        class, and passing it to the logger would ensure that the
        logger would add logs to the local database, in addition to
        the default handler, which is standard output.
        """
        Handler.__init__(self)
        self.connection = sqlite3.connect(file_name)
        self.file_name = file_name
        self.table_name = table_name

        cursor = self.connection.cursor()
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            date text,
            time text,
            desc text
        )
        """)
        self.connection.commit()

    def emit(self, rec : LogRecord) -> None:
        """
        This is used whenever the handler logs. This method should add
        the logs with the corresponding date and time.
        """
        cursor = self.connection.cursor()

        record = rec.getMessage()
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        query = f"""
        INSERT INTO {self.table_name}
        VALUES ("{date}", "{time}", "{record}")
        """

        cursor.execute(query)

        self.connection.commit()
