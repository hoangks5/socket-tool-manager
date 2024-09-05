import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsLineItem
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPen
from PyQt6.QtGui import QPainter  # Import QPainter for Antialiasing

class WorkflowView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(WorkflowScene())
        self.setRenderHint(QPainter.RenderHint.Antialiasing)  # Use QPainter's Antialiasing

    def add_workflow(self, x, y, width, height):
        return self.scene().add_workflow_block(x, y, width, height)

    def add_arrow(self, start_block, end_block):
        self.scene().add_arrow(start_block, end_block)

    def update_arrows(self):
        for arrow in self.scene().arrows:
            arrow.update_position()

class WorkflowBlock(QGraphicsRectItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | 
                      QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable | 
                      QGraphicsRectItem.GraphicsItemFlag.ItemSendsScenePositionChanges)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # Cập nhật vị trí sau khi kéo thả
        print(f'Block moved to {self.scenePos()}')

class Arrow(QGraphicsLineItem):
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.update_position()

    def update_position(self):
        start_pos = self.start_item.sceneBoundingRect().center()
        end_pos = self.end_item.sceneBoundingRect().center()
        self.setLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())

class WorkflowScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.arrows = []

    def add_workflow_block(self, x, y, width, height):
        block = WorkflowBlock(x, y, width, height)
        self.addItem(block)
        self.blocks.append(block)
        return block

    def add_arrow(self, start_block, end_block):
        arrow = Arrow(start_block, end_block)
        pen = QPen(Qt.GlobalColor.black, 2)
        arrow.setPen(pen)
        self.addItem(arrow)
        self.arrows.append(arrow)



class WorkflowApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.view = WorkflowView()

        # Thêm các khối workflow
        block1 = self.view.add_workflow(50, 50, 100, 50)
        block2 = self.view.add_workflow(200, 200, 100, 50)
        block3 = self.view.add_workflow(400, 100, 100, 50)

        # Nối các khối bằng mũi tên
        self.view.add_arrow(block1, block2)
        self.view.add_arrow(block2, block3)

        self.view.setWindowTitle("Workflow Designer")
        self.view.setGeometry(100, 100, 600, 400)
        self.view.show()

    def run(self):
        self.exec()

if __name__ == "__main__":
    app = WorkflowApp(sys.argv)
    app.run()
