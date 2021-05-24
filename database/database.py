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
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
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
                "select_house_ids": """SELECT `id`, `street_address` FROM `houses` ORDER BY 1 ASC""",
                "select_job_ids": """SELECT `id`, `date`, `house_id` FROM `jobs` ORDER BY 1 ASC""",
                "select_worker_ids": """SELECT `id`, `email` FROM `workers` ORDER BY 1 ASC""",
                "select_lawnmower_ids": """SELECT `id`, `model_name`, `make_year` FROM `lawnmowers` ORDER BY 1 ASC""",
                "select_sales_manager_ids": """SELECT `id`, `email` FROM `sales_managers` ORDER BY 1 ASC"""
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

    def _execute_query(self, query, args=None) -> dict:
        """
        Given a templated query and its arguments, executes the query and returns its results
        Convenience method for ease of opening / closing connections
        """
        conn = MySQLdb.connect(self.host, self.user, self.passwd, self.db)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, args)
        conn.commit()
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def get_table_fields(self, sql_table_name) -> List:
        """Given a table name, returns a list of all the fields in that table"""
        return self.schema[sql_table_name]
    
    def select_all(self, sql_table_name) -> dict:
        """Given a table name, runs a SELECT * query and returns the results"""
        query = f"""SELECT * FROM {sql_table_name}"""
        results = self._execute_query(query) 
        return results

    def search_contacts(self, first_name="", last_name="") -> dict:
        """
        Given a first/last name, runs a SELECT * query with WHERE filter against
        the customer contacts table and returns the results
        """
        args = {
            "first_name": f"%{first_name}%",  # add % wildcard characters before and after, for LIKE operator
            "last_name": f"%{last_name}%"
        }
        query = self.sql["select"]["search_contacts"]
        results = self._execute_query(query, args) 
        return results

    def get_jobs_total_price(self, house_id) -> int:
        """
        Calculates and returns a job's "total_price" as an int
        """
        query = self.sql["select"]["get_jobs_total_price"]
        args = {
            "house_id": house_id
        }
        results = self._execute_query(query, args)
        return results[0]["total_price"]  # there will only be one row at index 0
    
    def select_house_ids(self) -> list:
        """Used top populate the dropdown list in the HTML form; returns (id, street_address)[]"""
        query = self.sql["select"]["select_house_ids"]
        results = self._execute_query(query)
        return results
    
    def select_job_ids(self) -> list:
        """Used top populate the dropdown list in the HTML form; returns (id, date, house_id)[]"""
        query = self.sql["select"]["select_job_ids"]
        results = self._execute_query(query)
        return results

    def select_worker_ids(self) -> list:
        """Used top populate the dropdown list in the HTML form; returns (id, email)[]"""
        query = self.sql["select"]["select_worker_ids"]
        results = self._execute_query(query)
        return results

    def select_lawnmower_ids(self) -> list:
        """Used top populate the dropdown list in the HTML form; returns (id, model_name, make_year)[]"""
        query = self.sql["select"]["select_lawnmower_ids"]
        results = self._execute_query(query)
        return results

    def select_sales_manager_ids(self) -> list:
        """Used top populate the dropdown list in the HTML form; returns (id, email)[]"""
        query = self.sql["select"]["select_sales_manager_ids"]
        results = self._execute_query(query)
        return results

    def insert_into(self, sql_table_name: str, data: dict) -> bool:
        """
        Given a table name and a dict of field_name:value pairs, inserts the data into table
        Returns True if executed successfully, otherwise returns False
        """
        query = self.sql["insert"].get(sql_table_name)
        args = data
        if query is None:
            print("That table name is not valid")
            return False
        # if insertion is for a job, calculate and add the "total_price" field
        if sql_table_name == "jobs":
            house_id = args["house_id"]
            args["total_price"] = self.get_jobs_total_price(house_id)
        try:
            self._execute_query(query, args)
            return True
        except Exception as e:
            print(e)
            logger.exception("Error running INSERT operation")
            return False

