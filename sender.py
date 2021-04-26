import requests


def send(URL, sender, receiver, time, text):
    requests.post(URL + '/textreceiver',
                  json={"sender": sender, "receiver": receiver, "time": time, "text": text})

