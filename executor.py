import psycopg2
import psycopg2.extras as extras


class Executor:

    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def execute_values(self, dataframe, table):
        conn, cursor = self.conn, self.cursor

        query, tuples = self._prepare_values(dataframe, table)

        try:
            extras.execute_values(cursor, query, tuples)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            cursor.close()
            return 1

        print("The dataframe is inserted")

    def _prepare_values(self, dataframe, table):
        tuples = [tuple(x) for x in dataframe.to_numpy()]
        cols = ','.join(dataframe.columns)
        query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
        return query, tuples
