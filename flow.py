import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QFrame, QPushButton, QVBoxLayout, QWidget
import math

class FlowChartLabel(QLabel):
    def __init__(self, text, parent=None, flowchart_area=None):
        super().__init__(text, parent)
        self.setFrameStyle(QLabel.Shape.Box)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: lightblue;")
        self.setFixedSize(100, 50)
        self.dragging = False
        self.flowchart_area = flowchart_area  # Reference to the flowchart area

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            # Di chuyển nhãn
            self.move(self.mapToParent(event.pos() - self.drag_start_position))
            # Cập nhật lại kết nối khi nhãn di chuyển
            if self.flowchart_area:
                self.flowchart_area.update_connections()

    def mouseReleaseEvent(self, event):
        self.dragging = False


class FlowChartArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.labels = []
        self.connections = []  # (start_label, end_label)
        self.setStyleSheet("background-color: white;")

    def add_label(self, label):
        self.labels.append(label)
        # Kết nối nhãn mới với nhãn trước đó
        if len(self.labels) > 1:
            previous_label = self.labels[-2]
            self.connections.append((previous_label, label))
        self.update()

    def update_connections(self):
        """
        Cập nhật lại các kết nối khi nhãn di chuyển.
        """
        # Cập nhật lại các đường kết nối giữa các nhãn dựa trên vị trí hiện tại của chúng
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)

        # Vẽ tất cả các kết nối giữa các nhãn
        for start_label, end_label in self.connections:
            painter.drawLine(start_label.geometry().center(), end_label.geometry().center())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flowchart Application")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.flowchart_area = FlowChartArea()

        self.toolbar = QVBoxLayout()
        self.button_add_label = QPushButton("Add Label")
        self.button_add_label.clicked.connect(self.add_label)

        self.toolbar.addWidget(self.button_add_label)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addLayout(self.toolbar)
        self.layout.addWidget(self.flowchart_area)

    def add_label(self):
        label = FlowChartLabel("New Label", self.flowchart_area, flowchart_area=self.flowchart_area)
        
        # Nếu có nhãn nào đã tồn tại, đặt nhãn mới gần nhãn cuối cùng
        if self.flowchart_area.labels:
            last_label = self.flowchart_area.labels[-1]
            last_pos = last_label.pos()
            label.move(last_pos.x() + 120, last_pos.y())  # Đặt nhãn mới cạnh nhãn cuối cùng
        else:
            label.move(50, 50)  # Nếu chưa có nhãn, đặt ở vị trí khởi đầu

        label.show()
        self.flowchart_area.add_label(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
