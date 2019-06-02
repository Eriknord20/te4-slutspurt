import psycopg2

DBCONFIG = {"user": "dev", "password": "123qwe", "host": "localhost", "dbname": "test"}


class Connect():
    """[summary: Connect to database.
    Intitailizing connection: conn = Connect()
    Creating cursor that can execute queries: cur = conn.cursor()
    Executing query: cur.execute(query)
    ]

    :return: [description: Returns connection object]
    :rtype: [type: Connection object]
    """

    def __init__(self):
        """[summary: Initailize a connection to a database and assingning it to self.conn]"""
        try:
            self.connection = psycopg2.connect(**DBCONFIG)
        except (psycopg2.DatabaseError) as error:
            print("Error while creating PostgreSQL table", error)

    def cursor(self):
        """[summary: Create a cursor out of the connection that can execute sql queries]"""
        return self.connection.cursor()

    def conn(self):
        return self.connection

    def kill(self):
        """[summary: Kill the connection to the database]"""
        self.connection.close()
