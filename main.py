from mainui_v2 import Ui_MainWindow
from login import Ui_MainWindow as Ui_Login
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtCore import QRect, QPropertyAnimation, QEasingCurve, QAbstractAnimation, QTimer, Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import QtCore
import sys
import requests
import json
import time
import os
import datetime
import random
from connect_socket import *


socket_string = '3.18.29.6:12345'


def get_flag_url(country_code):
    response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}')
    data = response.json()
    flag_url = data[0]['flags']['png']
    return flag_url

def download_image(url):
    response = requests.get(url)
    image = QPixmap()
    image.loadFromData(response.content)
    return image

def get_script_name():
    return ['Mở trình duyệt', 'Tắt máy', 'Mở ứng dụng', 'Tải file', 'Cài đặt ứng dụng']
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
        self.resize_table()
        # tắt scroll stackwidget
        self.ui.stackedWidget.setContentsMargins(0, 0, 0, 0)
        self.ui.stackedWidget.setFrameStyle(0)
        self.add_item_combobox(self.ui.comboBox)
        
        
        self.load_clients_thread = LoadClientsThread(self.ip_socket, self.port_socket)
        self.load_clients_thread.clients.connect(self.update_clients)
        self.load_clients_thread.start()
        
        
        #self.setup_log_generation()
        
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
            
    def get_row_selected(self):
        selected_rows = []
        for i in range(self.ui.tableWidget.rowCount()):
            checkbox = self.ui.tableWidget.cellWidget(i, 0).layout().itemAt(0).widget()
            if checkbox.isChecked():
                selected_rows.append(i)
        return selected_rows
    
    def setup_script(self):
        # lấy script từ combobox
        script_name_now = self.ui.comboBox.currentText()
        # lấy row được chọn
        selected_rows = self.get_row_selected()
        for row in selected_rows:
            # đổi combobox thành script đã chọn
            self.combobox = QComboBox(parent=self.ui.widget_4)
            self.combobox.setStyleSheet("QComboBox{\n"
"background-color: rgb(85, 255, 127);\n"
"border-radius: 5px;\n"
"border: 2px solid #23074d;\n"
"height:40px;\n"
"width: 105px;\n"
"}\n"
"")
            self.add_item_combobox(self.combobox)
            self.combobox.setCurrentText(script_name_now)
            self.ui.tableWidget.setCellWidget(row, 4, self.combobox)
            # thêm log
            self.add_log_cmd(f"📜 [{self.get_current_time()}] [{self.ui.tableWidget.item(row, 2).text()}] Script {script_name_now} has been added to client {self.ui.tableWidget.item(row, 1).text()}")
           
            
    def add_log_cmd(self, message):
        self.ui.textEdit.append(message)  # Append the message to QTextEdit
    def resize_table(self):
        # thiết lập kích thước cột cho tableWidget reponsive với kích thuớc cửa sổ tính theo %
        table_width = self.ui.tableWidget.width()
        self.ui.tableWidget.setColumnWidth(0, int(table_width * 0.01))
        self.ui.tableWidget.setColumnWidth(1, int(table_width * 0.3))
        self.ui.tableWidget.setColumnWidth(2, int(table_width * 0.3))
        self.ui.tableWidget.setColumnWidth(3, int(table_width * 0.3))
        self.ui.tableWidget.setColumnWidth(4, int(table_width * 0.2))
        self.ui.tableWidget.setColumnWidth(5, int(table_width * 0.25))
        self.ui.tableWidget.setColumnWidth(6, int(table_width * 0.15))
        self.ui.tableWidget.setColumnWidth(7, int(table_width * 0.15))
        
    
        
    
    def add_item_combobox(self, combobox):
        list_script = get_script_name()
        combobox.addItems(list_script)
    
    def update_clients(self, clients):
        print(clients)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setRowCount(len(clients))
        for i, client in enumerate(clients):
            # cột 0 là ô checkbox
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem())
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(client['hostname']))
            ip = QTableWidgetItem(client['ip'])
            ip.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(i, 2, ip)
            country_code = client['country']
            flag_url = get_flag_url(country_code)
            flag_image = download_image(flag_url)
            # Create QIcon from QPixmap and set it to QTableWidgetItem
            flag_icon = QIcon(flag_image)
            flag_item = QTableWidgetItem(f"{client['city']} - {client['country']}")
            #flag_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            flag_item.setIcon(flag_icon)
            self.ui.tableWidget.setItem(i, 3, flag_item)
            
            # tạo status có icon online trong text
            status = QTableWidgetItem("🟢 Online")
            status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(i, 5, status)
            
            view_screen = QPushButton("🖥️")
            view_screen.setStyleSheet("QPushButton{\n"
"border-radius:5px;\n"
"border: 2px solid #23074d;\n"
"background-color: #cc5333;\n"
"color:#FFB6C1;\n"
"height: 40px;\n"
"width: 120px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 2px solid #009fff ;\n"
"    background-color:#23074d;\n"
"            }\n"
"QPushButton:pressed {\n"
"                background-color: #5650de; /* Màu nền khi nhấn */\n"
"            }\n"
"\n"
"QComboBox{\n"
"background-color: rgb(85, 255, 127);\n"
"border-radius: 5px;\n"
"border: 2px solid #23074d;\n"
"height:40px;\n"
"width: 105px;\n"
"}\n"
"")
            view_screen.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)       
            self.ui.tableWidget.setCellWidget(i, 6, view_screen)

            button_setting = QPushButton("⚙️")
            button_setting.setStyleSheet("QPushButton{\n"
"border-radius:5px;\n"
"border: 2px solid #23074d;\n"
"background-color: #cc5333;\n"
"color:#FFB6C1;\n"
"height: 40px;\n"
"width: 120px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 2px solid #009fff ;\n"
"    background-color:#23074d;\n"
"            }\n"
"QPushButton:pressed {\n"
"                background-color: #5650de; /* Màu nền khi nhấn */\n"
"            }\n"
"\n"
"QComboBox{\n"
"background-color: rgb(85, 255, 127);\n"
"border-radius: 5px;\n"
"border: 2px solid #23074d;\n"
"height:40px;\n"
"width: 105px;\n"
"}\n"
"")
            button_setting.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            self.ui.tableWidget.setCellWidget(i, 7, button_setting)
            
            # nhúng combobox vào tablewidget
            # copy self.ui.comboBox 
            self.combobox = QComboBox(parent=self.ui.widget_4)
            self.combobox.setStyleSheet("QComboBox{\n"
"background-color: rgb(85, 255, 127);\n"
"border-radius: 5px;\n"
"border: 2px solid #23074d;\n"
"height:40px;\n"
"width: 105px;\n"
"}\n"
"")
            self.add_item_combobox(self.combobox)
            self.ui.tableWidget.setCellWidget(i, 4, self.combobox)
            
        
            
        self.load_select()
    
    
    
    
    def load_select(self):
        for i in range(self.ui.tableWidget.rowCount()):
            checkbox = QCheckBox()
            checkbox.setChecked(False)  # Initially unchecked
            checkbox_layout = QWidget()
            checkbox_layout.setLayout(QHBoxLayout())
            checkbox_layout.layout().addWidget(checkbox)
            checkbox_layout.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.layout().setContentsMargins(0, 0, 0, 0)
            self.ui.tableWidget.setCellWidget(i, 0, checkbox_layout)
            
    def push_select_all(self, tableWidget):
        # kiểm tra xem tất cả row đã được chọn chưa
        is_all_checked = True
        for i in range(tableWidget.rowCount()):
            checkbox = tableWidget.cellWidget(i, 0).layout().itemAt(0).widget()
            if not checkbox.isChecked():
                is_all_checked = False
        # nếu tất cả row đã được chọn thì bỏ chọn tất cả
        if is_all_checked:
            for i in range(tableWidget.rowCount()):
                checkbox = tableWidget.cellWidget(i, 0).layout().itemAt(0).widget()
                checkbox.setChecked(False)
        else:
            for i in range(tableWidget.rowCount()):
                checkbox = tableWidget.cellWidget(i, 0).layout().itemAt(0).widget()
                checkbox.setChecked(True)
    
    
    
    # hàm test log
    def setup_log_generation(self):
        self.log_timer = QTimer(self)
        self.log_timer.timeout.connect(self.generate_log)
        self.log_timer.start(300)  # 1 second interval for generating logs
    def get_current_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def generate_log(self):
        icons = {
        "loading": "🔄",
        "request": "🌐",
        "database": "💾",
        "encrypted": "🔒",
        "integrity": "✅",
        "update": "⬆️",
        "backup": "🗃️",
        "auth": "🔑",
        "progress": "📈",
        "error": "❌",
        "success": "🎉"
    }

        logs = [
            f"{icons['loading']} [{self.get_current_time()}] Downloading data from server... Complete.",
            f"{icons['progress']} [{self.get_current_time()}] Processing request from: 192.168.1.1...",
            f"{icons['database']} [{self.get_current_time()}] Connecting to the database...",
            f"{icons['encrypted']} [{self.get_current_time()}] Data has been encrypted and stored.",
            f"{icons['integrity']} [{self.get_current_time()}] Verifying data integrity...",
            f"{icons['success']} [{self.get_current_time()}] System update completed successfully.",
            f"{icons['update']} [{self.get_current_time()}] Updating software version...",
            f"{icons['backup']} [{self.get_current_time()}] Creating data backup...",
            f"{icons['auth']} [{self.get_current_time()}] Authenticating user information...",
            f"{icons['error']} [{self.get_current_time()}] Error encountered: Connection timeout.",
            f"{icons['success']} [{self.get_current_time()}] Backup process completed successfully.",
            f"{icons['progress']} [{self.get_current_time()}] System health check: 85% complete.",
            f"{icons['update']} [{self.get_current_time()}] Applying configuration changes..."
        ]
        random_log = random.choice(logs)
        self.add_log_cmd(f"{random_log}")
        
        
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
        
        self.ui.pushButton_11.clicked.connect(lambda: self.push_select_all(self.ui.tableWidget))
        self.ui.pushButton_12.clicked.connect(self.setup_script)
        
        
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
        
        
        