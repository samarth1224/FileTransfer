import os
import struct
import json
from socket import *


class SendFileClient:
    def __init__(self,server_port,ip_address):
        self.server_port = server_port
        self.ip_address = ip_address
        self.clientSocket = socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect ((ip_address,server_port))

    def send_header(self,file_path):

        file_size = int(os.path.getsize(file_path) / 1024)
        file_type = file_path.split('\\')[-1].split('.')[-1]

        file_metadata = {
            "file_type": file_type,
            "file_size": file_size + 1
        }
        file_metadata_header = json.dumps(file_metadata)
        header_size = len(file_metadata_header)
        header_with_length = struct.pack("!I", header_size) + file_metadata_header.encode()
        self.clientSocket.send(header_with_length)

    def send_file(self,file_path):
        file_path = file_path.replace("/", "\\\\")
        self.send_header(file_path)
        with open(file_path, 'rb') as recived_file:
            while (chunk := recived_file.read(1024)) != b'':
              self.clientSocket.send(chunk)

    def close_connection(self):

        self.clientSocket.close()






