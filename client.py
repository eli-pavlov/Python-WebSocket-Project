import socket
from time import sleep


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

while True:
    with open("status.txt", "r") as status:
        data = status.read()
    print(data)
    sleep(60)
#     message = input('Enter message (or "exit" to quit): ')
#     if message == 'exit':
#         break
#     client_socket.sendall(message.encode())
#     response = client_socket.recv(1024).decode()
#     print('Server response:', response)
#
# client_socket.close()
