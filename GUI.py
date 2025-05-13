import sys
from PySide6 import QtCore,QtWidgets
from PySide6.QtGui import QIntValidator
from main import ReceivingClient
from client import SendFileClient

class MainWindow(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setFixedSize(400,400)
        self.setWindowTitle("Main window")



        self.main_layout = QtWidgets.QVBoxLayout(self)

        #stacked Widget
        self.stacked = QtWidgets.QStackedWidget()
        self.main_layout.addWidget(self.stacked)

        #main_frame_in_stacked_widget
        self.main_frame = QtWidgets.QFrame(parent = self.stacked)
        self.main_frame_layout = QtWidgets.QVBoxLayout(self.main_frame)


        # Recieve  Button
        self.recv_button = QtWidgets.QPushButton(parent = self.main_frame,text = "Receive")
        self.recv_button.setStyleSheet("QPushButton{ background-color: yellow; color: black; }")
        self.main_frame_layout.addWidget(self.recv_button)
        self.recv_button.clicked.connect(lambda : self.stacked.setCurrentIndex(1))

        #Send Button
        self.send_button = QtWidgets.QPushButton(parent=self.main_frame, text="Send")
        self.send_button.setStyleSheet("QPushButton{ background-color: yellow; color: black; }")
        self.main_frame_layout.addWidget(self.send_button)
        self.send_button.clicked.connect(lambda : self.stacked.setCurrentIndex(2))


        # RECV SERVER PAGE
        self.recv_frame = QtWidgets.QFrame(parent = self.stacked)
        self.recv_frame.setStyleSheet("QFrame{ background-color: red;}")
            #buttons and Line Edit
        self.recv_back_to_home_button = QtWidgets.QPushButton(parent= self.recv_frame,text= "Home Page")
        self.recv_back_to_home_button.setStyleSheet("QPushButton{ background-color: yellow; color: black; }")
        self.recv_back_to_home_button.clicked.connect(lambda : self.stacked.setCurrentIndex(0))
        self.start_recving = QtWidgets.QPushButton(parent = self.recv_frame,text = "Reciev",)
        # self.start_recving.setEnabled(False)
        self.start_recving.clicked.connect(self.recv_file_button_clicked)
        self.start_recving.setStyleSheet("QPushButton{ background-color: yellow; color: black; }")
        self.port_number = QtWidgets.QLineEdit(parent = self.recv_frame,placeholderText="Enter Port Number",maxLength=5)
        self.port_number.setValidator(QIntValidator())

            #recv_server page layouts
        self.recv_frame_main_layout = QtWidgets.QVBoxLayout(self.recv_frame)
        self.recv_frame_button_layout = QtWidgets.QHBoxLayout()
        self.recv_frame_button_layout.addWidget(self.recv_back_to_home_button)
        self.recv_frame_button_layout.addWidget(self.start_recving)
        self.recv_frame_main_layout.addWidget(self.port_number)
        self.recv_frame_main_layout.addLayout(self.recv_frame_button_layout)
        #--------------------------------------------------------------------------------------------#
        #SEND CLIENT PAGE
        self.send_frame_page= QtWidgets.QFrame(parent = self.stacked)
        self.recv_frame.setStyleSheet("QFrame{ background-color: red;}")
            #button and Line Edit
        self.send_back_to_home_button = QtWidgets.QPushButton(parent= self.send_frame_page,text= "Home Page")
        self.send_back_to_home_button.setStyleSheet("QPushButton{ background-color: yellow; color: black; }")
        self.send_back_to_home_button.clicked.connect(lambda : self.stacked.setCurrentIndex(0))
        self.send_file_button = QtWidgets.QPushButton(parent=self.send_frame_page, text="Send")
        self.send_file_button.clicked.connect(self.send_file_button_clicked)
        self.open_file_button = QtWidgets.QPushButton(parent = self.send_frame_page,text= "Open File")
        self.open_file_button.clicked.connect(self.open_file_button_clicked)
        self.port_number_send = QtWidgets.QLineEdit(parent = self.send_frame_page, placeholderText="Enter port number of reciving server",maxLength=5)
        self.port_number_send.setValidator(QIntValidator())
        self.ip_address_of_server = QtWidgets.QLineEdit(parent = self.send_frame_page, placeholderText="Enter IP Address of Recving server",maxLength=15)
        self.opend_file_name = QtWidgets.QLineEdit(parent = self.send_frame_page)
        self.opend_file_name.setClearButtonEnabled(True)
           #layouts
        self.send_frame_page_main_layout = QtWidgets.QVBoxLayout(self.send_frame_page)
        self.grid_layout = QtWidgets.QGridLayout(self.send_frame_page)
        self.grid_layout.addWidget(self.opend_file_name,0,0)
        self.grid_layout.addWidget(self.open_file_button,0,1)
        self.grid_layout.addWidget(self.ip_address_of_server,1,0)
        self.grid_layout.addWidget(self.port_number_send,1,1)
        self.grid_layout.addWidget(self.send_back_to_home_button,2,0)
        self.grid_layout.addWidget(self.send_file_button,2,1)
        self.send_frame_page_main_layout.addLayout(self.grid_layout)


        #Add pages to stacekd widgets
        self.stacked.addWidget(self.main_frame)
        self.stacked.addWidget(self.recv_frame)
        self.stacked.addWidget(self.send_frame_page)
    def recv_file_button_clicked(self):
        if int(self.port_number.text()) > 64000 or int(self.port_number.text())<0:
            port_warning_dialog = QtWidgets.QMessageBox.warning(self,"wrong Port Number","port number should be between 0 and 64000",QtWidgets.QMessageBox.Ok)
            return None
        else:
            recv_client = ReceivingClient(server_port=int(self.port_number.text()))
            recv_client.create_connection_socket()
            recv_bytes, file_type = recv_client.recv_file()
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save As","",f"{file_type}(*.{file_type});;All Files (*)")

            if file_path:
                recv_client.save_file(recv_bytes,file_type,file_path=file_path)

    def open_file_button_clicked(self):
        file_path,_ = QtWidgets.QFileDialog.getOpenFileName(self,"Open","")

        if file_path:
            self.opend_file_name.setText(file_path)
            return file_path


    def send_file_button_clicked(self):
        send_file = SendFileClient(server_port=int(self.port_number_send.text()),ip_address=self.ip_address_of_server.text())
        send_file.send_file(self.open_file_button_clicked())
        send_file.close_connection()















if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())






