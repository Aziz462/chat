import sys
import sqlite3


from passwordCheck import check_password
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtWidgets import QInputDialog, QMainWindow
from DialogForLogInAndSignUp import Ui_Dialog as LogInSignUpDialog



class log_in_window(QDialog, LogInSignUpDialog):
    def __init__(self, mainwindow):
        QDialog.__init__(self)
        self.mainwindow = mainwindow
        self.setupUi(self)
        self.setWindowTitle("Вход")
        self.con = sqlite3.connect("logs.sqlite")
        self.buttonBox.accepted.connect(self.log_in)

    def cancel(self):
        self.close()

    def log_in(self):
        command = """SELECT * FROM userdata"""
        userdata = self.con.cursor().execute(command).fetchall()
        self.user_found = False
        for name_password in userdata:
            if self.name.text() == name_password[0] and self.password.text() == name_password[1]:
                self.user_found = True
                break
        if not self.user_found:
            self.mainwindow.error.setText('Пользователь не найден')
            return
        name, password = self.name.text(), self.password.text()

        self.mainwindow.username = name
        self.mainwindow.password = password
        self.mainwindow.logged_in = True
        self.close()
