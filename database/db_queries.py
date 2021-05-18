import MySQLdb

def select_all(db_connection, sql_table_name):
    query = f"""SELECT * FROM {sql_table_name}"""
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, args=None)
    db_connection.commit()
    results = cursor.fetchall()
    return results