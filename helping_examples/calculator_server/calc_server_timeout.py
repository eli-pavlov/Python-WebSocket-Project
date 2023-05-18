import socket
import sys  # for exit


# client class object to make it easier to identify its elements
class Client:
    def __init__(self, socket=None, ip=None, port=None):
        self.socket = socket
        self.ip = ip
        self.port = port


## MAIN ##
try:
    # server preperation

    ip = input("set ip address bind:")
    port = int(input("set port bind:"))
    s = socket.socket()
    s.bind((ip, port))
    s.listen(10)
    # set timeout to a small number (millisecond) to make it non-blocking
    s.settimeout(0.001)
    client_list = []

    server_messages = ""
    something_changed = True

    # server loop
    while True:
        if something_changed:
            # "clear" the screen
            print("\n" * 100)
            # print server data
            print()
            print("listening on ", ip, ":", port)
            print("press ctrl+C to quit")
            print()
            # print current list of client
            if len(client_list) == 0:
                print("\tthere are no client connected\t")
            else:
                for i, client in enumerate(client_list):
                    print("%d) %s:%d" % (i, client.ip, client.port))

            print()
            print(server_messages)
            something_changed = False

        # try to accept a new client and add it to the list
        c = None
        try:
            c = s.accept()
        # don't do anything if we don't find any
        except socket.error:
            pass

        if c != None:
            c = Client(socket=c[0], ip=c[1][0], port=c[1][1])
            # set low timeout so recv won't block
            c.socket.settimeout(0.001)
            client_list.append(c)
            something_changed = True
            server_messages = "new client accepted"

        # check each client check for a message and respond
        # using list() to make a copy so we can remove form the orignal list
        for client in list(client_list):

            cs = client.socket

            message = None
            result = "invalid message"

            try:
                message = cs.recv(1024).decode()

                # empty string on recv --> client closed
                if message == "":
                    client_list.remove(client)
                    server_messages = "{}:{} has disconnected.".format(
                        client.ip, client.port)

                    something_changed = True
                    continue

                words = message.split()
                num1 = int(words[0])
                sign = str(words[1])
                num2 = int(words[2])

                if sign == "+":
                    result = num1 + num2
                elif sign == "-":
                    result = num1 - num2
                elif sign == "*":
                    result = num1 * num2


            except socket.error:
                message = None
            except ValueError:
                result = "invalid message"

            if message != None:
                cs.send(str(result).encode())
                something_changed = True
                server_messages = 'from {0}:{1}\nrecv: {2}\nsend:{3}'.format(
                    client.ip, client.port, message, result)
except KeyboardInterrupt:
    pass
finally:
    '''
    print "closing each client socket"
    for c in client_list:
        c.socket.send("goodbye")
        c.socket.close()
    '''
    print()
    print("closing server socket")
    s.close()
    print("goodbye")