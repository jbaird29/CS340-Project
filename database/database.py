from typing import Dict, List
import logging

logger = logging.getLogger()

class BaseTable:
    """Base Table class from which all other tables inherit"""
    def __init__(self, mysql, title, fields, field_titles, sql_browse, sql_insert) -> None:
        self._mysql = mysql
        self._title = title
        self._fields = fields
        self._field_titles = field_titles
        self._sql_browse = sql_browse
        self._sql_insert = sql_insert

    def _execute_query(self, query, args=None) -> dict:
        """Given a templated query and its arguments, executes the query and returns its results
        Convenience method for ease of opening / closing connections"""
        cursor = self._mysql.connection.cursor()
        cursor.execute(query, args)
        self._mysql.connection.commit()
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_field_titles(self) -> list:
        """Returns a list of all the field titles in the table"""
        return self._field_titles

    def get_title(self) -> str:
        """Returns the title of the table"""
        return self._title


    def select_all(self) -> list:
        """Selects all fields for the browse section of the UI"""
        query = self._sql_browse
        return self._execute_query(query)
    
    def insert_into(self, data: dict):
        """Given a table name and a dict of field_name:value pairs, inserts the data into table
        Returns tuple of: (True or False depending on result, status message)"""
        query = self._sql_insert
        args = data
        print(args)
        try:
            self._execute_query(query, args)
            return True, "Successfully inserted that entry."
        except Exception as e:
            logger.exception("Error running INSERT operation")
            print(e)
            return False, str(e)


class CustomerContacts(BaseTable):
    def __init__(self, mysql) -> None:
        title = "Customer Contacts"
        fields = ["id", "first_name", "last_name", "email", "phone_number", "house_id"]
        field_titles = ["ID", "First Name", "Last Name", "Email", "Phone Number", "House ID", "House Address"]
        sql_browse =  """SELECT c.id, c.first_name, c.last_name, c.email, c.phone_number, c.house_id, h.street_address 
                FROM customer_contacts c LEFT JOIN houses h ON c.house_id = h.id"""
        sql_insert = """INSERT INTO `customer_contacts` (`first_name`, `last_name`, `email`, `phone_number`, `house_id`)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(house_id)s)"""
        super().__init__(mysql, title, fields, field_titles, sql_browse, sql_insert)
        self.sql_search = sql_browse + """ WHERE c.first_name LIKE %(first_name)s AND c.last_name LIKE %(last_name)s"""

    def search(self, first_name="", last_name="") -> list:
        """Given a first/last name, runs a SELECT query with WHERE filter against the customer contacts table and returns the results
        """
        args = {
            "first_name": f"%{first_name}%",  # add % wildcard characters before and after, for LIKE operator
            "last_name": f"%{last_name}%"
        }
        query = self.sql_search
        print(query)
        return super()._execute_query(query, args) 


class Houses(BaseTable):
    def __init__(self, mysql) -> None:
        title = "Houses"
        fields = ["id", "street_address", "street_address_2", "city", "state", "zip_code", "yard_size_acres", "sales_manager_id"]
        field_titles = ["ID", "Street Address", "Street Address 2", "City", "State", "ZIP", "Yard Size (acres)", "Sales Manager ID", "Sales Manager Email"]
        sql_browse =  """SELECT h.id, h.street_address, h.street_address_2, h.city, h.state, h.zip_code, 
            h.yard_size_acres, h.sales_manager_id, s.email AS sales_manager_email FROM houses h LEFT JOIN sales_managers s ON h.sales_manager_id = s.id"""
        sql_insert = """INSERT INTO `houses` (`street_address`, `street_address_2`, `city`, `state`, `zip_code`, `yard_size_acres`, `sales_manager_id`)
            VALUES (%(street_address)s, %(street_address_2)s, %(city)s, %(state)s, %(zip_code)s, %(yard_size_acres)s, %(sales_manager_id)s)"""
        super().__init__(mysql, title, fields, field_titles, sql_browse, sql_insert)
        self._sql_update = """UPDATE `houses` SET `sales_manager_id` = %(sales_manager_id)s WHERE `id` = %(house_id)s"""
        self._sql_select_ids = """SELECT `id`, `street_address` FROM `houses` ORDER BY 1 ASC"""

    def insert_into(self, data: dict):
        """Given a table name and a dict of field_name:value pairs, inserts the data into table
        Returns tuple of: (True or False depending on result, status message)"""
        args = data
        print(args)
        args["sales_manager_id"] = None if args["sales_manager_id"] == "" else args["sales_manager_id"]  # change from '' to null
        args["street_address_2"] = None if args["street_address_2"] == "" else args["street_address_2"]  # change from '' to null
        return super().insert_into(args)

    def update_sales_manager(self, house_id: int, sales_manager_id: int):
        """Updates a house's sales manager"""
        query = self._sql_update
        sales_manager_id = None if sales_manager_id == "" else sales_manager_id
        args = {
            "house_id": house_id,
            "sales_manager_id": sales_manager_id
        }
        try:
            super()._execute_query(query, args)
            return True, "Successfully updated that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running UPDATE house's sales manager")
            return False, str(e)

    def select_ids(self) -> list:
        """Used top populate the dropdown list in the HTML form; returns (id, street_address)[]"""
        query = self._sql_select_ids
        return super()._execute_query(query)


