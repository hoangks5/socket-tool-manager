from mainui_v2 import Ui_MainWindow
from login import Ui_MainWindow as Ui_Login
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QVBoxLayout
from PyQt6.QtCore import QTimer
import sys
from connect_socket import *
from src.dashboard import Dashboard
from src.load_clients_thread import LoadClientsThread
from src.scripts import Scripts
import sys
from src.mapcanvas import MapCanvas, DataFetcher
from src.get_boundary_screen import ScreenCapture
from src.taskbar import TaskBar

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
        
 
    
class MainWindow(QMainWindow):
    def __init__(self, ip_socket, port_socket):
        super().__init__()
        self.ip_socket = ip_socket
        self.port_socket = port_socket
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.widget_2.hide()
      
        
        
        self.taskbar = TaskBar(self.ui)
        self.dashboard = Dashboard(self.ui)
        self.scipts = Scripts(self.ui, self.dashboard)
        
        self.map_canvas = MapCanvas(self.ui.widget_8, self.get_ip_locations_from_table())
        
        layout = QVBoxLayout(self.ui.widget_8)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.map_canvas)
        self.ui.widget_8.setLayout(layout)
        
        # Create and start the data fetcher thread
        self.data_fetcher = DataFetcher(self.ui.tableWidget)
        self.data_fetcher.data_fetched.connect(self.update_map_canvas)
        self.data_fetcher.start()
        
        self.load_clients_thread = LoadClientsThread(self.ip_socket, self.port_socket)
        self.load_clients_thread.clients.connect(self.dashboard.update_clients)
        self.load_clients_thread.start()
    
    def update_map_canvas(self, ip_locations):
        self.map_canvas.update_data(ip_locations)
        
    def get_ip_locations_from_table(self):
        ip_locations = []
        for row in range(self.ui.tableWidget.rowCount()):
            ip = self.ui.tableWidget.item(row, 2).text()
            lat = self.ui.tableWidget.item(row, 3).text().split("|")[1].split(",")[0]
            lon = self.ui.tableWidget.item(row, 3).text().split("|")[1].split(",")[1]
            country = self.ui.tableWidget.item(row, 3).text().split("|")[0].split("-")[1].strip()
            ip_locations.append({'ip': ip, 'lat': float(lat), 'lon': float(lon), 'country': country})
        return ip_locations
    
    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()
        # disconnect thread
        self.load_clients_thread.terminate()
        self.data_fetcher.terminate()

    def get_mouse_boundary(self):
        window = ScreenCapture(self.ui)
        window.setParent(self)
        window.showFullScreen()
        
        
    def connect_button(self):
        self.ui.pushButton_10.clicked.connect(self.logout)
        self.ui.pushButton_11.clicked.connect(lambda: self.dashboard.push_select_all(self.ui.tableWidget))
        self.ui.pushButton_12.clicked.connect(self.dashboard.setup_script)
        self.ui.pushButton_14.clicked.connect(lambda : self.dashboard.run_script(self.ip_socket, self.port_socket))
        #appflow
        self.ui.pushButton_85.clicked.connect(self.get_mouse_boundary)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
        
        
        