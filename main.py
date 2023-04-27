from telegram import Bot
from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler
from telegram.ext import CallbackContext
from telegram.utils.request import Request

from db import add_message
from db import init_db

import texts
import texts_for_images

TG_TOKEN = ""

CALLBACK_BUTTON_1 = 'callback_button_1'
CALLBACK_BUTTON_2 = 'callback_button_2'
CALLBACK_BUTTON_3 = 'callback_button_3'
CALLBACK_BUTTON_4 = 'callback_button_4'

TILES = {
    CALLBACK_BUTTON_1: 'Хорошо',
    CALLBACK_BUTTON_2: 'Не нажимайте',
    CALLBACK_BUTTON_3: 'Я понял. Сделаю',
    CALLBACK_BUTTON_4: 'Вопрос?',
}


# def message_handler(bot: Bot, update: Update):

def get_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(TILES[CALLBACK_BUTTON_1], callback_data=CALLBACK_BUTTON_1)
            ],
            [
                InlineKeyboardButton(TILES[CALLBACK_BUTTON_2], callback_data=CALLBACK_BUTTON_2)
            ],
        ],
    )


def get_keyboard_2():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(TILES[CALLBACK_BUTTON_3], callback_data=CALLBACK_BUTTON_3)
            ],
            [
                InlineKeyboardButton(TILES[CALLBACK_BUTTON_4], callback_data=CALLBACK_BUTTON_4)
            ],
        ],
    )


def callback_handler(update: Update, context: CallbackContext):
    callback_data = update.callback_query.data
    user = update.effective_user

    if callback_data == CALLBACK_BUTTON_1:
        update.effective_message.reply_text(
            text=texts.text2,
            reply_markup=get_keyboard_2(),
        )
    elif callback_data == CALLBACK_BUTTON_3:
        update.effective_message.reply_text(
            text=texts.text3,
        )
    elif callback_data == CALLBACK_BUTTON_4:
        update.effective_message.reply_text(
            text='Можете написать автору проекта @daniil_murga'
        )
    elif callback_data == CALLBACK_BUTTON_2:
        update.effective_message.reply_text(
            text=texts.dont_press_text,
            reply_markup=get_keyboard(),
        )




def message_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    text = update.message.text

    if text == '/start':
        add_message(user_id=user.id, text=text)
        update.message.reply_text(
            text=texts.text1,
            reply_markup=get_keyboard(),
            parse_mode='markdown',
        )
    elif text == '/what_to_trade':
        add_message(user_id=user.id, text=text)
        update.message.reply_text(
            text=texts.what_to_trade_text,
        )

    elif text == '/how_to_trade':
        add_message(user_id=user.id, text=text)
        update.message.reply_text(
            text=texts.how_to_trade_text,
            parse_mode='markdown',
        )

    elif text == '/author':
        add_message(user_id=user.id, text=text)
        update.message.reply_text(
            text=texts.author_text,
            parse_mode='markdown'
        )

    elif text == '/brokers':
        add_message(user_id=user.id, text=text)
        update.message.reply_text(
            text=texts.brokers_text,
        )

    elif text == '/order_types':
        add_message(user_id=user.id, text=text)
        update.message.reply_text(
            text=texts.order_types_text,
            parse_mode='markdown'
        )

    elif text == '/example':
        add_message(user_id=user.id, text=text)
        update.message.reply_photo(
            caption=texts_for_images.text_for_example_image_RTS,
            photo=open('example_image.png', 'rb'),
            parse_mode='markdown'
        )

    else:
        update.message.reply_text(
            text='Поддерживаются только предложеные команды'
        )


def main():
    print('Starting bot with no sql')

    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )

    bot = Bot(
        token=TG_TOKEN,
        request=req,
        base_url='https://telegg.ru/orig/bot',
    )

    updater = Updater(
        bot=bot,
        use_context=True,
    )

    info = bot.get_me()
    print(info)

    init_db()

    updater.dispatcher.add_handler(MessageHandler(Filters.command, message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
