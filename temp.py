from PyQt6.QtCore import QMimeData, Qt, pyqtSignal
from PyQt6.QtGui import QDrag, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DragItem(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContentsMargins(25, 5, 25, 5)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 1px solid black;")
        self.data = self.text()

    def set_data(self, data):
        self.data = data

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)


class DragWidget(QWidget):
    orderChanged = pyqtSignal(list)

    def __init__(self, *args, orientation=Qt.Orientation.Vertical, **kwargs):
        super().__init__()
        self.setAcceptDrops(True)
        self.orientation = orientation

        if self.orientation == Qt.Orientation.Vertical:
            self.blayout = QVBoxLayout()
        else:
            self.blayout = QHBoxLayout()

        self.setLayout(self.blayout)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.position()
        widget = e.source().parent()
        self.blayout.removeWidget(widget)

        for n in range(self.blayout.count()):
            w = self.blayout.itemAt(n).widget()
            if self.orientation == Qt.Orientation.Vertical:
                drop_here = pos.y() < w.y() + w.size().height() // 2
            else:
                drop_here = pos.x() < w.x() + w.size().width() // 2

            if drop_here:
                break
        else:
            n += 1

        self.blayout.insertWidget(n, widget)
        self.orderChanged.emit(self.get_item_data())
        e.accept()

    def add_item(self, item):
        self.blayout.addWidget(item)

    def remove_item(self, item):
        self.blayout.removeWidget(item)
        item.deleteLater()

    def get_item_data(self):
        data = []
        for n in range(self.blayout.count()):
            w = self.blayout.itemAt(n).widget()
            data.append(w.drag_item.data)
        return data


class ButtonWithDelete(QWidget):
    def __init__(self, label, drag_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drag_item = DragItem(label)
        self.drag_item.set_data(label)

        self.delete_button = QPushButton("X")
        self.delete_button.setFixedSize(20, 20)
        self.delete_button.clicked.connect(self.on_delete)

        layout = QHBoxLayout()
        layout.addWidget(self.drag_item)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)

        self.drag_widget = drag_widget

    def on_delete(self):
        self.drag_widget.remove_item(self)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drag = DragWidget(orientation=Qt.Orientation.Vertical)

        for n, l in enumerate(["A", "B", "C", "D"]):
            item = ButtonWithDelete(l, self.drag)
            self.drag.add_item(item)

        self.drag.orderChanged.connect(print)

        container = QWidget()
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.drag)
        layout.addStretch(1)
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication([])
w = MainWindow()
w.show()

app.exec()
