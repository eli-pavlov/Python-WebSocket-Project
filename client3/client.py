import socket
from time import sleep

while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 5000))
    except Exception as e:
        print("Failed to connect to server...\nTrying again in 60 seconds")
    else:
        with open("status.txt", "r") as status:
            data = status.read()
        message = str(data.split("\n"))
        print(f"Sending message: {message}")
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        print('Server response:', response)
        client_socket.close()
    sleep(60)
