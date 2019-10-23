# app.py
from flask import Flask, request, render_template, jsonify
from decouple import config
import requests
import random

import google_translate as gt

app = Flask(__name__)

token = config("TOKEN")
token_short = ''.join(token.split(':')[1:])
api_url = f"https://api.telegram.org/bot{token}"
update_url = f"{api_url}/getUpdates"
# print(update_url)``

# print(api_url)

response = requests.get(update_url).json() # json형태로 받아옵니다.
# print(response['result'][0]['message']['chat'])

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    message = request.args.get("message")
    message_url = f"{api_url}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(message_url)
    return "메시지 전송 완료했어용!"

@app.route(f'/{token}', methods=["POST"])
def telegram():
    message = request.get_json()

    # chat id를 가져옵니다.
    chat_id = message['message']['chat']['id']

    # 우리가 텔레그램에서 보낸 메세지를 꺼냅니다.
    text = message['message']['text']

    if text == "로또":
        reply = random.sample(range(1, 46), 6)
    elif text[0:3] == '/번역':
        reply = gt.translate(text[4:])
    else:
        reply = text

    # 메세지를 보내는 요청 주소를 통해 텔레그램에 전달!
    message_url = f"{api_url}/sendMessage?chat_id={chat_id}&text={reply}"
    requests.get(message_url)

    return f'{chat_id} / {text}', 200

@app.route(f'/{token_short}', methods=["POST"])
def telegram2():
    message = request.get_json()

    # 우리가 텔레그램에서 보낸 메세지를 꺼냅니다.
    text = message['queryResult']['queryText']

    if text == "로또":
        reply = ' '.join(map(str, random.sample(range(1, 46), 6)))
    elif text[0:3] == '/번역':
        reply = gt.translate(text[4:])
    else:
        reply = '' # 나머지는 google dialogflow에서 처리

    # 메세지를 보내는 요청 주소를 통해 텔레그램에 전달!
    # message_url = f"{api_url}/sendMessage?chat_id={chat_id}&text={reply}"
    # requests.get(message_url)
    result = {'fulfillmentText': reply}
    return jsonify(result)
    # return f'{chat_id} / {text}', 200


if __name__ == "__main__":
    app.run(debug=True)