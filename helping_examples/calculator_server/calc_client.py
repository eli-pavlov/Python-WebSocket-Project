import socket

with socket.socket() as s:
    ip = input("enter ip:")
    port = int(input("enter port:"))

    s.connect((ip, port))

    while True:
        inp = input("enter calcualtion ('q' = quit):")

        if inp == 'q' or inp == 'Q':
            break

        s.send(inp.encode())
        res = s.recv(1024).decode()

        print("result =", res)

    print("goodbye")