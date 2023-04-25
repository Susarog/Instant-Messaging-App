import sys
import socket
import threading

HOST = socket.gethostname()  
PORT = int(sys.argv[1])
# need a lock when adding/deleting clients
CLIENTS = dict()

def thread_callback(conn):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            if data == b"EX":
                return
            elif data == b"BM":
                conn.sendall(b"Enter Public Message:")
                data = conn.recv(1024)
                for _, (user, conn) in enumerate(CLIENTS.items()):
                    conn.sendall(data)
            elif data == b"DM":
                return
            else:
                print("Incorrect command, Please Try Again")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    thread_list = list()
    print("Waiting for connection...")
    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        data = conn.recv(1024)
        if not data:
            break
        CLIENTS[data.decode("utf-8")] = conn
        conn.sendall(data)
        current_thread = threading.Thread(target=thread_callback, args=(conn,))
        thread_list.append(current_thread)
        current_thread.start()
