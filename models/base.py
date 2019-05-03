from db.db import Connect
class Base:
    def __init__():
        pass
    columns = []
    def conn(self):
        conn = Connect.conn()
    
    def table_name(self, name):
        table_name = name
    
    def column(self, name):
        columns.append(name)
    
    def all(self):
        query = "SELECT * FROM {table_name}"
        conn.execute(query)
        return conn.fetchall()

class Role(Base):
    def __init__(self):
        Base.__init__(self)
    table_name('test_role')
    column('id')
    column('role_name')