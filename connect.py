import config
import psycopg2
import psycopg2.extras as extras


class Connector:

    def __init__(self,
                 host=config.PGHOST,
                 port='5432',
                 dbname=config.PGDATABASE,
                 user=config.PGUSER,
                 password=config.PGPASSWORD):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password

    def _conn_string(self):

        conn_string = f"host={self.host} " \
                      f"port={self.port} " \
                      f"dbname={self.dbname} " \
                      f"user={self.user} " \
                      f"password={self.password}"

        return conn_string

    def _connect(self):

        conn_string = self._conn_string()
        conn = psycopg2.connect(conn_string)
        print('Connected!')

        return conn

    def connect(self):

        conn = self._connect()
        cursor = conn.cursor()

        return conn, cursor


if __name__ == "__main__":

    connector = Connector()
    conn, cursor = connector.connect()
    cursor.execute("SELECT MAX(play_id) FROM playbyplay")
    max_play_id = cursor.fetchall()[0][0]
    conn.commit()
    conn.close()
    print(max_play_id)