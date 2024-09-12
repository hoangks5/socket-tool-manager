import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QRubberBand
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QRect, QSize
from PIL import ImageGrab

class ScreenCapture(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = parent
        self.screenshot = self.capture_screen()
        self.pixmap = QPixmap.fromImage(self.pil_image_to_qimage(self.screenshot))

        # Set the size of the window to the size of the screenshot
        self.setWindowTitle("Select a region")
        self.setGeometry(0, 0, self.pixmap.width(), self.pixmap.height())
        
        self.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.origin = None
        
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.setCentralWidget(self.label)
        
        # Disable resizing of the window
        self.setFixedSize(self.pixmap.size())
        
        self.setMouseTracking(True)
        self.label.setMouseTracking(True)

    def capture_screen(self):
        # Capture the entire screen
        screenshot = ImageGrab.grab()
        return screenshot
    
    def pil_image_to_qimage(self, pil_image):
        # Convert PIL image to QImage
        rgb_image = pil_image.convert("RGB")
        qimage = QImage(rgb_image.tobytes(), rgb_image.width, rgb_image.height, rgb_image.width * 3, QImage.Format.Format_RGB888)
        return qimage

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.origin = event.position().toPoint()
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if self.origin is not None:
            rect = QRect(self.origin, event.position().toPoint()).normalized()
            self.rubberBand.setGeometry(rect)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.origin is not None:
            rect = QRect(self.origin, event.position().toPoint()).normalized()
            x, y, width, height = rect.getRect()
            self.ui.lineEdit_90.setText(str(x))
            self.ui.lineEdit_91.setText(str(y))
            self.ui.lineEdit_89.setText(str(width))
            self.ui.lineEdit_88.setText(str(height))
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenCapture()
    window.showFullScreen()  # Make the window fullscreen
    sys.exit(app.exec())
