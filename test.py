import socket
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(str(sys.argv[1]).encode(), ("169.254.42.45", 8081))