from telegram import Bot
from telegram.ext import Updater

from telegram import ParseMode
from telegram.utils.request import Request
import json
import sys

import texts_for_images

TG_TOKEN = ""

with open(sys.argv[1], 'r') as f:
    list_with_user_id = json.loads(f.read())


def main():

    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )

    bot = Bot(
        token=TG_TOKEN,
        request=req,
        base_url='https://telegg.ru/orig/bot',
    )


    info = bot.get_me()
    print('Confirmation that bot is online and working')
    print(info)

    for i in range(len(list_with_user_id)):
        bot.send_photo(
            chat_id=list_with_user_id[i],
            photo=open(sys.argv[2], 'rb'),
            caption=texts_for_images.text_for_image_RTS,
            parse_mode='markdown'

        )

    print('sending is complete')


if __name__ == '__main__':
    main()
