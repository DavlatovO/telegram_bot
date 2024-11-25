import mysql.connector

def save_user(id, is_bot, first_name, username, type, message_text):
    con = mysql.connector.connect(
        user='root',
        password='siuu',
        host='127.0.0.1',
        port=3306,
        database='bot_database'
    )

    cursor = con.cursor()

    # Use parameterized queries to safely insert data
    query1 = '''INSERT INTO Users (id, is_bot, first_name, username, type)
                VALUES (%s, %s, %s, %s, %s);'''

    query2 = '''INSERT INTO messages (user_id, message_text)
                VALUES (%s, %s);'''

    # Execute the queries with data passed as tuple parameters
    cursor.execute(query1, (id, is_bot, first_name, username, type))
    cursor.execute(query2, (id, message_text))

    # Commit the transaction to save the changes
    con.commit()

    cursor.close()
    con.close()
