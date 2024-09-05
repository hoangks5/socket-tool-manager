from mainui_v2 import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6.QtCore import QRect, QPropertyAnimation, QEasingCurve, QAbstractAnimation, QTimer
from PyQt6.QtWidgets import QPushButton
import sys
import requests
import json
import time
import os
import datetime
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.widget_2.hide()
        self.setup_marquee()
        self.ui.textEdit.verticalScrollBar().setVisible(False)
        self.ui.textEdit.horizontalScrollBar().setVisible(False)
        
        
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
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()
    
    
    
    
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
        
        
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.connect_button()
    sys.exit(app.exec())
        
        
        