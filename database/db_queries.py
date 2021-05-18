import MySQLdb

def select_all(db_connection, sql_table_name):
    query = f"""SELECT * FROM {sql_table_name}"""
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, args=None)
    db_connection.commit()
    results = cursor.fetchall()
    return results

def search_contacts(db_connection, first_name, last_name):
    query = f"""SELECT * FROM `customer_contacts` 
    WHERE `first_name` LIKE '%{first_name}%' AND `last_name` LIKE '%{last_name}%'"""
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, args=None)
    db_connection.commit()
    results = cursor.fetchall()
    print(results)
    return results