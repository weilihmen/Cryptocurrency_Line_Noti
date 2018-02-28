import re
import json

from linebot import LineBotApi
from linebot.models import TextSendMessage

line_bot_api = LineBotApi('')
def notification(content):
    line_bot_api.push_message('to', TextSendMessage(text=content))
    return True



