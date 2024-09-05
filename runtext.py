import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget

class Marquee(QWidget):
    def __init__(self):
        super().__init__()
        
        # Tạo QLineEdit
        self.line_edit = QLineEdit(self)
        self.line_edit.setReadOnly(True)
        self.text = "                                                                                                                                                                                                                    Đây là dòng chữ chạy từ trái sang phải."
        self.displayed_text = ""
        
        # Cấu hình QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(200)  # Thời gian giữa mỗi bước (200 ms)
        
        # Cấu hình giao diện
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit)
        self.setLayout(layout)
        
        self.index = 0
        self.paused = False

    def scroll_text(self):
        if not self.paused:
            # Cập nhật chuỗi văn bản hiển thị
            self.displayed_text = self.text[self.index:] + self.text[:self.index]
            self.line_edit.setText(self.displayed_text)

            # Tăng chỉ số để dịch chuyển chuỗi
            self.index = (self.index + 1) % len(self.text)

            # Kiểm tra nếu chuỗi đã quay lại vị trí ban đầu
            if self.index == 0:
                self.paused = True
                self.timer.start(1)  # Tạm dừng 2 giây
        else:
            self.paused = False
            self.timer.start(200)  # Tiếp tục cuộn sau khi hết tạm dừng

# Chạy ứng dụng
app = QApplication(sys.argv)
window = Marquee()
window.setWindowTitle("Dòng chữ chạy từ trái qua phải")
window.resize(400, 100)
window.show()
sys.exit(app.exec())
