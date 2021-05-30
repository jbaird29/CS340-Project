from typing import Dict, List
import logging

logger = logging.getLogger()

# SELECT id, date, total_price, house_id, GROUP_CONCAT(worker_id) AS worker_ids FROM jobs LEFT JOIN job_workers ON jobs.id = job_workers.job_id GROUP BY jobs.id;

class LennysDB:
    """
    Represents the database connection and it schema, with methods to perform CRUD queries
    """
    def __init__(self, mysql) -> None:
        self.mysql = mysql
        self.schema = {
            "customer_contacts": ["id", "first_name", "last_name", "email", "phone_number", "house_id"],
            "houses": ["id", "street_address", "street_address_2", "city", "state", "zip_code", "yard_size_acres", "sales_manager_id"],
            "jobs": ["id", "date", "total_price", "house_id"],
            "job_workers": ["job_id", "worker_id"],
            "lawnmowers": ["id", "brand", "make_year", "model_name", "is_functional"],
            "sales_managers": ["id", "region", "first_name", "last_name", "email", "phone_number"],
            "workers": ["id", "first_name", "last_name", "email", "phone_number", "lawnmower_id"],
        }
        self.browse_fields = {
            "customer_contacts": ["ID", "First Name", "Last Name", "Email", "Phone Number", "House ID"],
            "houses": ["ID", "Street Address", "Street Address 2", "City", "State", "ZIP", "Yard Size (acres)", "Sales Manager ID", "Sales Manager Email"],
            "jobs": ["ID", "Date", "Total Price", "House ID", "House Address", "Worker IDs"],
            "job_workers": ["Job ID", "Job Date", "Job House ID", "Job House Address", "Worker ID", "Worker Email"],
            "lawnmowers": ["ID", "Brand", "Make Year", "Model Name", "Is Functional?"],
            "sales_managers": ["ID", "Region", "First Name", "Last Name", "Email", "Phone Number"],
            "workers": ["ID", "First Name", "Last Name", "Email", "Phone Number", "Lawnmower ID", "Lawnmower Name", "Lawnmower Year"],
        }
        self.sql = {
            "select": {
                "browse_jobs": """SELECT j.id, j.date, j.total_price, j.house_id, h.street_address, 
                    GROUP_CONCAT(jw.worker_id SEPARATOR ', ') AS worker_ids FROM jobs j 
                    LEFT JOIN job_workers jw ON j.id = jw.job_id LEFT JOIN houses h ON h.id = j.house_id GROUP BY j.id""",
                "browse_job_workers": """SELECT jw.job_id AS job_id, j.date AS job_date, j.house_id AS job_house_id, 
                    h.street_address AS job_house_address, jw.worker_id, w.email AS worker_email 
                    FROM job_workers jw LEFT JOIN jobs j ON jw.job_id = j.id LEFT JOIN workers w ON jw.worker_id = w.id 
                    LEFT JOIN houses h ON h.id = j.house_id""",
                "browse_workers": """SELECT w.id, w.first_name, w.last_name, w.email, w.phone_number, w.lawnmower_id, 
                    l.model_name AS lawnmower_model_name, l.make_year AS lawnmower_make_year FROM workers w 
                    LEFT JOIN lawnmowers l ON l.id = w.lawnmower_id""",
                "browse_houses": """SELECT h.id, h.street_address, h.street_address_2, h.city, h.state, h.zip_code, 
                    h.yard_size_acres, h.sales_manager_id, s.email AS sales_manager_email FROM houses h LEFT JOIN sales_managers s ON h.sales_manager_id = s.id""",
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
            },
            "delete": {
                "sales_manager": """DELETE FROM `sales_managers` WHERE `id` = %(sales_manager_id)s""",
                "job_worker": """DELETE FROM `job_workers` WHERE `job_id` = %(job_id)s AND `worker_id` = %(worker_id)s""",
                "job": """DELETE FROM `jobs` WHERE `id` = %(job_id)s"""
            },
            "update": {
                "lawnmower_status": """UPDATE `lawnmowers` SET `is_functional` = %(is_functional)s 
                    WHERE `id` = %(lawnmower_id)s""",
                "houses_sales_manager": """UPDATE `houses` SET `sales_manager_id` = %(sales_manager_id)s
                    WHERE `id` = %(house_id)s""",
                "job_worker": """UPDATE `job_workers` SET  `job_id` = %(new_job_id)s, `worker_id` = %(new_worker_id)s
                    WHERE `job_id` = %(old_job_id)s AND `worker_id` = %(old_worker_id)s"""
            }
        }

    def _execute_query(self, query, args=None) -> dict:
        """
        Given a templated query and its arguments, executes the query and returns its results
        Convenience method for ease of opening / closing connections
        """
        cursor = self.mysql.connection.cursor()
        cursor.execute(query, args)
        self.mysql.connection.commit()
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_table_fields(self, sql_table_name) -> list:
        """Given a table name, returns a list of all the fields in that table"""
        return self.browse_fields[sql_table_name]
    
    def select_all(self, sql_table_name) -> list:
        """Given a table name, runs a SELECT * query and returns the results"""
        query = f"""SELECT * FROM {sql_table_name}"""
        results = self._execute_query(query) 
        return results

    def select_all_jobs(self) -> list:
        """Selects all fields for the Jobs table"""
        query = self.sql["select"]["browse_jobs"]
        results = self._execute_query(query)
        return results

    def select_all_job_workers(self) -> list:
        """Selects all fields for the Jobs Workers table"""
        query = self.sql["select"]["browse_job_workers"]
        results = self._execute_query(query)
        return results

    def select_all_workers(self) -> list:
        """Selects all fields for the Workers table"""
        query = self.sql["select"]["browse_workers"]
        results = self._execute_query(query)
        return results
    
    def select_all_houses(self) -> list:
        """Selects all fields for the Houses table"""
        query = self.sql["select"]["browse_houses"]
        results = self._execute_query(query)
        return results
        
    def select_all_lawnmowers(self) -> dict:
        """Runs a SELECT * of all lawnmowers; changes 1 and 0 to Yes and No"""
        query = f"""SELECT `id`, `brand`, `make_year`, `model_name`, 
        CASE WHEN `is_functional` = 1 THEN "Yes" ELSE "No" END AS is_functional FROM `lawnmowers` """
        results = self._execute_query(query) 
        return results

    def search_contacts(self, first_name="", last_name="") -> list:
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

    def insert_into(self, sql_table_name: str, data: dict):
        """
        Given a table name and a dict of field_name:value pairs, inserts the data into table
        Returns tuple of: (True or False depending on result, status message)
        """
        query = self.sql["insert"].get(sql_table_name)
        args = data
        print(args)
        if query is None:
            print("That table name is not valid")
            return False
        # if insertion is for a job, calculate and add the "total_price" field
        if sql_table_name == "jobs":
            house_id = args["house_id"]
            args["total_price"] = self.get_jobs_total_price(house_id)
        # if insertion is for a house, coalesce the empty string to null valid if necessary
        if sql_table_name == "houses":
            args["sales_manager_id"] = None if args["sales_manager_id"] == "" else args["sales_manager_id"]
            args["street_address_2"] = None if args["street_address_2"] == "" else args["street_address_2"]
        try:
            self._execute_query(query, args)
            return True, "Successfully inserted that entry."
        except Exception as e:
            logger.exception("Error running INSERT operation")
            print(e)
            return False, str(e)
    
    def delete_sales_manager(self, sales_manager_id: int):
        """Given a sales_manager_id, deletes that record"""
        query = self.sql["delete"]["sales_manager"]
        args = {
            "sales_manager_id": sales_manager_id
        }
        try:
            self._execute_query(query, args)
            return True, "Successfully deleted that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running DELETE sales manager")
            return False, str(e)

    def update_lawnmower_status(self, lawnmower_id: int, is_functional: int):
        """Updates whether a lawnmower is functional or not"""
        query = self.sql["update"]["lawnmower_status"]
        args = {
            "lawnmower_id": lawnmower_id,
            "is_functional": is_functional
        }
        try:
            self._execute_query(query, args)
            return True, "Successfully updated that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running UPDATE lawnmower status")
            return False, str(e)

    def update_houses_sales_manager(self, house_id: int, sales_manager_id: int):
        """Updates a house's sales manager"""
        query = self.sql["update"]["houses_sales_manager"]
        sales_manager_id = None if sales_manager_id == "" else sales_manager_id
        args = {
            "house_id": house_id,
            "sales_manager_id": sales_manager_id
        }
        try:
            self._execute_query(query, args)
            return True, "Successfully updated that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running UPDATE house's sales manager")
            return False, str(e)

    def update_job_worker(self, old_job_id, old_worker_id, new_worker_id, new_job_id):
        """Updates a job worker table entry"""
        query = self.sql["update"]["job_worker"]
        args = {
            "old_job_id": old_job_id,
            "old_worker_id": old_worker_id,
            "new_worker_id": new_worker_id,
            "new_job_id": new_job_id
        }
        try:
            self._execute_query(query, args)
            return True, "Successfully updated that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running UPDATE job worker")
            return False, str(e)

    def delete_job_worker(self, job_id, worker_id):
        """Delete a job worker table entry"""
        query = self.sql["delete"]["job_worker"]
        args = {
            "job_id": job_id,
            "worker_id": worker_id,
        }
        try:
            self._execute_query(query, args)
            return True, "Successfully deleted that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running DELETE job worker")
            return False, str(e)

    def delete_job(self, job_id):
        """Delete a job worker table entry"""
        query = self.sql["delete"]["job"]
        args = {
            "job_id": job_id,
        }
        try:
            self._execute_query(query, args)
            return True, "Successfully deleted that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running DELETE job worker")
            return False, str(e)


