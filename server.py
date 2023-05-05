import sys
import socket
import threading
from util import *

FORMAT = 'utf-8'
HOST = socket.gethostname() 
PORT = int(sys.argv[1])
CLIENTS = dict()
lock = threading.Lock()
threads = list()

def thread_callback(conn, addr):
    with conn:
        while True:
            data = recv_msg(conn)
            if data == None: break
            (command, username, *msg) = data.decode(FORMAT).split()
            if command == "EX":
                with lock:
                    del CLIENTS[username]
                break
            elif command == "BM":
                msg = ' '.join([str(word) for word in msg])
                with lock:
                    for _, (client, client_conn) in enumerate(CLIENTS.items()):
                        if (not client == username):
                            send_msg(client_conn, msg.encode(FORMAT))
            else:
                print(data)
        print(f"Connection closed by {addr}")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for connection...")
        while True:
            conn, addr = s.accept()
            data = recv_msg(conn)
            if not data:
                break
            with lock:
                CLIENTS[data.decode(FORMAT)] = conn
            current_thread = threading.Thread(target=thread_callback, args=(conn, addr ))
            threads.append(current_thread)
            current_thread.start()
except KeyboardInterrupt:
    if s:
        s.close()
    for thread in threads:
        thread.join()
    sys.exit(0)
