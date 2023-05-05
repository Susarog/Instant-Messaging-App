import struct
FORMAT = 'utf-8'

def send_msg(sock, msg):
    """
    sends a message with the byte length of the message
        Params:
            socket (socket): A socket object
            msg: str
        Returns: 
            None 
    """
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def send_encoded_msg(sock,msg):
    """
    Encodes a message to FORMAT and sends to socket
        Params:
            socket (socket): A socket object
            msg: str
        Returns: 
            None 
    """
    data_message = msg.encode(FORMAT) 
    send_msg(sock,data_message)

def recv_msg(sock):
    """
    receives size of stream to receive size of 
    message then recieves the rest of the message
        Params:
            socket (socket): A socket object
        Returns: 
            A bytearray containing the stream 
            of bytes recieved from the socket
    """
    raw_msglen = recv_all(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recv_all(sock, msglen)

def recv_all(sock, n):
    """
    helper function that receives all bytes from the socket
        Params:
            socket (socket): A socket object
            n: size
        Returns: 
            A bytearray containing the stream 
            of bytes recieved from the socket
    """
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
