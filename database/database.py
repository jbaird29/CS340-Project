from typing import Dict, List
import MySQLdb

class Database:
    """
    Represents the database connection and it schema, with methods to perform CRUD queries
    """
    def __init__(self, host, user, passwd, db, schema) -> None:
        self.conn = MySQLdb.connect(host,user,passwd,db)
        self.schema = schema

    def get_table_fields(self, sql_table_name) -> List:
        """Given a table name, returns a list of all the fields in that table"""
        return self.schema[sql_table_name]
    
    def select_all(self, sql_table_name) -> Dict:
        """Given a table name, runs a SELECT * query and returns the results"""
        query = f"""SELECT * FROM {sql_table_name}"""
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, args=None)
        self.conn.commit()
        results = cursor.fetchall()
        return results

    def search_contacts(self, first_name, last_name) -> Dict:
        """
        Given a first/last name, runs a SELECT * query with WHERE filter against
        the customer contacts table and returns the results
        """
        query = f"""SELECT * FROM `customer_contacts` 
        WHERE `first_name` LIKE '%{first_name}%' AND `last_name` LIKE '%{last_name}%'"""
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, args=None)
        self.conn.commit()
        results = cursor.fetchall()
        print(results)
        return results

    def select_house_ids(self) -> List:
        """
        Runs a SELECT id from houses query and returns the results as a List
        Used top populate the dropdown list in the HTML form
        """
        query = f"""SELECT `id` FROM `houses` ORDER BY 1 ASC"""
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, args=None)
        self.conn.commit()
        results = cursor.fetchall()
        house_ids = [result["id"] for result in results]
        return house_ids

    def select_sales_manager_ids(self) -> List:
        """
        Runs a SELECT id from sales_managers query and returns the results as a List
        Used top populate the dropdown list in the HTML form
        """
        query = f"""SELECT `id` FROM `sales_managers` ORDER BY 1 ASC"""
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, args=None)
        self.conn.commit()
        results = cursor.fetchall()
        sales_manager_ids = [result["id"] for result in results]
        return sales_manager_ids
