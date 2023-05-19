import sqlite3
from time import sleep

while True:
    # Connect to the SQLite database
    conn = sqlite3.connect('data.sqlite')
    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute('SELECT * FROM station_status')
    rows = cursor.fetchall()

    # Display the retrieved rows
    for row in rows:
        print(row)
    print("\n")

    # Close the connection
    conn.close()
    sleep(60)
