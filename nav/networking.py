import socket
import threading
from time import sleep


class Networking:

    def __init__(self, host, port, bufferSize):

        self.host = host
        self.port = port
        self.running = True
        self.recieved = []
        self.bufferSize = bufferSize
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))
        print("Server started")


    def listener__(self):

        while self.running:

            buffer = self.server.recvfrom(self.bufferSize)
            if buffer:
                print(f"[{buffer[1]}] : {buffer[0]}")
                self.recieved.append(buffer[0].decode())


    def listener(self):

        threading._start_new_thread(self.listener__, ())