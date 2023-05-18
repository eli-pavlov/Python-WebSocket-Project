import select
import socket

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen(5)

# List to keep track of connected clients
client_sockets = [server_socket]

print('Server is running...')

while True:
    # Use select to monitor socket activity
    readable, _, _ = select.select(client_sockets, [], [])

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
                # Echo the received data back to the client
                sock.sendall(data.encode())
            else:
                # Client has closed the connection
                print('Client disconnected:', sock.getpeername())
                sock.close()
                client_sockets.remove(sock)
