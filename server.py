import select
import socket
import datetime
import sqlite3 as sql


# Define last_date function
def current_date():
    now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    return str(now_date)

# define and create database if not exists:
##########################################
db_file = "data.sqlite"

# Create table instructions as variable
sql_create_table = """
CREATE TABLE IF NOT EXISTS station_status (
	station_id INT,
	last_date TEXT,
	alarm1 INT,
	alarm2 INT,
	PRIMARY KEY(station_id)
);
"""

# SQL INJECTION protection.
# Formatting incoming data as INTEGERS only, and using placeholders for input.
def sql_new_data(station_id, alarm1, alarm2):
    data_dict = {
        'station_id': int(station_id),
        'alarm1': int(alarm1),
        'alarm2': int(alarm2),
    }
    return data_dict

# Create the table
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

print('Server is running...\n')

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
            print('Client connected on:', address)
        else:
            # Incoming data from a client
            data = sock.recv(1024).decode()
            if data:
                data = eval(data)
                # Incoming message type check for additional SQL injection protection
                try:
                    for item in data:
                        if type(int(item)) != int or len(item) > 10000:
                            raise Exception ("Invalid Message")
                except Exception as e:
                    print(f"Invalid Message received from {address}\nDatabase was not updated.")
                    response = "Invalid message received"
                # If message OK, proceed with DB status update
                else:
                    print(f"Received data from Station {data[0]} on port {address[1]}: {data}")
                    new_data = sql_new_data(data[0], data[1], data[2])
                    date = current_date()
                    # Enter received data to database:
                    with sql.connect(db_file) as conn:
                        cur = conn.cursor()
                        # Check if a row with the given name already exists
                        cur.execute('SELECT * FROM station_status WHERE station_id = ?', (new_data['station_id'],))
                        existing_row = cur.fetchone()
                        if existing_row:
                            # If the row exists, update it
                            cur.execute('''
                                UPDATE station_status
                                SET last_date = ?, alarm1 = ?, alarm2 = ? 
                                WHERE station_id = ?
                            ''', (date, new_data['alarm1'], new_data['alarm2'], new_data['station_id']))
                            print(f'Existing row updated for Station {data[0]}.')
                        else:
                            # If the row doesn't exist, insert a new row
                            cur.execute('''
                                INSERT INTO station_status (station_id, last_date, alarm1, alarm2)
                                VALUES (?, ?, ?, ?)
                            ''', (new_data['station_id'], date, new_data['alarm1'], new_data['alarm2']))
                            print(f'New row inserted for Station {data[0]}.')
                        conn.commit()
                        response = "Status received successfully"
                # Return reply to the client
                sock.sendall(response.encode())
            else:
                # Client has closed the connection
                print('Client disconnected to save resources:', sock.getpeername(),'\n')
                sock.close()
                client_sockets.remove(sock)
