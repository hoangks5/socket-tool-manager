from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QCalendarWidget, QHBoxLayout, QFormLayout, QLineEdit
from PyQt6.QtCore import Qt, QDate

class SchedulerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VPS Scheduler')

        # Create main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Calendar
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.show_hourly_schedule)
        self.layout.addWidget(self.calendar)

        # Table for scheduling
        self.table = QTableWidget(0, 2)  # 0 rows, 2 columns
        self.table.setHorizontalHeaderLabels(['VPS', 'Schedule'])
        self.layout.addWidget(self.table)

        # Add schedule button
        self.add_schedule_button = QPushButton('Add Schedule')
        self.add_schedule_button.clicked.connect(self.add_schedule)
        self.layout.addWidget(self.add_schedule_button)

        # Input form for new schedule
        self.form_layout = QFormLayout()
        self.vps_input = QLineEdit()
        self.script_input = QLineEdit()
        self.form_layout.addRow('VPS:', self.vps_input)
        self.form_layout.addRow('Script:', self.script_input)
        self.layout.addLayout(self.form_layout)

        # Hourly schedule table
        self.hourly_table = QTableWidget(24, 2)  # 24 rows, 2 columns
        self.hourly_table.setHorizontalHeaderLabels(['Hour', 'Scheduled Script'])
        self.hourly_table.setVerticalHeaderLabels([f'{i:02d}:00' for i in range(24)])
        self.layout.addWidget(self.hourly_table)

        # Populate table with VPS
        self.populate_table()

    def populate_table(self):
        # Example data - you can replace this with your own logic
        vps_list = ['VPS1', 'VPS2', 'VPS3']
        for vps in vps_list:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(vps))
            self.table.setItem(row_position, 1, QTableWidgetItem(''))

    def add_schedule(self):
        vps = self.vps_input.text()
        script = self.script_input.text()
        if vps and script:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(vps))
            self.table.setItem(row_position, 1, QTableWidgetItem(script))

    def show_hourly_schedule(self):
        selected_date = self.calendar.selectedDate()
        # Clear the hourly table
        self.hourly_table.clearContents()

        # For demonstration, this just shows empty data
        # Replace with your logic to show scheduled scripts for the selected date
        for hour in range(24):
            self.hourly_table.setItem(hour, 1, QTableWidgetItem('No script scheduled'))

if __name__ == '__main__':
    app = QApplication([])
    window = SchedulerApp()
    window.resize(800, 600)
    window.show()
    app.exec()
