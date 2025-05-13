# from socket import *
# serverName = 'servername'
# serverPort = 12000
# clientSocket = socket(AF_INET, SOCK_STREAM)
# clientSocket.connect(('127.0.0.1', serverPort))
# sentence = input('Input lowercase sentence:')
# clientSocket.send(sentence.encode())
# print("sent")
# modifiedSentence = clientSocket.recv(1024)
# print('From Server: ', modifiedSentence.decode())
# clientSocket.close()
import sys
import time
import os
import struct
import json
from socket import *
from PySide6 import QtCore,QtWidgets




# class window(QtWidgets.QWidget):
#     def __init__(self,parent=None):
#         super().__init__(parent)
#         self.setFixedSize(400,400)
#         self.setWindowTitle("Client")
#
#
#     def send_file(self):
#



# Create a UDP client socket
# clientSocket = socket(AF_INET, SOCK_STREAM)
# clientSocket.connect(('127.0.0.1', 61054))
#
#
#
# def get_file_size(filepath):
#     """Returns the size of a file in bytes. Returns -1 if the file does not exist or an error occurs"""
#     try:
#         size = os.path.getsize(filepath)
#         print(size)
#         return size
#     except FileNotFoundError:
#         print(f"File not found: {filepath}")
#         return -1
#     except OSError as e:
#         print(f"An OS error occurred: {e}")
#         return -1
#
#
# file_size = int(get_file_size("C:\\Users\\OM\\PycharmProjects\\pythonProject3\\telgram.png")/1024)
# print(file_size)
#
# file_metadata= {
#     "file_type":"png",
#     "file_size":file_size+1
# }
#
# file_metadata_header = json.dumps(file_metadata)
# header_size = len(file_metadata_header)
# print(header_size)
#
# print(sys.getsizeof(struct.pack("!I", header_size)))
# header_with_length = file_metadata_header.encode() + struct.pack("!I", header_size)
# print(sys.getsizeof(header_with_length))
# print(len(header_with_length))
# clientSocket.send(header_with_length)
#
#
#
#
# with open("C:\\Users\\OM\\PycharmProjects\\pythonProject3\\telgram.png",'rb') as recived_file:
#     print(f'file size sys {sys.getsizeof(recived_file)}')
#     # print(f'file size len {len(recived_file)}')
#     while (chunk := recived_file.read(1024)) != b'':
#
#         # print(chunk)
#         # clientSocket.send(file_size.encode())
#         print(clientSocket.send(chunk))
#
#
#  # clientSocket.send("png".encode(encoding="utf-8"))
#
#
#
#
#
#     # Close the socket
# time.sleep(10)
# clientSocket.send(header_with_length)
# print('closing')
# clientSocket.close()


class SendFileClient:
    def __init__(self,server_port,ip_address):
        self.server_port = server_port
        self.ip_address = ip_address
        self.clientSocket = socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect ((ip_address,server_port))

    def get_file_size(self,file_path):
        """Returns the size of a file in bytes. Returns -1 if the file does not exist or an error occurs"""
        try:
            size = os.path.getsize(file_path)
            print(size)
            return size
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return -1
        except OSError as e:
            print(f"An OS error occurred: {e}")
            return -1

    def send_header(self,file_path):
        file_size = int(self.get_file_size(file_path) / 1024)
        file_type = file_path.split('\\')[-1].split('.')[-1]
        print(file_size)
        print(file_type)

        file_metadata = {
            "file_type": file_type,
            "file_size": file_size + 1
        }

        file_metadata_header = json.dumps(file_metadata)
        header_size = len(file_metadata_header)
        print(header_size)

        print(sys.getsizeof(struct.pack("!I", header_size)))
        header_with_length = struct.pack("!I", header_size) + file_metadata_header.encode()
        print(sys.getsizeof(header_with_length))
        print(len(header_with_length))

        self.clientSocket.send(header_with_length)



    def send_file(self,file_path):
        file_path = file_path.replace("/", "\\\\")
        self.send_header(file_path)
        with open(file_path, 'rb') as recived_file:
            print(f'file size sys {sys.getsizeof(recived_file)}')
            # print(f'file size len {len(recived_file)}')
            while (chunk := recived_file.read(1024)) != b'':
                # print(chunk)
                # clientSocket.send(file_size.encode())
                print(self.clientSocket.send(chunk))

    def close_connection(self):
        print('closing')
        self.clientSocket.close()






