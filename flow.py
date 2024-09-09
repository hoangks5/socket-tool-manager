import sys
from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtWidgets import QApplication, QGroupBox, QMainWindow, QPushButton, QWidget
from flowapp import Ui_MainWindow
from PyQt6.QtWidgets import QMessageBox, QLineEdit

        


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection_button()
        

    def add_chrome(self):
        link = self.lineEdit_12.text()
        code_python = '''# --------------------- ADD CHROME ---------------------
import webbrowser
webbrowser.open_new_tab('{}')
# --------------------------------------------------------'''.format(link)
        # ghi thêm textedit ở đây
        self.textEdit.append(code_python)
    def add_sleep(self):
        time = self.lineEdit_7.text()
        time_random = self.lineEdit_8.text()
        code_python = '''# --------------------- ADD SLEEP ---------------------
import time
import random
time.sleep({time} - random.randint(-{time_random}, {time_random}))
# --------------------------------------------------------'''.format(time=time, time_random=time_random)
        # ghi thêm textedit ở đây
        self.textEdit.append(code_python)
        
    
        
        
    
    def connection_button(self):
        self.pushButton_19.clicked.connect(self.run_test)
        self.pushButton_18.clicked.connect(self.delete_step)
        self.pushButton_17.clicked.connect(self.save_file)
        
        
        self.pushButton_3.clicked.connect(self.add_chrome)
        self.pushButton_5.clicked.connect(self.add_sleep)
        
        
    def run_test(self):
        # lấy code từ textedit sau đó chạy
        code = self.textEdit.toPlainText()
        # tạo 1 thread chạy exec code để không block UI
        import threading
        def run_code():
            exec(code)
        threading.Thread(target=run_code).start()
    
    
    def delete_step(self):
        # xóa bước cuối cùng
        text = self.textEdit.toPlainText()
        import re


        # Sửa lại biểu thức chính quy để khớp với đoạn văn bản
        pattern = r'# ---------------------.*?# --------------------------------------------------------'
        matches = list(re.finditer(pattern, text, re.DOTALL))
        if matches:
            # xóa bước cuối cùng
            last_match = matches[-1]
            start, end = last_match.span()
            text = text[:start] + text[end:]
            self.textEdit.setPlainText(text)
        else:
            self.textEdit.setPlainText('')
            
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
                    file.write(self.textEdit.toPlainText())
                    
                    
            
            
        
        
        
        
        
        
        
    
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
