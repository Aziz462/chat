import sys
import sqlite3


from passwordCheck import check_password
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtWidgets import QInputDialog, QMainWindow
from DialogForLogInAndSignUp import Ui_Dialog as LogInSignUpDialog


class sign_up_window(QDialog, LogInSignUpDialog):
    def __init__(self, mainwindow):
        QDialog.__init__(self)
        self.mainwindow = mainwindow
        self.setupUi(self)
        self.con = sqlite3.connect("logs.sqlite")
        self.mainwindow.account_created = False
        self.buttonBox.accepted.connect(self.create_user)
        self.buttonBox.rejected.connect(self.cancel)

    def cancel(self):
        self.close()

    def create_user(self):
        command = """SELECT name FROM userdata"""
        users = self.con.cursor().execute(command).fetchall()
        for username in users:
            if self.name.text() == username[0]:
                self.mainwindow.error.setText('Имя пользователя занято')
                return
        name, password = self.name.text(), self.password.text()
        passcheckresult = check_password(password)
        if passcheckresult != 'ok':
            self.mainwindow.error.setText(passcheckresult)
            return
        print(passcheckresult)
        command = f"""INSERT INTO userdata VALUES ('{name}', '{password}')"""
        self.con.cursor().execute(command)
        self.con.commit()
        self.mainwindow.username = name
        self.mainwindow.account_created = True
        self.close()


