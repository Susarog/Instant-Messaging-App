import socket
import sys

HOST = socket.gethostname()  
PORT = int(sys.argv[1])
USERNAME = sys.argv[2]

def send_input(socket):
    client_input = input()
    socket.sendall(bytes(client_input, "utf-8"))
    data = socket.recv(1024)
    print(data.decode('utf-8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #username to server to keep track of
    s.sendall(bytes(USERNAME, "utf-8"))
    data = s.recv(1024)
    while True:
        print("Please enter a command (BM: Broadcast Messaging, DM: Direct Messaging, EX: Exit)")
        # need threading for input and detecting if there is a recv
        send_input(s)
