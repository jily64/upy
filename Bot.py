import logging
import os
import time
import json
import telegram
from telegram import files as fil

import Controller

# импорты библиотек, которые мы установили (тут только python telegram bot)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler
)

import main

# сетап логгирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger()

# глобальная переменная, которая будет нужна потом
some_bot_message = None

class bot:
    # описание функций, которые могут как-то что-то делать
    def __init__(self):
        pass
    def start(self, update: Update, context: CallbackContext):
        """Отправить пользователю информацию по команде /start"""
        keyboard = [
            [
                InlineKeyboardButton("Больше или Меньше", callback_data='bm'),
                InlineKeyboardButton("Статистика", callback_data='statics')]

        ]
        print(update)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Выберите опцию:", reply_markup=reply_markup)

    def button(self, update:telegram.Update, context):
        query = update.callback_query
        query.answer()
        # здесь можно добавить обработчик для ответа на callback-запрос
        user_id = update.effective_chat.id

        if "bm" in query.data:
            bm_game = main.UpGame.bm()
            keyboard = [
                [
                    InlineKeyboardButton("Больше", callback_data='bmБольше'),
                    InlineKeyboardButton("Меньше", callback_data='bmМеньше')],
                [
                    InlineKeyboardButton("На главную", callback_data='Main')
                ]
            ]

            if query.data[2::] == "Больше" or query.data[2::] == "Меньше":
                game = bm_game.big_or_small(query.data[2::])

                if game == True:
                    ans = "Вы угадали! +10$"
                    cash = 10
                else:
                    ans = "Неверно! - 10$"
                    cash = -10

                with open("data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                try:
                    user_data = data[str(user_id)]
                    user_data["money"] += cash
                    user_data["games"] += 1

                except:
                    user_data = {
                        "money": cash,
                        "games": 1
                    }

                data[str(user_id)] = user_data

                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                print(update.message)

                new_markup = [
                [
                    InlineKeyboardButton("Заново", callback_data='bmRetry')]
                ]

                new_markup = InlineKeyboardMarkup(new_markup)

                update.callback_query.message.edit_text(ans, reply_markup=new_markup)

            else:

                reply_markup = InlineKeyboardMarkup(keyboard)
                update.callback_query.message.edit_text("Выберите, число будет больше или меньше нуля?", reply_markup=reply_markup)

        elif query.data == "statics":
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            try:
                user_data = data[str(user_id)]

            except:
                user_data = {
                    "money": 0,
                    "games": 0
                }

                data[str(user_id)] = user_data

                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            print(update)

            new_markup = [
                [
                    InlineKeyboardButton("Вернуться", callback_data='Main')]
            ]
            new1_markup = InlineKeyboardMarkup(new_markup)

            mess = f'*Статистика пользователя {update.effective_chat.username}*\n\nДенег - {user_data["money"]}\nВсего игр - {user_data["games"]}'
            update.callback_query.message.edit_text(mess, parse_mode="markdown", reply_markup=new1_markup)
        elif query.data == "Main":
            keyboard = [
                [
                    InlineKeyboardButton("Больше или Меньше", callback_data='bm'),
                    InlineKeyboardButton("Статистика", callback_data='statics')]

            ]
            print(update)
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.callback_query.message.edit_text("Выберите опцию:", reply_markup=reply_markup)


    def echo(self, update: Update, context: CallbackContext):
        """Отправить пользователю то, что мы ему написали"""
        user_id = update.effective_chat.id
        message_text = update.message.text
        context.bot.send_message(chat_id=user_id, text=message_text)





    def main(self):
        # сетап
        updater = Updater(
            token="6377435643:AAEzxRszxMagJhpPYnTU8CgJx2h7NmFJ16U", use_context=True
        )
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CallbackQueryHandler(self.button))
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.echo))


        updater.start_polling()
b = bot()
b.main()