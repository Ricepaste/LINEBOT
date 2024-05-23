import os
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi(
    '0VH971y+3x7IbFvRMKzY+0w/pFaOOvJa6M+IEpADMVmNWZLtmLLNB7wek1PBcOnKVAWRYh3eqtD2JjNXpReRpxg42KQTEFQqMLk9wr9uZR3TrSOAhlRnT1URcX3zDiNFiIKYue4AQXT3T0pySXGEVQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ef511c10f38305d34d906fe9421acd39')


@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event


@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    line_bot_api.reply_message(reply_token, TextSendMessage(text=message))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
