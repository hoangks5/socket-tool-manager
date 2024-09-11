from PyQt6.QtCore import QTimer, QObject

class TaskBar(QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.connect_button()
        self.setup_marquee()
        self.ui.textEdit.verticalScrollBar().setVisible(False)
        self.ui.textEdit.horizontalScrollBar().setVisible(False)
        
        # tắt scroll stackwidget
        self.ui.stackedWidget.setContentsMargins(0, 0, 0, 0)
        self.ui.stackedWidget.setFrameStyle(0)
        

        
        
    def connect_button(self):
        self.ui.pushButton.clicked.connect(self.switch_to_dashboard)
        self.ui.pushButton_5.clicked.connect(self.switch_to_dashboard)
        self.ui.pushButton_2.clicked.connect(self.switch_to_system)
        self.ui.pushButton_6.clicked.connect(self.switch_to_system)
        self.ui.pushButton_3.clicked.connect(self.switch_to_monitor)
        self.ui.pushButton_7.clicked.connect(self.switch_to_monitor)
        self.ui.pushButton_4.clicked.connect(self.switch_to_setting)
        self.ui.pushButton_8.clicked.connect(self.switch_to_setting)
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