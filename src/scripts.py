
import keyboard
from pynput import mouse
from PyQt6.QtWidgets import QMessageBox, QLineEdit
import subprocess

# tạo 1 hàm lắng nghe phím bấm sau đó trả về ký tự tương ứng
def listen_key():
    key = keyboard.read_event()
    if key.event_type == keyboard.KEY_DOWN:
        return key.name
    
    
class Scripts:
    def __init__(self, ui, dashboard):
        self.ui = ui
        self.dashboard = dashboard
        self.connect_button()
    
    
        
    # Tab Chrome
    def add_chrome(self):
        link = self.ui.lineEdit_19.text()
        code_python = '''# --------------------- ADD CHROME ---------------------
import webbrowser
webbrowser.open_new_tab('{}')
import time
time.sleep(1)
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
    def add_chrome_new_undetected_chromedriver(self):
        code_python = '''# --------------------- ADD CHROME NEW UNDETECTED CHROMEDRIVER ---------------------
from undetected_chromedriver import Chrome, ChromeOptions
options = ChromeOptions()
driver = Chrome(options=options)
import time
time.sleep(1)
# --------------------------------------------------------'''
        self.ui.textEdit_3.append(code_python)
        
    def add_resize_chrome(self):
        width = self.ui.lineEdit_95.text()
        height = self.ui.lineEdit_96.text()
        code_python = '''# --------------------- ADD RESIZE CHROME ---------------------
driver.set_window_size({}, {})
import time
time.sleep(1)
# --------------------------------------------------------'''.format(width, height)
        self.ui.textEdit_3.append(code_python)
    def add_maximize_chrome(self):
        code_python = '''# --------------------- ADD MAXIMIZE CHROME ---------------------
driver.maximize_window()
import time
time.sleep(1)
# --------------------------------------------------------'''
        self.ui.textEdit_3.append(code_python)
    def add_zoom_chrome(self):
        zoom = self.ui.lineEdit_98.text()
        code_python = '''# --------------------- ADD ZOOM CHROME ---------------------
driver.execute_script("document.body.style.zoom='{}%'")
import time
time.sleep(1)
# --------------------------------------------------------'''.format(zoom)
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
import time
time.sleep(1)
# --------------------------------------------------------'''.format(key)
        self.ui.textEdit_3.append(code_python)
    def add_text_keyboard(self):
        text = self.ui.lineEdit_72.text()
        code_python = f'''# --------------------- ADD TEXT KEYBOARD ---------------------
import pyautogui
import time
import random
for s in '{text}':
    pyautogui.typewrite(s, interval=random.randint(1,10)/50)
time.sleep(1)
# --------------------------------------------------------'''
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
import time
time.sleep(1)
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
            

    
        
        
    def add_mouse_move_random_in_boundary(self):
        x = self.ui.lineEdit_90.text()
        y = self.ui.lineEdit_91.text()
        width = self.ui.lineEdit_89.text()
        height = self.ui.lineEdit_88.text()
        code_python = '''# --------------------- ADD MOUSE MOVE RANDOM IN BOUNDARY ---------------------
import pyautogui
import random
import time
import math
def move_like_human(x_start, y_start, x_end, y_end, duration):
    steps = random.randint(1, 7)  # Giảm số bước để di chuyển nhanh hơn
    sleep_time = duration / steps
    for step in range(steps):
        t = step / (steps - 1)  # Đảm bảo t = 1 ở bước cuối cùng
        ease_t = (math.sin((t - 0.5) * math.pi) + 1) / 2  # Hiệu ứng di chuyển mượt
        x = x_start + (x_end - x_start) * ease_t
        y = y_start + (y_end - y_start) * ease_t
        
        pyautogui.moveTo(x, y)
        time.sleep(sleep_time)  # Thời gian nghỉ giữa mỗi bước
    pyautogui.moveTo(x_end, y_end)

x_start, y_start = pyautogui.position()
x_end = random.randint({}, {})
y_end = random.randint({}, {})
move_like_human(x_start, y_start, x_end, y_end, duration=0.02)
time.sleep(1)
# --------------------------------------------------------'''.format(int(x), int(x) + int(width), int(y), int(y) + int(height))
        self.ui.textEdit_3.append(code_python)
        
        
    def add_mouse_move(self):
        x = self.ui.lineEdit_85.text()
        y = self.ui.lineEdit_84.text()
        code_python = '''# --------------------- ADD MOUSE MOVE ---------------------
import pyautogui
import random
import time
import math
def move_like_human(x_start, y_start, x_end, y_end, duration):
    steps = random.randint(1, 7)  # Giảm số bước để di chuyển nhanh hơn
    sleep_time = duration / steps
    for step in range(steps):
        t = step / (steps - 1)  # Đảm bảo t = 1 ở bước cuối cùng
        ease_t = (math.sin((t - 0.5) * math.pi) + 1) / 2  # Hiệu ứng di chuyển mượt
        x = x_start + (x_end - x_start) * ease_t
        y = y_start + (y_end - y_start) * ease_t
        
        pyautogui.moveTo(x, y)
        time.sleep(sleep_time)  # Thời gian nghỉ giữa mỗi bước
    pyautogui.moveTo(x_end, y_end)
x_start, y_start = pyautogui.position()
x_end = {}
y_end = {}
move_like_human(x_start, y_start, x_end, y_end, duration=0.02)
time.sleep(1)
# --------------------------------------------------------'''.format(x, y)
        self.ui.textEdit_3.append(code_python)
    def add_mouse_right_click(self):
        code_python = '''# --------------------- ADD MOUSE RIGHT CLICK ---------------------
import pyautogui
pyautogui.rightClick()
import time
time.sleep(1)
# --------------------------------------------------------'''
        self.ui.textEdit_3.append(code_python)
    def add_mouse_left_click(self):
        code_python = '''# --------------------- ADD MOUSE LEFT CLICK ---------------------
import pyautogui
pyautogui.leftClick()
import time
time.sleep(1)
# --------------------------------------------------------'''
        self.ui.textEdit_3.append(code_python)
    def add_mouse_scroll(self):
        wheel = self.ui.lineEdit_86.text()
        # whell sẽ là số âm nếu muốn cuộn lên, dương nếu muốn cuộn xuống
        code_python = '''# --------------------- ADD MOUSE SCROLL ---------------------
import pyautogui
pyautogui.scroll({wheel})
import time
time.sleep(1)
# --------------------------------------------------------'''.format(wheel=wheel)
        self.ui.textEdit_3.append(code_python)
        
        
        
        
    def run_test(self):
        # lấy code từ textedit sau đó chạy
        code = self.ui.textEdit_3.toPlainText()
        # lưu code vào file
        with open('temp.py', 'w', encoding='utf-8') as file:
            file.write(code)
        # tạo 1 thread chạy exec code để không block UI
        import threading
        def run_code():
            subprocess.run(['python', 'temp.py'])
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
    def delete_all_step(self):
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
        self.ui.pushButton_86.clicked.connect(self.add_mouse_move_random_in_boundary)
        self.ui.pushButton_26.clicked.connect(self.add_chrome_new_undetected_chromedriver)
        self.ui.pushButton_95.clicked.connect(self.add_resize_chrome)
        self.ui.pushButton_94.clicked.connect(self.add_maximize_chrome)
        self.ui.pushButton_97.clicked.connect(self.add_zoom_chrome)
        
        self.ui.pushButton_22.clicked.connect(self.run_test)
        self.ui.pushButton_23.clicked.connect(self.delete_step)
        self.ui.pushButton_24.clicked.connect(self.save_file)
        self.ui.pushButton_25.clicked.connect(self.delete_all_step)