from flask import Flask, request
import sqlite3, requests




def start_server():

    app = Flask(__name__)


    @app.route('/usercheck')
    def usercheck():
        """Функция нужна для user_add.py для проверки ссылки"""
        return 'UserIsReal' 

    @app.route('/textreceiver', methods=['POST', 'GET']) 
    def textreceiver():
        """Обрабатывает сообщения и отправляет их в базу данных"""
        data = request.json
        con = sqlite3.connect("logs.sqlite") 
        cur = con.cursor() 
        
        cur.execute(f"""INSERT INTO messages VALUES("{data['sender']}", "{data['receiver']}", "{data['time']}", "{data['text']}" )""")
        con.commit()
        return 'success'

    @app.route('/')
    def default_page():
        """Базовая Страница"""
        return "That's default page"
    

    app.run()


start_server()