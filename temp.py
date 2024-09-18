import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QCalendarWidget, QPushButton, QTableWidget, QTableWidgetItem, 
    QInputDialog, QMessageBox
)
from PyQt6.QtCore import QDate

class CalendarApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendar Task App")
        self.setGeometry(100, 100, 600, 400)

        # Dictionary to store tasks for each day
        self.tasks = {}

        # Create layout
        main_layout = QVBoxLayout()

        # Create calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.show_tasks)
        main_layout.addWidget(self.calendar)

        # Create table for showing tasks
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(2)
        self.task_table.setHorizontalHeaderLabels(["Time", "Task"])
        main_layout.addWidget(self.task_table)

        # Create buttons for adding, editing, and removing tasks
        button_layout = QHBoxLayout()
        self.add_task_btn = QPushButton("Add Task")
        self.add_task_btn.clicked.connect(self.add_task)
        self.remove_task_btn = QPushButton("Remove Task")
        self.remove_task_btn.clicked.connect(self.remove_task)
        button_layout.addWidget(self.add_task_btn)
        button_layout.addWidget(self.remove_task_btn)
        
        main_layout.addLayout(button_layout)

        # Set main layout
        self.setLayout(main_layout)

    def show_tasks(self):
        """Display tasks for the selected date."""
        self.task_table.setRowCount(0)  # Clear the table
        selected_date = self.calendar.selectedDate()
        date_str = selected_date.toString("yyyy-MM-dd")
        
        if date_str in self.tasks:
            tasks_for_day = self.tasks[date_str]
            for time, task in tasks_for_day:
                row_position = self.task_table.rowCount()
                self.task_table.insertRow(row_position)
                self.task_table.setItem(row_position, 0, QTableWidgetItem(time))
                self.task_table.setItem(row_position, 1, QTableWidgetItem(task))

    def add_task(self):
        """Add a new task for the selected date."""
        selected_date = self.calendar.selectedDate()
        date_str = selected_date.toString("yyyy-MM-dd")

        # Get task details from the user
        time, ok = QInputDialog.getText(self, "Task Time", "Enter task time (e.g. 14:00):")
        if not ok or not time:
            return
        task, ok = QInputDialog.getText(self, "Task Description", "Enter task description:")
        if not ok or not task:
            return

        # Store task
        if date_str not in self.tasks:
            self.tasks[date_str] = []
        self.tasks[date_str].append((time, task))

        # Update the table
        self.show_tasks()

    def remove_task(self):
        """Remove the selected task from the table."""
        selected_row = self.task_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a task to remove.")
            return

        selected_date = self.calendar.selectedDate()
        date_str = selected_date.toString("yyyy-MM-dd")
        
        if date_str in self.tasks:
            del self.tasks[date_str][selected_row]
            if not self.tasks[date_str]:  # Remove date if no tasks left
                del self.tasks[date_str]
        
        self.show_tasks()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec())
