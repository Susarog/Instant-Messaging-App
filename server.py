import sys
import socket
import threading
import struct

HOST = socket.gethostname()  
PORT = int(sys.argv[1])
CLIENTS = dict()
lock = threading.Lock()
threads = list()

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def thread_callback(conn, addr):
    with conn:
        while True:
            data = recv_msg(conn)
            if not data or data == None: break
            (command, username, *msg) = data.decode().split()
            if command == "EX":
                lock.acquire()
                del CLIENTS[username]
                lock.release()
                print(f"Connection closed by {addr}")
                break
            elif command == "BM":
                msg = ' '.join([str(word) for word in msg])
                print(msg)
                lock.acquire()
                for _, (client, conn) in enumerate(CLIENTS.items()):
                    if (not client == username):
                        send_msg(conn, msg.encode())
                lock.release()
            else:
                print(data)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for connection...")
        while True:
            conn, addr = s.accept()
            data = recv_msg(conn)
            if not data:
                break
            lock.acquire()
            CLIENTS[data.decode()] = conn
            lock.release()
            current_thread = threading.Thread(target=thread_callback, args=(conn,addr, ),daemon=True)
            threads.append(current_thread)
            current_thread.start()
except KeyboardInterrupt:
    if s:
        s.close()
    for thread in threads:
        thread.join()
    sys.exit(0)
