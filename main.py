from sign_up import sign_up_window  # Импортируем классы диалоговых окон,
from log_in import log_in_window  # из .py файлов созданных pyuic5
from user_add import User_add
from window_interface import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui # QtGui для добавления гиф иконки
from tunnel import create_tunnel # pyngrok туннели для связи с другими пользователями
from sender import send
import datetime # Для сохранения времени отправленного сообщения
import sys
import sqlite3




class Chat_widget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        self.list_of_chat_obj = [ #  списки объектов разных назначений
            self.add_a_user, # чтобы скрыть или показать их 
            self.label, # в зависимости от того, зарегистрирован пользователь или нет
            self.label_2,
            self.userList,
            self.messages,
            self.msg_txt,
            self.send_btn,
            self.label_chat,
            self.chat_icon,
            self.clear_btn
        ]
        self.list_of_log_in_obj = [
            self.error,
            self.log_in_btn,
            self.sign_up_btn
        ]
        
        self.setWindowTitle("Чаты")

        self.tunnel = create_tunnel() # создание ngrok туннеля
        self.ngrok_link.setText(self.tunnel.public_url)

        self.con = sqlite3.connect("logs.sqlite") # подключение к базе данных
        self.cur = self.con.cursor()

        self.logged_in = False

        self.userDict = {} # Словарь пользователей, с которыми можно начать общение

        self.hide_chat_objects()

        self.chat_icon.move = QtGui.QMovie("гиф_иконки.gif")
        self.chat_icon.move.start()
        self.chat_icon.setMovie(self.chat_icon.move)
        self.chat_icon.setScaledContents(True)


        self.add_a_user.clicked.connect(self.add_user) 
        self.send_btn.clicked.connect(self.send_textmessage)
        self.log_in_btn.clicked.connect(self.log_in)
        self.sign_up_btn.clicked.connect(self.sign_up)
        self.sign_out_btn.clicked.connect(self.sign_out)
        self.refresh_btn.clicked.connect(self.refresh_messages)
        self.userList.currentItemChanged.connect(self.refresh_messages)
        self.clear_btn.clicked.connect(self.clear_messages)

    def clear_messages(self): 
        """Очищает сообщения"""
        command = "DELETE from messages"
        self.cur.execute(command)
        self.refresh_messages()

    def send_textmessage(self): 
        """Метод для отправки сообщений, использующий функцию из отдельного файла sender.py"""
        if len(self.msg_txt.text()) > 50:
            self.error_3.setText('Сообщение преодолело максимальное кол-во символов: 50')
            return
        if not self.userList.currentItem():
            return
        URL = self.userDict[self.userList.currentItem().text()]
        sender = self.username
        receiver = self.userList.currentItem().text()
        timenow = datetime.datetime.now().strftime("%H:%M:%S")
        text = self.msg_txt.text()
        command = f"""INSERT INTO messages VALUES("{sender}", "{receiver}", "{timenow}", "{text}")"""
        self.cur.execute(command)
        self.con.commit()
        send(URL, sender, receiver, timenow, text)

        self.refresh_messages()
        self.msg_txt.setText('')

    def refresh_messages(self): 
        """Обновляет сообщения"""
        self.other_user = self.userList.currentItem()
        if not self.other_user:
            return
        else:
            self.other_user = self.userList.currentItem().text()
        try:
            command = f"""SELECT sender, time, text FROM messages
                          WHERE receiver like '{self.other_user}' AND sender like '{self.username}'"""
            command1 = f"""SELECT sender, time, text FROM messages
                           WHERE receiver like '{self.username}' AND sender like '{self.other_user}'"""
        except sqlite3.OperationalError:
            return
        self.messages.clear()
        messageList = self.cur.execute(command).fetchall()
        messageList += self.cur.execute(command1).fetchall()
        self.label.setText(F'Переписка с {self.other_user}')
        messageList.sort(key=lambda x: x[1], reverse=True)
        for message in messageList:
            self.messages.addItem(str(message[1][:-3]) + ' - ' + str(message[2]) + ' - ' + str(message[0]))

    def sign_out(self): 
        """Осуществляет выход из аккаунта"""
        self.logged_in = False
        self.hide_chat_objects()

    def hide_chat_objects(self):
        """Метод нужен, чтобы можно было в одном окне совместить окно входа и интерфейс мессенджера"""
        for obj in self.list_of_chat_obj:
            obj.hide()
        for obj in self.list_of_log_in_obj:
            obj.show()
        self.resize(500, 400)
        self.userList.clear()
        self.messages.clear()

    def show_chat_objects(self):
        """Метод нужен, чтобы можно было в одном окне совместить окно входа и интерфейс мессенджера"""
        for obj in self.list_of_chat_obj:
            obj.show()
        for obj in self.list_of_log_in_obj:
            obj.hide()
        self.resize(1007, 702)


    def sign_up(self):
        """Метод для диалогового окна для регистрации"""
        window = sign_up_window(self)
        # Пользователь вводит имя и пароль
        # Аккаунт не создаётся если:
        #     Имя пользователя занято
        #     Некорректный пароль
        #     Пользователь закрывает окно или нажимает cancel
        window.show()
        window.exec()
        if not self.account_created:
            pass
        else:
            self.error.setText('Вы успешно создали аккаунт, попробуйте войти')

    def log_in(self):
        """Метод для диалогового окна для входа"""
        window = log_in_window(self)
        # Пользователь вводит имя и пароль
        # Вход не осуществляется если:
        #     Имя не найдено
        #     Пользователь закрывает окно или нажимает cancel
        window.show()
        window.exec()
        if self.logged_in:
            self.show_chat_objects()

    def add_user(self):
        """Метод для диалогового окна для добавления других пользователей"""
        window = User_add(self)
        window.show()
        window.exec()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chat_widget()
    ex.show()
    sys.exit(app.exec_())