class Jobs(BaseTable):
    def __init__(self, mysql) -> None:
        title = "Jobs"
        fields = ["id", "date", "total_price", "house_id"]
        field_titles = ["ID", "Date", "Total Price", "House ID", "House Address", "Worker IDs"]
        sql_browse =  """SELECT j.id, j.date, j.total_price, j.house_id, h.street_address, 
            GROUP_CONCAT(jw.worker_id SEPARATOR ', ') AS worker_ids FROM jobs j 
            LEFT JOIN job_workers jw ON j.id = jw.job_id LEFT JOIN houses h ON h.id = j.house_id GROUP BY j.id"""
        sql_insert = """INSERT INTO `jobs` (`date`, `total_price`, `house_id`) VALUES (%(date)s, %(total_price)s, %(house_id)s)"""
        super().__init__(mysql, title, fields, field_titles, sql_browse, sql_insert)
        self._sql_get_total_price = """SELECT 50 * `yard_size_acres` AS total_price FROM `houses` WHERE `id` = %(house_id)s"""
        self._sql_select_ids = """SELECT `id`, `date`, `house_id` FROM `jobs` ORDER BY 1 ASC"""
        self._sql_delete_job = """DELETE FROM `jobs` WHERE `id` = %(job_id)s"""

    def get_jobs_total_price(self, house_id) -> int:
        """Calculates and returns a job's "total_price" as an int"""
        query = self._sql_get_total_price
        args = {
            "house_id": house_id
        }
        results = super()._execute_query(query, args)
        return results[0]["total_price"]  # there will only be one row at index 0

    def insert_into(self, data: dict):
        """Given a table name and a dict of field_name:value pairs, inserts the data into table
        Returns tuple of: (True or False depending on result, status message)"""
        args = data
        print(args)
        house_id = args["house_id"]
        args["total_price"] = self.get_jobs_total_price(house_id)  # add the total price to the dict of fields to insert
        return super().insert_into(args)

    def select_ids(self) -> list:
        """Used top populate the dropdown list in the HTML form; returns (id, date, house_id)[]"""
        query = self._sql_select_ids
        return super()._execute_query(query)

    def delete(self, job_id):
        """Delete a job worker table entry"""
        query = self._sql_delete_job
        args = {
            "job_id": job_id,
        }
        try:
            super()._execute_query(query, args)
            return True, "Successfully deleted that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running DELETE job worker")
            return False, str(e)


class JobWorkers(BaseTable):
    def __init__(self, mysql) -> None:
        title = "Job Workers"
        fields = ["job_id", "worker_id"]
        field_titles = ["Job ID", "Job Date", "Job House ID", "Job House Address", "Worker ID", "Worker Email"]
        sql_browse =  """SELECT jw.job_id AS job_id, j.date AS job_date, j.house_id AS job_house_id, 
            h.street_address AS job_house_address, jw.worker_id, w.email AS worker_email 
            FROM job_workers jw LEFT JOIN jobs j ON jw.job_id = j.id LEFT JOIN workers w ON jw.worker_id = w.id 
            LEFT JOIN houses h ON h.id = j.house_id"""
        sql_insert = """INSERT INTO `job_workers` (`job_id`, `worker_id`)
            VALUES (%(job_id)s, %(worker_id)s)"""
        super().__init__(mysql, title, fields, field_titles, sql_browse, sql_insert)
        self._sql_update = """UPDATE `job_workers` SET  `job_id` = %(new_job_id)s, `worker_id` = %(new_worker_id)s
            WHERE `job_id` = %(old_job_id)s AND `worker_id` = %(old_worker_id)s"""
        self._sql_delete = """DELETE FROM `job_workers` WHERE `job_id` = %(job_id)s AND `worker_id` = %(worker_id)s"""


    def update(self, old_job_id, old_worker_id, new_worker_id, new_job_id):
        """Updates a job worker table entry"""
        query = self._sql_update
        args = {
            "old_job_id": old_job_id,
            "old_worker_id": old_worker_id,
            "new_worker_id": new_worker_id,
            "new_job_id": new_job_id
        }
        try:
            super()._execute_query(query, args)
            return True, "Successfully updated that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running UPDATE job worker")
            return False, str(e)

    def delete(self, job_id, worker_id):
        """Delete a job worker table entry"""
        query = self._sql_delete
        args = {
            "job_id": job_id,
            "worker_id": worker_id,
        }
        try:
            super()._execute_query(query, args)
            return True, "Successfully deleted that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running DELETE job worker")
            return False, str(e)


