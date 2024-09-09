from mainui_v2 import Ui_MainWindow
from login import Ui_MainWindow as Ui_Login
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtCore import QRect, QPropertyAnimation, QEasingCurve, QAbstractAnimation, QTimer, Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import QtCore
import sys
import time
from connect_socket import *
from src.dashboard import Dashboard



class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
    
    def connect_button(self):
        self.ui.pushButton.clicked.connect(self.login)
        
    def check_socket(self):
        socket = self.ui.lineEdit.text()
        if socket == "":
            return False
        else:
            socket = socket.split(":")
            if len(socket) == 2:
                ip, port = socket
                status = check_server(ip, int(port))
                return status
            else:
                QMessageBox.critical(None, "Error", "Địa chỉ socket không hợp lệ")
                return False
        
    def login(self):
        if self.check_socket() == True:
            self.ip_socket = self.ui.lineEdit.text().split(":")[0]
            self.port_socket = self.ui.lineEdit.text().split(":")[1]
            
            self.main_window = MainWindow(self.ip_socket, self.port_socket)
            self.main_window.show()
            self.main_window.connect_button()
            self.close()
        else:
            QMessageBox.critical(None, "Error", "Không thể kết nối đến server")
            
    def show(self):
        super().show()
        self.connect_button()
        
        
class LoadClientsThread(QtCore.QThread):
    clients = QtCore.pyqtSignal(list)
    old_clients = []
    def __init__(self, ip_socket, port_socket):
        self.ip_socket = ip_socket
        self.port_socket = port_socket
        super().__init__()
    def run(self):
        self.main()
        
    def main(self):
        while True:
            clients = get_clients(self.ip_socket, int(self.port_socket))
            if clients != self.old_clients:
                self.old_clients = clients
                self.clients.emit(clients)
                time.sleep(2)
            else:
                time.sleep(2)
        

    
    
    
                                      
    
    
class MainWindow(QMainWindow):
    def __init__(self, ip_socket, port_socket):
        super().__init__()
        self.ip_socket = ip_socket
        self.port_socket = port_socket
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.widget_2.hide()
        self.setup_marquee()
        self.ui.textEdit.verticalScrollBar().setVisible(False)
        self.ui.textEdit.horizontalScrollBar().setVisible(False)
        
        # tắt scroll stackwidget
        self.ui.stackedWidget.setContentsMargins(0, 0, 0, 0)
        self.ui.stackedWidget.setFrameStyle(0)
        
        
        self.dashboard = Dashboard(self.ui)
        
        
        self.load_clients_thread = LoadClientsThread(self.ip_socket, self.port_socket)
        self.load_clients_thread.clients.connect(self.dashboard.update_clients)
        self.load_clients_thread.start()
        
        
        #self.setup_log_generation()
    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()
        
        # disconnect thread
        self.load_clients_thread.terminate()
        
        
    def setup_marquee(self):
        self.text = " "*250 + " Khuyến mãi giảm giá 50% cho tất cả các sản phẩm. Hãy nhanh tay đặt hàng ngay hôm nay! "
        self.index = 0
        self.paused = False
        # Tạo QTimer để cuộn chữ
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(50)  # Thời gian giữa mỗi bước (200 ms)
    def scroll_text(self):
        if not self.paused:
            displayed_text = self.text[self.index:] + self.text[:self.index]
            self.ui.lineEdit.setText(displayed_text)
            # Tăng chỉ số để dịch chuyển chuỗi
            self.index = (self.index + 1) % len(self.text)
            
    
        
        
    def switch_to_dashboard(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def switch_to_system(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def switch_to_monitor(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def switch_to_setting(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    
        
    def connect_button(self):
        self.ui.pushButton.clicked.connect(self.switch_to_dashboard)
        self.ui.pushButton_5.clicked.connect(self.switch_to_dashboard)
        self.ui.pushButton_2.clicked.connect(self.switch_to_system)
        self.ui.pushButton_6.clicked.connect(self.switch_to_system)
        self.ui.pushButton_3.clicked.connect(self.switch_to_monitor)
        self.ui.pushButton_7.clicked.connect(self.switch_to_monitor)
        self.ui.pushButton_4.clicked.connect(self.switch_to_setting)
        self.ui.pushButton_8.clicked.connect(self.switch_to_setting)
        
        self.ui.pushButton_10.clicked.connect(self.logout)
        
        self.ui.pushButton_11.clicked.connect(lambda: self.dashboard.push_select_all(self.ui.tableWidget))
        self.ui.pushButton_12.clicked.connect(self.dashboard.setup_script)
        
        
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
        
        
        