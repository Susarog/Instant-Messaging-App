import socket
import sys
import threading
import errno
import struct

HOST = socket.gethostname()  
PORT = int(sys.argv[1])
USERNAME = sys.argv[2]
thread = -1 

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
    print(data)
    return data

def receive_messages(socket):
    while True:
        data = recv_msg(socket)
        if data == None:
            break;
        print(f"Message received: {data.decode()}\n""Please enter a command (BM: Broadcast Messaging, EX: Exit): ")
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        send_msg(s,USERNAME.encode())
        thread = threading.Thread(target=receive_messages, args=(s,),daemon=True)
        thread.start()
        while True:
            client_input = input("Please enter a command (BM: Broadcast Messaging, EX: Exit):\n")
            if client_input == "EX":
                data_message = (client_input + ' ' + USERNAME).encode();
                send_msg(s,data_message)
                break
            elif client_input == "BM":
                msg = input("Enter Public Message:\n")
                data_message = (client_input + ' '+ USERNAME + ' ' + msg).encode(); 
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
