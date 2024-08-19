import json
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

def lambda_handler(event, context):
    # Lambdaに届いたHTTPリクエストを取得
    headers = event['headers']
    body = event['body']
    
    # LINE Botの署名検証
    signature = headers['x-line-signature']
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid signature. Check your Channel Secret and Access Token.')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }

def get_english_data():
    json_open = open('english_data.json', 'r')
    json_data = json.load(json_open)
    return json_data

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # generate randam int
    index = random.randint(0, 97)
    english_data = get_english_data()
    reply_message = english_data[index]['sentence']
    # when user message is '成長', bot reply to english sentence
    if event.message.text == '成長':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="成長と打ち込むと英語センテンスが送られてくるよ！そのセンテンスで英作文を作ってみよう！")
        )
    
    