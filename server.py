import select
import socket
import datetime
import sqlite3 as sql

# Define last_date function
def last_date():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    return str(current_date)
print(last_date())


# define and create database if not exists:
##########################################
db_file = "data.sqlite"

sql_create_table = """
CREATE TABLE IF NOT EXISTS station_status (
	station_id INT,
	alarm1 INT,
	alarm2 INT,
	last_date TEXT,
	PRIMARY KEY(station_id)
);
"""

sql_select_all_stations = """
SELECT rowid, *
FROM station_status;
"""

sql_insert_message = """
INSERT INTO station_status VALUES
(?, ?, ?, ?);
"""

with sql.connect(db_file) as conn:
    cur = conn.cursor()
    cur.execute(sql_create_table)
    conn.commit()

#############################################

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen(16)

# List to keep track of connected clients
client_sockets = [server_socket]

print('Server is running...')

# Main server loop
###############################################
while True:
    # Use select to monitor socket activity
    readable, _, _ = select.select(client_sockets, [], [])
    # Iterate through connections
    for sock in readable:
        if sock is server_socket:
            # New client connection
            client_socket, address = server_socket.accept()
            client_sockets.append(client_socket)
            print('New client connected:', address)
        else:
            # Incoming data from a client
            data = sock.recv(1024).decode()
            if data:
                print('Received data:', data)
                # Enter received data to database:
                with sql.connect(db_file) as conn:
                    conn.execute(sql_insert_message, (station_id, alarm1, alarm2, last_date))
                # Return reply to the client
                sock.sendall(data.encode())
            else:
                # Client has closed the connection
                print('Client disconnected:', sock.getpeername())
                sock.close()
                client_sockets.remove(sock)
