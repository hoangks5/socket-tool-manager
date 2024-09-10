from mainui_v2 import Ui_MainWindow
from login import Ui_MainWindow as Ui_Login
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QSizePolicy, QVBoxLayout
from PyQt6.QtCore import QRect, QPropertyAnimation, QEasingCurve, QAbstractAnimation, QTimer, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import QtCore
import sys
import time
from connect_socket import *
from src.dashboard import Dashboard
from src.load_clients_thread import LoadClientsThread
from src.script_keyboard import *
from pynput import mouse
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import pandas as pd
import pycountry
from PIL import Image
from io import BytesIO
import requests
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def convert_alpha_2_to_alpha_3(alpha_2_code):
    try:
        country = pycountry.countries.get(alpha_2=alpha_2_code)
        return country.alpha_3 if country else "Unknown country code"
    except LookupError:
        return "Unknown country code"

def convert_alpha_3_to_alpha_2(alpha_3_code):
    try:
        country = pycountry.countries.get(alpha_3=alpha_3_code)
        return country.alpha_2 if country else "Unknown country code"
    except LookupError:
        return "Unknown country code"

def fetch_flag_image(alpha_2_code):
    url = f"https://flagcdn.com/w320/{alpha_2_code.lower()}.png"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content)).convert("RGBA")
    else:
        return None

class DataFetcher(QThread):
    data_fetched = pyqtSignal(list)  # Signal to send data to the main thread

    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget

    def run(self):
        data_old = []
        while True:
            # Fetch data from table widget
            ip_locations = self.get_ip_locations_from_table()
            if ip_locations != data_old:
                data_old = ip_locations
                self.data_fetched.emit(ip_locations)
                time.sleep(1)  # Wait for 10 seconds before fetching data again
            else:
                time.sleep(1)

    def get_ip_locations_from_table(self):
        ip_locations = []
        try:
            for row in range(self.table_widget.rowCount()):
                ip = self.table_widget.item(row, 2).text()
                lat = self.table_widget.item(row, 3).text().split("|")[1].split(",")[0]
                lon = self.table_widget.item(row, 3).text().split("|")[1].split(",")[1]
                country = self.table_widget.item(row, 3).text().split("|")[0].split("-")[1].strip()
                ip_locations.append({'ip': ip, 'lat': float(lat), 'lon': float(lon), 'country': country})
            return ip_locations
        except Exception as e:
            return []
    
    
