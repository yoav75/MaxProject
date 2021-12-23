from socket import *
import threading

SERVER_ADDRESS = ("0.0.0.0", 5053)
client_list = []


class ThreadClass(threading.Thread):
    def __init__(self, val):
        threading.Thread.__init__(self)
        self.val = val

    def getName(self):
        return self.val

    def run(self):
        while True:
            m = (self.val.recv(1024)).decode()
            print(m)
            if not m:
                break
            for i in client_list:
                i.send(("server says " + m).encode())



class Server(ThreadClass):
    def __init__(self):
        print("init")
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(SERVER_ADDRESS)
        self.socket.listen(3)  # The serversock is listening to requests

    def run_server(self):
        print("run_server")
        while True:
            global clientList
            print("Waiting for connection..")
            clientsock, addr = self.socket.accept()
            print("Connected from:", addr)
            client_list.append(clientsock)
            th1 = ThreadClass(clientsock)
            th1.start()



s = Server()
s.run_server()