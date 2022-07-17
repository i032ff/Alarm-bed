import RPi.GPIO as GPIO
import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
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
def message_text(event):
    text = event.message.text

    # テキストの内容で条件分岐
    if text == '作動':
        # 作動
        SwitchOn()
        # 返事
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage('目覚まし作動')
        )
    elif text == '停止':
        # 停止
        SwitchoOff()
        # 返事
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage('目覚まし停止')
        )
    elif text == '設定':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage('目覚まし停止')
        )

    else:
        # 木霊
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="指定された文字列ではありません\n[" + event.message.text + "]")
        )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port ] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
