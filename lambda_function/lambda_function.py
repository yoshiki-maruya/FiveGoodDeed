import json
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザーからのメッセージに対して同じメッセージを返信する
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )