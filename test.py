import sys
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
import requests
from io import BytesIO

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    return data['ip']

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

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IP Table with Flags")
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['IP Address', 'Country', 'Flag'])

        # Get public IP
        public_ip = get_public_ip()
        country_code = 'US'  # Ví dụ mã quốc gia cho IP công cộng

        # Example data
        data = [
            (public_ip, country_code),
            ('93.184.216.34', 'GB'),
            ('2001:db8::ff00:42:8329', 'FR'),
        ]

        self.table.setRowCount(len(data))
        for row, (ip, country_code) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(ip))
            self.table.setItem(row, 1, QTableWidgetItem(country_code))
            
            # Download flag image
            flag_url = get_flag_url(country_code)
            flag_image = download_image(flag_url)
            
            # Create QIcon from QPixmap and set it to QTableWidgetItem
            flag_icon = QIcon(flag_image)
            flag_item = QTableWidgetItem()
            flag_item.setIcon(flag_icon)
            self.table.setItem(row, 2, flag_item)
        
        layout.addWidget(self.table)
        self.setLayout(layout)

app = QApplication(sys.argv)
window = TableWidget()
window.show()
sys.exit(app.exec())
