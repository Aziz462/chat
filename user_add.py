from PyQt5.QtWidgets import QDialog
from pyngrok import ngrok
import requests
from DialogForUserAdd import Ui_Dialog as add_user_window


class User_add(QDialog, add_user_window):
    def __init__(self, mainwindow):
        QDialog.__init__(self)
        self.mainwindow = mainwindow
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.add_to_userlist)
        self.buttonBox.rejected.connect(self.cancel)
    
    def cancel(self):
        self.close()


    def add_to_userlist(self):
        try:
            # Отправляется запрос ссылке и если она действительна пользователь добавляется
            requests.get(self.ngrok_tunnel.text() + '/usercheck')
        except:
            self.mainwindow.error_2.setText('Пользователь не найден')
            return
        self.mainwindow.userDict[self.name.text()] = self.ngrok_tunnel.text()
        self.mainwindow.userList.addItem(self.name.text())
        self.close()