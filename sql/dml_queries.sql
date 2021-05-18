-------------------------------------------------
-- BROWSE [TABLE] SECTIONS ------------------
-------------------------------------------------
-- these are for the Browse {TABLE} sections of each page of the site
SELECT * FROM `job`
SELECT * FROM `job_workers`
SELECT * FROM `workers`
SELECT * FROM `houses`
SELECT * FROM `lawnmowers`
SELECT * FROM `sales_managers`
SELECT * FROM `customer_contacts`


-------------------------------------------------
-- ADD A NEW [ENTITY] SECTIONS ------------------
-------------------------------------------------
-- these are for the Add a new {ENTITY} sections of each page of the site
-- the syntax {} denotes where user input will be inserted into the query

-- add a new job
INSERT INTO `jobs` (`date`, `total_price`, `house_id`)
VALUES ({date}, {total_price_calculation}, {house_id})

-- add a new job: perform the total_price_calculation referenced above
SELECT 50 * `yard_size_acres` FROM `houses` WHERE `id` = {house_id}

-- add a new job: populate the house id dropdown
SELECT `id` FROM `houses` ORDER BY 1 ASC

-- add a new job worker
INSERT INTO `job_workers` (`job_id`, `worker_id`)
VALUES ({job_id}, {worker_id})

-- add a new job worker: populate the job_id dropdown
SELECT `id` FROM `jobs` ORDER BY 1 ASC

-- add a new job worker: populate the worker_id dropdown
SELECT `id` FROM `workers` ORDER BY 1 ASC

-- add a new worker
INSERT INTO `workers` (`first_name`, `last_name`, `email`, `phone_number`, `lawnmower_id`)
VALUES ({first_name}, {last_name}, {email}, {phone_number}, {lawnmower_id})
-- add a new worker: populate the lawnmower_id dropdown
SELECT `id` FROM `lawnmowers` ORDER BY 1 ASC

-- add a new house
INSERT INTO `houses` (`street_address`, `street_address_2`, `city`, `state`, `zip_code`, `yard_size_acres`, `sales_manager_id`)
VALUES ({street_address}, {street_address_2}, {city}, {state}, {zip_code}, {yard_size_acres}, {sales_manager_id})

-- add a new house: populate the sales manager id dropdown
SELECT `id` FROM `sales_managers` ORDER BY 1 ASC

-- add a new lawnmower
INSERT INTO `lawnmowers` (`brand`, `make_year`, `model_name`, `is_functional`)
VALUES ({brand}, {make_year}, {model_name}, {is_functional})

-- add a new sales manager
INSERT INTO `sales_managers` (`region`, `first_name`, `last_name`, `email`, `phone_number`)
VALUES ({region}, {first_name}, {last_name}, {email}, {phone_number})

-- add a new customer contact
INSERT INTO `customer_contacts` (`first_name`, `last_name`, `email`, `phone_number`, `house_id`)
VALUES ({first_name}, {last_name}, {email}, {phone_number}, {house_id})

-- add a new customer contact: populate the house id dropdown
SELECT `id` FROM `houses` ORDER BY 1 ASC

-------------------------------------------------
-- UPDATE [ENTITY] SECTIONS ------------------
-------------------------------------------------
-- these are for the Update Record sections of each page of the site
-- the syntax {} denotes where user input will be inserted into the query

-- update a job
UPDATE `jobs` SET 
    `date` = {date},
    `total_price` = {total_price},
    `house_id` = {house_id}
WHERE `id` = {job_id}

-- update a job worker
-- will need both the old values and the new values
UPDATE `job_workers` SET 
    `job_id` = {new_job_id},
    `worker_id` = {new_worker_id}
WHERE `job_id` = {old_job_id} AND `worker_id` = {old_worker_id}

-- update a house's sales_manager_id
UPDATE `houses` SET 
    `sales_manager_id` = {sales_manager_id}
WHERE `id` = {house_id}

-- update a lawnmowers's is_functional
UPDATE `lawnmowers` SET 
    `is_functional` = {is_functional}
WHERE `id` = {lawnmower_id}

-------------------------------------------------
-- DELETE [ENTITY] SECTIONS ------------------
-------------------------------------------------
-- these are for the Delete Record sections of each page of the site
-- the syntax {} denotes where user input will be inserted into the query

-- delete a job
DELETE FROM `jobs` WHERE `id` = {job_id}

-- delete a job worker
DELETE FROM `job_workers` WHERE `job_id` = {job_id} AND `worker_id` = {worker_id}

-- delete a sales manager
DELETE FROM `sales_managers` WHERE `id` = {sales_manager_id}

-------------------------------------------------
-- SEARCH [ENTITY] SECTIONS ------------------
-------------------------------------------------
-- this is for the Search Customer Contacts by Name section 
-- the syntax {} denotes where user input will be inserted into the query

SELECT * FROM `customer_contacts` 
WHERE `first_name` LIKE %{first_name}% AND `last_name` LIKE %{last_name}%