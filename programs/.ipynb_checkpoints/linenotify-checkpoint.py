import requests

def send_message(message):
    f = open('../key/line_notify.txt', 'r', encoding='UTF-8')
    token = f.read()
    f.close()

    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization" : "Bearer "+ token}

    payload = {"message" :  message}

    r = requests.post(url ,headers = headers ,params=payload)

if __name__ == "__main__":
    send_message("aaa")
