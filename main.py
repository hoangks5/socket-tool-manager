from mainui_v2 import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6.QtCore import QRect, QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PyQt6.QtWidgets import QPushButton
import sys
import requests
import json
import time
import os
from datetime import datetime
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.widget_2.hide()
        
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
        
        
        