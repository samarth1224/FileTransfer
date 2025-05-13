import sys
from socket import *
import time
import json
import struct
class ReceivingClient():
    def __init__(self,server_port):
        self.server_port = server_port
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(("", self.server_port))
        self.server_socket.listen(1)

    def create_connection_socket(self):
        self.connection_socket,self.address = self.server_socket.accept()
        return self.connection_socket

    def _recv_header(self):
        """ Deal with Header/Meta data """

        header_size = self.connection_socket.recv(4)
        print(f'header = {header_size}')
        print(f'len heder = {len(header_size)}')
        if not header_size:
            return {}
        json_header = self.connection_socket.recv(struct.unpack("!I", header_size)[0])
        print(f'json header {json_header}')

        return json.loads(json_header)


    def recv_file(self):
        """ recieve file data """

        recieved_bytes = b''
        file_type = None
        try:
            header = self._recv_header()
            file_type = header["file_type"]
            kb = header["file_size"]
            for i in range(kb):
                recieved_bytes += self.connection_socket.recv(1024)
            # print(f'total_recived_bytes = {len(recieved_bytes)}')
            return  (recieved_bytes,file_type)
        except (KeyError):
            return (None,None)

    def save_file(self,recieved_bytes,file_type,file_path):
        if recieved_bytes is None or file_type == None:
            print("No data")
        else:
            with open(f"{file_path}", 'wb') as file:
                file.write(recieved_bytes)
        self.connection_socket.close()

    def close_connection(self):
        self.server_socket.close()