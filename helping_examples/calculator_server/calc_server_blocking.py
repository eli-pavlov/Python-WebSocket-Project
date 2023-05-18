import socket

with socket.socket() as s:
    s.bind(('', 0))
    s.listen(10)
    client_list = []


    ip, port = s.getsockname()
    print("listening on {}:{}.".format(ip,port))

    while True:
        print('''
        1) accept client
        2) receive message
        0) quit
        ''')

        inp = input("enter option:")

        if inp == '1':
            client_and_address = s.accept()
            client_list.append(client_and_address)

        elif inp == '2':

            for i, client in enumerate(client_list):
                print("%d %s" % (i, client))

            client_num = int(input("enter client index:"))

            if 0 <= client_num and client_num < len(client_list):
                c = client_list[client_num][0]

                message = c.recv(1024).decode()
                words = message.split()
                num1 = int(words[0])
                sign = words[1]
                num2 = int(words[2])

                result = "invalid message"

                if sign == "+":
                    result = str(num1 + num2)
                elif sign == "-":
                    result = str(num1 - num2)
                elif sign == "*":
                    result = str(num1 * num2)

                c.send(result.encode())

        elif inp == '0':
            break
        else:
            print("error: not a valid option")
    print("goodbye")
