# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(311, 173)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/logo-iart.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QWidget{\n"
"background-color: rgb(0, 0, 0);\n"
"}\n"
"QMessageBox{\n"
"background-color: rgb(255, 255, 255,0);\n"
"    color: rgb(255, 255, 0);\n"
"}\n"
"QPushButton{\n"
"border-radius:10px;\n"
"border: 2px solid #23074d;\n"
"background-color: #cc5333;\n"
"color:#FFB6C1;\n"
"height: 40px;\n"
"width: 120px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 2px solid #009fff ;\n"
"    background-color:#23074d;\n"
"            }\n"
"QPushButton:pressed {\n"
"                background-color: #5650de; /* Màu nền khi nhấn */\n"
"            }\n"
"\n"
"QLineEdit{\n"
"background-color: rgb(220, 220, 220);\n"
"border-radius: 10px;\n"
"    color: rgb(34, 0, 52);\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 100, 111, 41))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 40, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Iart VPSControl Pro"))
        self.pushButton.setText(_translate("MainWindow", "Connect"))
        self.lineEdit.setText(_translate("MainWindow", "3.18.29.6:12345"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Địa chỉ socket"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
