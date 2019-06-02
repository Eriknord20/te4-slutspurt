import psycopg2
from db.db import Connect


class Base:
    """
    Base class for every model

    :return: Base class for every model
    :rtype: object
    """

    def __init__(self, connection):
        """
        Initailising the base for every model

        :param connection: It is an object of type psycopg2
        :type connection: type: object
        """
        self.connection = connection
        self.conn = self.connection.conn()
        self.cursor = self.connection.cursor()
        self.table = ""
        self.columns = []

    def table_name(self, name):
        """
        Takes the tableName and assings it to a varible

        :param name: nName of the table
        :type name: type: string
        """
        self.table = name

    def column(self, name):
        """
        Takes the columnName and adds it to a list

        :param name: The name of the column
        :type name: type: string
        """
        self.columns.append(name)

    def update(self, key, params, prev_id):
        """
        Updates a row in the specified table

        :param params: The array contains key and a value
        :type params: Array
        """
        try:
            if len(params) >= 2:
                query = """UPDATE %s SET %s = %s, %s = '%s' WHERE id = %s""" % (
                    self.table, key[0], params[0], key[1], params[1], prev_id)
            else:
                query = """UPDATE %s SET %s = %s WHERE id = %s""" % (
                    self.table, key, params[0], prev_id)
            print(query)
            self.cursor.execute(query)
            self.conn.commit()
        except ValueError:
            print("***")
            print("Something went wrong")
            print("***")

    def insert(self, values: []):
        """
        Inserts into the sepcified table

        :param keys: Key name
        :type keys: list, optional,
        :param values: Value
        :type values: list, optional
        """
        try:
            if values[0]:
                query = """INSERT INTO %s (%s, %s) VALUES(%s, '%s');""" % (
                    self.table, self.columns[0], self.columns[1], values[0], values[1])
            else:
                query = "INSERT INTO %s (%s) VALUES('%s');" % (
                    self.table, self.columns[1], values[1])
            print("***3")
            print(query)
            print("***3")
            self.cursor.execute(query)
            self.conn.commit()
        except psycopg2.DatabaseError as error:
            print("Something went wrong while inserting into table: %s" %
                  self.table)
            print(error)
        finally:
            print("Every thing workout fine")

    def delete(self, _id: int):
        """
        Example:
        user = User(): instance of the user table
        user.delete(_id)

        :param _id: Delete where id = _id
        :type _id: int
        """
        query = """DELETE FROM %s WHERE %s = %s""" % (
            self.table, self.columns[0], _id)
        self.cursor.execute(query)
        self.conn.commit()

    def find_by_id(self, _id: int):
        """
        Get row with the specified id

        :param _id: Id for a specific row
        :type _id: type: integer
        :return: Array of rows from the database
        :rtype: Array
        """
        try:
            query = """SELECT * FROM %s WHERE id = %s""" % (self.table, _id)
            print(query)
            self.cursor.execute(query)
            self.conn.commit()
            return self.cursor.fetchone()
        except ValueError:
            print("Something went wrong while getting data from table: %s" %
                  self.table)
        finally:
            print("Every thing workout fine")

    def find_by_name(self, key, value):
        try:
            query = """SELECT * FROM %s WHERE %s = '%s'""" % (
                self.table, key, value)
            print(query)
            self.cursor.execute(query)
            self.conn.commit()
            return self.cursor.fetchall()
        except ValueError:
            print("Something went wrong while getting data from table: %s" %
                  self.table)
        finally:
            print("Every thing workout fine")

    def all_rel(self):
        """
        Get everything across multible connected tables

        :return: Array of rows
        :rtype: Array
        """

        query = """select u.id, u.user_name, r.role_name from %s u
                    left join user_role on u.id = user_role.user_id
                    left join test_role r on user_role.role_id = r.id;
                """ % (self.table)
        print(self.table)
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()

    def all(self):
        """
        Get the everything from the specified table

        :return: Array of rows
        :rtype: type: Array
        """
        query = """SELECT * FROM  %s""" % self.table
        print(self.table)
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()


class Role(Base):
    """
    Role class contains the database tabel name and all of its columns

    :param Base: Inherites the base class
    :type Base: type: class
    """

    def __init__(self):
        Base.__init__(self, Connect())
        super().table_name('test_role')
        super().column('id')
        super().column('role_name')

    def get_role_by_user_id(self, _id):
        user_role = UserRole()
        role_rel = user_role.find_by_name('user_id', _id)
        if role_rel == []:
            return None
        return self.find_by_id(role_rel[0][2])


class User(Base):
    """
    Role class contains the database tabel name and all of its columns

    :param Base: Inherites the base class
    :type Base: type: class
    """

    def __init__(self):
        Base.__init__(self, Connect())
        super().table_name('test_user')
        super().column('id')
        super().column('user_name')


class UserRole(Base):
    def __init__(self):
        Base.__init__(self, Connect())
        super().table_name('user_role')
        super().column('user_id')
        super().column('role_id')
