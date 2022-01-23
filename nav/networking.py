import time
import socket
import threading


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

        self.last_checked = time.time()


    def listener__(self):

        while self.running:

            buffer = self.server.recvfrom(self.bufferSize)
            if buffer:
                if buffer.decode() == "checked":
                    self.last_checked = time.time()
                    print("checked")
                else:
                    print(f"[{buffer[1]}] : {buffer[0]}")
                    self.recieved.append(buffer[0].decode())

                if time.time() - self.last_checked >= 5000:
                    print("not checked")
                    self.recieved.append("3x0000")

        self.running = False


    def listener(self):

        threading._start_new_thread(self.listener__, ())