class MapCanvas(FigureCanvas):
    def __init__(self, parent=None, ip_locations=None):
        self.ip_locations = ip_locations
        print("IP Locations:", self.ip_locations)
        fig, self.ax = plt.subplots(figsize=(10, 7), tight_layout=True)  # Adjusted size for better view
        super().__init__(fig)
        self.setParent(parent)  # Set parent to ensure proper embedding
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Ensure the canvas expands
        self.draw_map()
       
    def update_data(self, ip_locations):
        # xoá hết các label và flag cũ
        for artist in self.ax.artists:
            artist.remove()
        for line in self.ax.lines:
            line.remove()
        for text in self.ax.texts:
            text.remove()
        self.ip_locations = ip_locations
        self.draw_map()
        
    def draw_map(self):
        # Load world map shapefile
        world = gpd.read_file('./map/ne_110m_admin_0_countries.shp')
        if self.ip_locations == []:
            return
        
        ip_locations = [dict(ip_location, country=convert_alpha_2_to_alpha_3(ip_location['country'])) for ip_location in self.ip_locations]
        # Convert to DataFrame
        ip_df = pd.DataFrame(ip_locations)

        # Count IPs per country
        ip_counts = ip_df['country'].value_counts()

        # Merge IP counts with world map data
        world = world.merge(ip_counts, how='left', left_on='ADM0_A3', right_index=True)
        world['count'].fillna(0, inplace=True)

        # Plot the world map with IP counts
        norm = Normalize(vmin=0, vmax=ip_counts.max())
        world.plot(ax=self.ax, column='count', cmap='OrRd', linewidth=0.8, edgecolor='0.8', norm=norm, legend=False)

        # Hide x and y axis labels
        self.ax.set_xlabel('')
        self.ax.set_ylabel('')

        # Hide the grid
        self.ax.grid(False)

        # Remove ticks
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Remove borders and frame
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)

        # Add labels for IP counts and flags
        for idx, row in world.iterrows():
            if row['count'] > 0:  # Only label countries with IPs
                x, y = row.geometry.centroid.x, row.geometry.centroid.y
                self.ax.annotate(
                    f"{int(row['count'])}",
                    xy=(x, y),
                    xytext=(3, 3),  # Offset text
                    textcoords="offset points",
                    fontsize=8,
                    color='black',
                    weight='bold'
                )

                # Fetch and place flag image
                flag_image = fetch_flag_image(convert_alpha_3_to_alpha_2(row['ADM0_A3']))
                if flag_image:
                    # Convert the image to an appropriate format
                    imagebox = OffsetImage(flag_image, zoom=0.1)  # Adjust zoom for flag size
                    ab = AnnotationBbox(imagebox, (x, y),
                                        frameon=False,
                                        pad=0.1,
                                        xycoords='data',
                                        boxcoords="offset points",
                                        box_alignment=(0.5, 0.5))
                    self.ax.add_artist(ab)

        # Remove the title
        self.ax.set_title('')

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
        self.setup_marquee()
        self.ui.textEdit.verticalScrollBar().setVisible(False)
        self.ui.textEdit.horizontalScrollBar().setVisible(False)
        
        # tắt scroll stackwidget
        self.ui.stackedWidget.setContentsMargins(0, 0, 0, 0)
        self.ui.stackedWidget.setFrameStyle(0)
        
        
        self.dashboard = Dashboard(self.ui)
        
    
        
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
    
        
        
    # Tab Chrome
    def add_chrome(self):
        link = self.ui.lineEdit_19.text()
        code_python = '''# --------------------- ADD CHROME ---------------------
import webbrowser
webbrowser.open_new_tab('{}')
# --------------------------------------------------------'''.format(link)
        # ghi thêm textedit ở đây
        self.ui.textEdit_3.append(code_python)
    def add_sleep(self):
        time = self.ui.lineEdit_20.text()
        time_random = self.ui.lineEdit_21.text()
        code_python = '''# --------------------- ADD SLEEP ---------------------
import time
import random
time.sleep({time} - random.randint(-{time_random}, {time_random}))
# --------------------------------------------------------'''.format(time=time, time_random=time_random)
        # ghi thêm textedit ở đây
        self.ui.textEdit_3.append(code_python)
        
        
    # Tab Keyboard
    def get_key(self):
        key = listen_key()
        self.ui.lineEdit_83.setText(key)
    def add_key(self):
        key = self.ui.lineEdit_83.text()
        code_python = '''# --------------------- ADD KEY ---------------------
import pyautogui
pyautogui.press('{}')
# --------------------------------------------------------'''.format(key)
        self.ui.textEdit_3.append(code_python)
    def add_text_keyboard(self):
        text = self.ui.lineEdit_72.text()
        delay = self.ui.lineEdit_82.text()
        code_python = '''# --------------------- ADD TEXT KEYBOARD ---------------------
import pyautogui
import time
pyautogui.typewrite('{}', interval={})
# --------------------------------------------------------'''.format(text, delay)
        self.ui.textEdit_3.append(code_python)
    def get_key_multi(self):
        key = listen_key()
        # lấy key hiện tại trong lineedit
        key_current = self.ui.lineEdit_87.text().split(" ")
        key_current = [key for key in key_current if key != ""]
        key_current.append(key)
        self.ui.lineEdit_87.setText(" ".join(key_current))
    def add_key_multi(self):
        key = self.ui.lineEdit_87.text()
        keys = key.split(" ")
        keys_formatted = "', '".join(keys)
        code_python = '''# --------------------- ADD KEY MULTI ---------------------
import pyautogui
pyautogui.hotkey('{}')
# --------------------------------------------------------'''.format(keys_formatted)
        self.ui.textEdit_3.append(code_python)
        
        
    # Tab Mouse
    def on_click(self, x, y, button, pressed):
        if pressed:
            print(f"Chuột được nhấn tại vị trí: ({x}, {y})")
            self.ui.lineEdit_85.setText(str(x))
            self.ui.lineEdit_84.setText(str(y))
            # Sau khi lấy tọa độ, bạn có thể ngừng lắng nghe
            return False

    def get_mouse_position(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
    def add_mouse_move(self):
        x = self.ui.lineEdit_85.text()
        y = self.ui.lineEdit_84.text()
        code_python = '''# --------------------- ADD MOUSE MOVE ---------------------
import pyautogui
pyautogui.moveTo({}, {})
# --------------------------------------------------------'''.format(x, y)
        self.ui.textEdit_3.append(code_python)
    def add_mouse_right_click(self):
        code_python = '''# --------------------- ADD MOUSE RIGHT CLICK ---------------------
import pyautogui
pyautogui.rightClick()
# --------------------------------------------------------'''
        self.ui.textEdit_3.append(code_python)
    def add_mouse_left_click(self):
        code_python = '''# --------------------- ADD MOUSE LEFT CLICK ---------------------
import pyautogui
pyautogui.leftClick()
# --------------------------------------------------------'''
        self.ui.textEdit_3.append(code_python)
    def add_mouse_scroll(self):
        wheel = self.ui.lineEdit_86.text()
        # whell sẽ là số âm nếu muốn cuộn lên, dương nếu muốn cuộn xuống
        code_python = '''# --------------------- ADD MOUSE SCROLL ---------------------
import pyautogui
pyautogui.scroll({wheel})
# --------------------------------------------------------'''.format(wheel=wheel)
        self.ui.textEdit_3.append(code_python)
        
        
        
        
    def run_test(self):
        # lấy code từ textedit sau đó chạy
        code = self.ui.textEdit_3.toPlainText()
        # tạo 1 thread chạy exec code để không block UI
        import threading
        def run_code():
            exec(code)
        threading.Thread(target=run_code).start()
    
    
    def delete_step(self):
        # xóa bước cuối cùng
        text = self.ui.textEdit_3.toPlainText()
        import re


        # Sửa lại biểu thức chính quy để khớp với đoạn văn bản
        pattern = r'# ---------------------.*?# --------------------------------------------------------'
        matches = list(re.finditer(pattern, text, re.DOTALL))
        if matches:
            # xóa bước cuối cùng
            last_match = matches[-1]
            start, end = last_match.span()
            text = text[:start] + text[end:]
            self.ui.textEdit_3.setPlainText(text)
        else:
            self.ui.textEdit_3.setPlainText('')
            
    def save_file(self):
        # tạo ra 1 qmessagebox để lưu file với 1 lineedit ở bên trên
        
        noti = QMessageBox()
        noti.setWindowTitle("Save file")
        noti.setText("Vui lòng nhập tên file để lưu")
        noti.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        noti.setDefaultButton(QMessageBox.StandardButton.Ok)
        lineedit = QLineEdit()
        lineedit.setPlaceholderText("Enter file name")
        noti.layout().addWidget(lineedit)
        
        ret = noti.exec()
        
        if ret == QMessageBox.StandardButton.Ok:
            file_name = lineedit.text()
            if file_name:
                with open(f'./scripts/{file_name}.py', 'w') as file:
                    file.write(self.ui.textEdit_3.toPlainText())
        
        self.dashboard.add_item_combobox(self.ui.comboBox)
        
        
        
        
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
        self.ui.pushButton_14.clicked.connect(lambda : self.dashboard.run_script(self.ip_socket, self.port_socket))
        #appflow
        self.ui.pushButton_27.clicked.connect(self.add_chrome)
        self.ui.pushButton_28.clicked.connect(self.add_sleep)
        self.ui.pushButton_77.clicked.connect(self.get_key)
        self.ui.pushButton_78.clicked.connect(self.add_key)
        self.ui.pushButton_69.clicked.connect(self.add_text_keyboard)
        self.ui.pushButton_83.clicked.connect(self.get_key_multi)
        self.ui.pushButton_84.clicked.connect(self.add_key_multi)
        self.ui.pushButton_79.clicked.connect(self.get_mouse_position)
        self.ui.pushButton_80.clicked.connect(self.add_mouse_move)
        self.ui.pushButton_81.clicked.connect(self.add_mouse_left_click)
        self.ui.pushButton_61.clicked.connect(self.add_mouse_right_click)
        self.ui.pushButton_82.clicked.connect(self.add_mouse_scroll)
        
        
        
        self.ui.pushButton_22.clicked.connect(self.run_test)
        self.ui.pushButton_23.clicked.connect(self.delete_step)
        self.ui.pushButton_24.clicked.connect(self.save_file)
        
        

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
        
        
        