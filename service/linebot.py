from flask import request, abort
import logging
import requests
import uuid

from datetime import datetime
from utility.tcp_helper import tcp_client
from utility.open_ai_helper import openApi
from config.config import line_config

# v3
from linebot.v3 import (WebhookHandler)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3 import (
    WebhookHandler
)


access_token = line_config['access_token']
handler = WebhookHandler(line_config['channel_secret'])


def linebot_server():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logging.error(
            "Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


def linebot_push_server():
    msg = '誒胖臉'
    user_id = 'Uafab14d3f48e0865aac0959d004cda9a'
    x_line_uuid = str(uuid.uuid4()).upper()
    print(x_line_uuid)
    try:
        url = 'https://api.line.me/v2/bot/message/push'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'X-Line-Retry-Key': x_line_uuid,
        }

        data = {
            "to": user_id,
            "messages": [
                {
                    "type": "text",
                    "text": msg
                }
            ]
        }

        response = requests.post(url, json=data, headers=headers)
        logging.debug(response)
    except Exception as e:
        print("Exception when calling MessagingApi->reply_message: %s\n" % e)


@handler.add(MessageEvent, message=TextMessageContent)
def response_message(event):
    configuration = Configuration(access_token=access_token)
    with ApiClient(configuration) as api_client:
        current_time = datetime.now()
        msg = event.message.text
        user_id = event.source.user_id

        tcp_string = f'LQ,{current_time},{user_id}, tommy, {msg}'
        tcp_response = tcp_client(tcp_string)
        gpt_response = openApi(tcp_response['message'])
        print(gpt_response)
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=tcp_response['message'])]
            )
        )
