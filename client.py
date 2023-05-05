import socket
import sys
import threading
import errno
from util import *

FORMAT = 'utf-8'
HOST = socket.gethostname()  
PORT = int(sys.argv[1])
USERNAME = sys.argv[2]

def receive_messages(socket):
    while True:
        data = recv_msg(socket)
        if data == None:
            break
        print(f"Message received: {data.decode(FORMAT)}\n""Please enter a command (BM: Broadcast Messaging, EX: Exit): ")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        send_msg(s,USERNAME.encode(FORMAT))
        thread = threading.Thread(target=receive_messages, args=(s,),daemon=True)
        thread.start()
        while True:
            client_input = input("Please enter a command (BM: Broadcast Messaging, EX: Exit):\n")
            if client_input == "EX":
                data_message = (client_input + ' ' + USERNAME).encode(FORMAT)
                send_msg(s,data_message)
                break
            elif client_input == "BM":
                msg = input("Enter Public Message:\n")
                data_message = (client_input + ' '+ USERNAME + ' ' + msg).encode(FORMAT) 
                send_msg(s,data_message)
            else:
                print("Incorrect command, Please Try Again")
        thread.join()
except (EOFError, KeyboardInterrupt):
    if s:
        s.close()
except (socket.error, ConnectionRefusedError) as err:
    print("Server is off or incorrect port")
    if err.errno == errno.EPIPE:
        s.close()
