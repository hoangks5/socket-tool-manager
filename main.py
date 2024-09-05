from mainui_v2 import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
    
        
        self.load_clients()
        
        
        
        self.setup_log_generation()
        
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
    def add_log_cmd(self, message):
        self.ui.textEdit.append(message)  # Append the message to QTextEdit
    def resize_table(self):
        # thiết lập kích thước cột cho tableWidget reponsive với kích thuớc cửa sổ tính theo %
        table_width = self.ui.tableWidget.width()
        self.ui.tableWidget.setColumnWidth(0, int(table_width * 0.01))
        self.ui.tableWidget.setColumnWidth(1, int(table_width * 0.3))
        self.ui.tableWidget.setColumnWidth(2, int(table_width * 0.2))
        self.ui.tableWidget.setColumnWidth(3, int(table_width * 0.3))
        self.ui.tableWidget.setColumnWidth(4, int(table_width * 0.3))
        self.ui.tableWidget.setColumnWidth(5, int(table_width * 0.2))
        self.ui.tableWidget.setColumnWidth(7, int(table_width * 0.2))
        
    def load_clients(self):
        clients = get_clients(client_socket)
        print(clients)
        
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
            
            view_screen = QTableWidgetItem("🖥️")
            view_screen.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(i, 6, view_screen)
            
            setting = QTableWidgetItem("⚙️")
            setting.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(i, 7, setting)
            
            
            
        
            
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
        
        
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.connect_button()
    sys.exit(app.exec())
        
        
        