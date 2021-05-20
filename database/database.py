from typing import Dict, List
import MySQLdb
import logging

MySQLdb.paramstyle = "named"
logger = logging.getLogger()

class LennysDB:
    """
    Represents the database connection and it schema, with methods to perform CRUD queries
    """
    def __init__(self, host, user, passwd, db) -> None:
        self.conn = MySQLdb.connect(host, user, passwd, db)
        self.schema = {
            "customer_contacts": ["id", "first_name", "last_name", "email", "phone_number", "house_id"],
            "houses": ["id", "street_address", "street_address_2", "city", "state", "zip_code", "yard_size_acres", "sales_manager_id"],
            "jobs": ["id", "date", "total_price", "house_id"],
            "job_workers": ["job_id", "worker_id"],
            "lawnmowers": ["id", "brand", "make_year", "model_name", "is_functional"],
            "sales_managers": ["id", "region", "first_name", "last_name", "email", "phone_number"],
            "workers": ["id", "first_name", "last_name", "email", "phone_number", "lawnmower_id"],
        }
        self.sql = {
            "select": {
                "search_contacts": """SELECT * FROM `customer_contacts` 
                    WHERE `first_name` LIKE %(first_name)s AND `last_name` LIKE %(last_name)s""",
                "get_jobs_total_price": """SELECT 50 * `yard_size_acres` AS total_price FROM `houses` 
                    WHERE `id` = %(house_id)s""",
            },
            "insert": {
                "jobs": """INSERT INTO `jobs` (`date`, `total_price`, `house_id`)
                    VALUES (%(date)s, %(total_price)s, %(house_id)s)""",
                "job_workers": """INSERT INTO `job_workers` (`job_id`, `worker_id`)
                    VALUES (%(job_id)s, %(worker_id)s)""",
                "workers": """INSERT INTO `workers` (`first_name`, `last_name`, `email`, `phone_number`, `lawnmower_id`)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(lawnmower_id)s)""",
                "houses": """INSERT INTO `houses` (`street_address`, `street_address_2`, `city`, `state`, `zip_code`, `yard_size_acres`, `sales_manager_id`)
                    VALUES (%(street_address)s, %(street_address_2)s, %(city)s, %(state)s, %(zip_code)s, %(yard_size_acres)s, %(sales_manager_id)s)""",
                "lawnmowers": """INSERT INTO `lawnmowers` (`brand`, `make_year`, `model_name`, `is_functional`)
                    VALUES (%(brand)s, %(make_year)s, %(model_name)s, %(is_functional)s)""",
                "sales_managers": """INSERT INTO `sales_managers` (`region`, `first_name`, `last_name`, `email`, `phone_number`)
                    VALUES (%(region)s, %(first_name)s, %(last_name)s, %(email)s, %(phone_number)s)""",
                "customer_contacts": """INSERT INTO `customer_contacts` (`first_name`, `last_name`, `email`, `phone_number`, `house_id`)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(house_id)s)""",
            }
        }

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

    def search_contacts(self, first_name="", last_name="") -> dict:
        """
        Given a first/last name, runs a SELECT * query with WHERE filter against
        the customer contacts table and returns the results
        """
        params = {
            "first_name": f"%{first_name}%",  # add % wildcard characters before and after
            "last_name": f"%{last_name}%"
        }
        query = self.sql["select"]["search_contacts"]
        print(query)
        print(params)
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, params)
        self.conn.commit()
        results = cursor.fetchall()
        return results

    def get_jobs_total_price(self, house_id) -> int:
        """
        Calculates and returns a job's "total_price" as an int
        """
        query = self.sql["select"]["get_jobs_total_price"]
        params = {
            "house_id": house_id
        }
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, params)
        self.conn.commit()
        results = cursor.fetchall()
        return results[0]["total_price"]

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

    def insert_into(self, sql_table_name: str, data: dict) -> bool:
        """
        Given a table name and a dict of field_name:value pairs, inserts the data into table
        Returns True if executed successfully, otherwise returns False
        """
        query = self.sql["insert"].get(sql_table_name)
        if query is None:
            print("That table name is not valid")
            return False
        # if insertion is for a job, calculate and add the "total_price" field
        if sql_table_name == "jobs":
            house_id = data["house_id"]
            data["total_price"] = self.get_jobs_total_price(house_id)
        # attempt to run the insert query
        try:
            cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, data)  # this replaces %s with the actual values
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            print('sql_table_name:', sql_table_name)
            print('data:', data)
            print('query:', query)
            logger.exception("Error running INSERT operation")
            return False

