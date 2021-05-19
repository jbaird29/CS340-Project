from typing import Dict, List
import MySQLdb
import logging

logger = logging.getLogger()

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
    
    def select_all(self, sql_table_name) -> dict:
        """Given a table name, runs a SELECT * query and returns the results"""
        query = f"""SELECT * FROM {sql_table_name}"""
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, args=None)
        self.conn.commit()
        results = cursor.fetchall()
        return results

    def search_contacts(self, first_name, last_name) -> dict:
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
        return results

    def select_ids(self, sql_table_name) -> list:
        """
        Runs a SELECT id from {sql_table_name} query and returns the results as a List
        Used top populate the dropdown list in the HTML form
        """
        query = f"""SELECT `id` FROM {sql_table_name} ORDER BY 1 ASC"""
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, args=None)
        self.conn.commit()
        results = cursor.fetchall()
        ids = [result["id"] for result in results]
        return ids

    def insert_into(self, sql_table_name: str, data: dict) -> None:
        """
        Given a table name and a dict of field_name:value pairs, inserts the data into table
        """
        # helper lists
        fields = [key for key in data.keys()]
        values = [data[key] for key in data.keys()]
        placeholders = ["%s"] * len(fields)  # these are the '%s' placeholders in query
        # helper strings - for insertion into query
        fields_str = ', '.join(fields)
        placeholder_str = ', '.join(placeholders)
        # create the SQL with %s placeholders
        query = f"""INSERT INTO {sql_table_name} ({fields_str})
        VALUES ({placeholder_str})"""
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query, values)  # this replaces %s with the actual values
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            print('sql_table_name:', sql_table_name)
            print('data:', data)
            print('query:', query)
            logger.exception("Error running INSERT operation")
            return False

