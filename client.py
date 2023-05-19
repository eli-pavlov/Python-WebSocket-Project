import socket
from time import sleep

DELAY_BETWEEN_REPORTS = 5  # Seconds

while True:
    try:
        print("\nConnecting to Server...")
        with open("status.txt", "r") as status:
            data = status.read()
            check_list = data.splitlines()
            for item in check_list:
                if type(int(item)) != int:
                    raise Exception("Wrong data in file")
    except Exception as e:
        print("\nCould not open status file or invalid data,\nTry updating status file manually")
    else:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', 5000))
        except Exception as e:
            print("Failed to connect to server...\nTrying again in 60 seconds")
        else:
            message = str(data.split("\n"))
            print(f"Sending message: {message}")
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024).decode()
            print('Response from Server:', response)
            client_socket.close()
    sleep(DELAY_BETWEEN_REPORTS)
