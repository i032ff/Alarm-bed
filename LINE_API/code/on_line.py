import RPi.GPIO as GPIO
import os
import sys
from multiprocessing import Process, Manager
import time
from datetime import datetime as dt
# encoding: utf-8
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)

# チャンネルシークレットとチャンネルアクセストークンの登録
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# スイッチON・OFF関数の登録
SWITCH_PIN = 23

m = Manager()
db = m.dict()

def watcher(d):
    while True:
        try:
            for key, value in d.items() :
                future = [date - dt.now() for date in value]
                future.sort()

                if (len(future) > 0 and future[0].total_seconds()) < 0:
                    temp = db[key]
                    item = temp.pop(0)                          
                    db[key] = temp
                    print('設定時間になりました!')
                    line_bot_api.push_message(key, TextSendMessage(text='設定時間になりました!'))
        except Exception as e:
            print(e)
        time.sleep(3)


p = Process(name='p1', target=watcher, args=(db, ))
p.start()

def SwitchOn():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SWITCH_PIN, GPIO.OUT)
    GPIO.output(SWITCH_PIN, GPIO.HIGH)
    # GPIO.cleanup()


def SwitchoOff():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SWITCH_PIN, GPIO.OUT)
    GPIO.output(SWITCH_PIN, GPIO.LOW)
    # GPIO.cleanup()


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
# def message_text(event):
#     text = event.message.text

#     # テキストの内容で条件分岐
#     if text == '作動':
#         # 作動
#         SwitchOn()
#         # 返事
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage('目覚まし作動')
#         )
#     elif text == '停止':
#         # 停止
#         SwitchoOff()
#         # 返事
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage('目覚まし停止')
#         )
#     elif text == '設定':
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage('目覚まし停止')
#         )

#     else:
#         # 木霊
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(
#                 text="指定された文字列ではありません\n[" + event.message.text + "]")
#         )

def handle_text_message(event):
    text = event.message.text #message from user
    reply = ""
    print(event)
    print(event.message)
    print(dir(event.source))
    print(vars(event.source))
    inp = text.split(" ")   
    inp.insert(0,event.source.user_id)
    print(inp)    
    try:
        time_set = None
        in_length = len(inp)
        if in_length == 2:
            inp_time = inp[1].split(":")
            try:
                hour = int(inp_time[0])
                minute = 0
                if len(inp_time) == 2:         
                    minute=int(inp_time[1])
                time_set = dt.now().replace(hour=hour,minute=minute,second=0)
                reply = f'time{hour},{minute}'
            except Exception:
                reply = "Jam hanya bisa dari 00-23 dan menit hanya bisa dari 00-59"
        elif in_length == 3:
            inp_date = inp[1].split("-")
            inp_time = inp[2].split(":")
            try:
                day = int(inp_date[0])
                month = int(inp_date[1])
                year = int(inp_date[2])
                hour = int(inp_time[0])
                minute = 0
                if len(inp_time) == 2:         
                    minute=int(inp_time[1])
                time_set = dt(year=year,month=month,day=day,hour=hour,minute=minute)
            except Exception:
                reply = "Format waktunya dd-mm-yyy, jam hanya bisa dari 00-23, dan menit hanya bisa dari 00-59"
        else:
            reply = "Kurang tanggal dan/ jam"
        
        if time_set is not None:    
            try:
                db[inp[0]]
            except:
                db[inp[0]] = []
            if (time_set - dt.now()).total_seconds() > 0:
                db[inp[0]] = db[inp[0]] + [time_set]
                print(time_set)
                alerm_time = time_set.strftime('%Y/%m/%d %H:%M')
                reply = f'{alerm_time} にアラームが設定されました'
            else:
                reply = "Alarm tidak berhasil di set karena waktu nya lampau"
    except ValueError:
        reply = "Jam hanya bisa dari 00-23 dan menit hanya bisa dari 00-59"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply),timeout=10) #reply the same message from user


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port ] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