class Lawnmowers(BaseTable):
    def __init__(self, mysql) -> None:
        title = "Lawnmowers"
        fields = ["id", "brand", "make_year", "model_name", "is_functional"]
        field_titles = ["ID", "Brand", "Make Year", "Model Name", "Is Functional?"]
        sql_browse =  """SELECT id, brand, make_year, model_name, CASE WHEN is_functional = 1 THEN "Yes" ELSE "No" END AS is_functional FROM lawnmowers"""
        sql_insert = """INSERT INTO `lawnmowers` (`brand`, `make_year`, `model_name`, `is_functional`)
            VALUES (%(brand)s, %(make_year)s, %(model_name)s, %(is_functional)s)"""
        super().__init__(mysql, title, fields, field_titles, sql_browse, sql_insert)
        self._sql_select_ids = """SELECT `id`, `model_name`, `make_year` FROM `lawnmowers` ORDER BY 1 ASC"""
        self._sql_update = """UPDATE `lawnmowers` SET `is_functional` = %(is_functional)s WHERE `id` = %(lawnmower_id)s"""

    def select_ids(self) -> list:
        """Used top populate the dropdown list in the HTML form; returns (id, model_name, make_year)[]"""
        query = self._sql_select_ids
        return super()._execute_query(query)

    def update_status(self, lawnmower_id: int, is_functional: int):
        """Updates whether a lawnmower is functional or not"""
        query = self._sql_update
        args = {
            "lawnmower_id": lawnmower_id,
            "is_functional": is_functional
        }
        try:
            super()._execute_query(query, args)
            return True, "Successfully updated that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running UPDATE lawnmower status")
            return False, str(e)


class SalesManagers(BaseTable):
    def __init__(self, mysql) -> None:
        title = "Sales Managers"
        fields = ["id", "region", "first_name", "last_name", "email", "phone_number"]
        field_titles = ["ID", "Region", "First Name", "Last Name", "Email", "Phone Number"]
        sql_browse =  """SELECT id, region, first_name, last_name, email, phone_number FROM sales_managers"""
        sql_insert = """INSERT INTO `sales_managers` (`region`, `first_name`, `last_name`, `email`, `phone_number`)
            VALUES (%(region)s, %(first_name)s, %(last_name)s, %(email)s, %(phone_number)s)"""
        super().__init__(mysql, title, fields, field_titles, sql_browse, sql_insert)
        self._sql_select_ids = """SELECT `id`, `email` FROM `sales_managers` ORDER BY 1 ASC"""
        self._sql_delete = """DELETE FROM `sales_managers` WHERE `id` = %(sales_manager_id)s"""

    def select_ids(self) -> list:
        """Used top populate the dropdown list in the HTML form; returns (id, email)[]"""
        query = self._sql_select_ids
        return super()._execute_query(query)

    def delete(self, sales_manager_id: int):
        """Given a sales_manager_id, deletes that record"""
        query = self._sql_delete
        args = {
            "sales_manager_id": sales_manager_id
        }
        try:
            super()._execute_query(query, args)
            return True, "Successfully deleted that entry"
        except Exception as e:
            print(e)
            logger.exception("Error running DELETE sales manager")
            return False, str(e)


class Workers(BaseTable):
    def __init__(self, mysql) -> None:
        title = "Workers"
        fields = ["id", "first_name", "last_name", "email", "phone_number", "lawnmower_id"]
        field_titles = ["ID", "First Name", "Last Name", "Email", "Phone Number", "Lawnmower ID", "Lawnmower Name", "Lawnmower Year"]
        sql_browse =  """SELECT w.id, w.first_name, w.last_name, w.email, w.phone_number, w.lawnmower_id, 
            l.model_name AS lawnmower_model_name, l.make_year AS lawnmower_make_year FROM workers w 
            LEFT JOIN lawnmowers l ON l.id = w.lawnmower_id"""
        sql_insert = """INSERT INTO `workers` (`first_name`, `last_name`, `email`, `phone_number`, `lawnmower_id`)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(lawnmower_id)s)"""
        super().__init__(mysql, title, fields, field_titles, sql_browse, sql_insert)
        self._sql_select_ids = """SELECT `id`, `email` FROM `workers` ORDER BY 1 ASC"""

    def select_ids(self) -> list:
        """Used top populate the dropdown list in the HTML form; returns (id, email)[]"""
        query = self._sql_select_ids
        return super()._execute_query(query)


class LennysDB:
    """
    Represents the database and it tables"""
    def __init__(self, mysql) -> None:
        self.mysql = mysql
        self.customer_contacts = CustomerContacts(mysql)
        self.houses = Houses(mysql)
        self.jobs = Jobs(mysql)
        self.job_workers = JobWorkers(mysql)
        self.lawnmowers = Lawnmowers(mysql)
        self.sales_managers = SalesManagers(mysql)
        self.workers = Workers(mysql)    
