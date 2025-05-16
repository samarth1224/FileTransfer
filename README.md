A simple File Transfer client made using Socket module of Python,and GUI created using PySide6.
I have used Socket module to create a TCP connection, for sending and recving files.
I created this mostly because i just read a computer networking book to quench my thirst of learning "how internet works", and partially because i needed a file transfer app to send
files from android phone to PC without connecting to Global internet. But i am yet to create a client for android. Although i plane to create one in future.

NOTE: PySide6 and Socket Module of Python are must requirment to run this project.

This project contains 3 python file, server.py, GUI.py, and client.py.
1) server.py
  -> This contains the class ReciveingClient for establishing the server, creating and accepting the TCP connection, and at last recving the file.
  -> After establishing connection with client, the server start recving the header. The header contains metadata about the file(in JSON format) , including file type and file size.
   This meta data is used for deciding the amount of time the for loop will run in recv_file function.
  -> server.py also contains, save_file function, which is called when the server has succefully recived the full file.

2) client.py
  -> This contains the class SendFileClient, it is used establish client connection with server.
  -> It contains the methods to get file size and file type and dump it in the json to send it as header.

3) GUI.py
   -> This file implements the GUI using PySide6.
   -> This file act as main file utilizing classes from both server.py and client.py.
   -> The GUI currently implemented is very basic and naive looking, but can be easily stylized later on.
   -> The aim of the project was to use TCP connection to get to create a usable file transfer application and to learn, what challengs comes in the way when creating a network application
       from the ground up using sockets.
