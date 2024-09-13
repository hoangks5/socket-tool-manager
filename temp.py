from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QGroupBox, QWidget
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import QEvent, QPoint
from PyQt6.QtCore import Qt

class CustomTooltip(QWidget):
    def __init__(self, gif_path):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | 
                            Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.ToolTip)
        
        # Tạo QLabel để hiển thị GIF
        self.label = QLabel(self)
        movie = QMovie(gif_path)
        self.label.setMovie(movie)
        movie.start()

    def show_tooltip(self, pos):
        """Hiển thị tooltip tại vị trí chuột"""
        self.move(pos)
        self.show()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Tạo GroupBox
        self.groupbox = QGroupBox("Hover over me")
        layout.addWidget(self.groupbox)

        # Tạo QLabel mô phỏng tooltip để hiển thị GIF
        self.tooltip = CustomTooltip("test.gif")

        # Đăng ký sự kiện di chuột cho groupbox
        self.groupbox.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.groupbox:
            if event.type() == QEvent.Type.Enter:
                # Hiển thị tooltip khi chuột di vào
                self.tooltip.show_tooltip(self.mapToGlobal(QPoint(self.groupbox.width() // 2, self.groupbox.height())))
            elif event.type() == QEvent.Type.Leave:
                # Ẩn tooltip khi chuột ra khỏi widget
                self.tooltip.hide()
        return super().eventFilter(obj, event)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
