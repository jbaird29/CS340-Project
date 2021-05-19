import MySQLdb

class Database:
    """
    Represents the database connection and it schema, with methods to perform CRUD queries
    """
    def __init__(self, host, user, passwd, db, schema) -> None:
        self.conn = MySQLdb.connect(host,user,passwd,db)
        self.schema = schema
    
    def select_all(self, sql_table_name):
        query = f"""SELECT * FROM {sql_table_name}"""
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, args=None)
        self.conn.commit()
        results = cursor.fetchall()
        return results

    def search_contacts(self, first_name, last_name):
        query = f"""SELECT * FROM `customer_contacts` 
        WHERE `first_name` LIKE '%{first_name}%' AND `last_name` LIKE '%{last_name}%'"""
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, args=None)
        self.conn.commit()
        results = cursor.fetchall()
        print(results)
        return results