import psycopg2

dbConfig = {
    'host':'localhost',
    'db':'test',
    'user':'dev',
    'pw':'123qwe',
}
class Connect():
    def conn():
        conn = psycopg2.connect("dbname=test user=dev password=123qwe host=localhost")
        return conn.cursor()
        
