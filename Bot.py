import logging
import os
import time

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


# сетап логгирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger()

# глобальная переменная, которая будет нужна потом
some_bot_message = None


# описание функций, которые могут как-то что-то делать
def start(update: Update, context: CallbackContext):
    """Отправить пользователю информацию по команде /start"""
    keyboard = [
        [
            InlineKeyboardButton("Сапер", callback_data='Saper'),
            InlineKeyboardButton("Рулетка (не робит пока что)", callback_data='2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите опцию:", reply_markup=reply_markup)


def button(update:telegram.Update, context):
    query = update.callback_query
    query.answer()
    # здесь можно добавить обработчик для ответа на callback-запрос
    user_id = update.effective_chat.id
    controller = Controller.Telegramm_Controller()
    saper_game = controller.saper()
    if query.data == 'Saper':

        path = saper_game.generate_new_image(user=update.effective_chat)

        saper_keyboard = []

        for i in range(len(saper_game.matrix)):
            button_line = []
            for j in range(len(saper_game.matrix[i])):
                print(saper_game.matrix[i][j])
                button = InlineKeyboardButton(str(j), callback_data=f"{i}<!>{j}")
                button_line.append(button)
            saper_keyboard.append(button_line)

        markup = InlineKeyboardMarkup(saper_keyboard)



        context.bot.send_photo(chat_id=user_id, caption="Saper",photo=open(path, "rb"), reply_markup=markup)
        #os.remove(path)

    elif "<!>" in query.data:
        saper_keyboard = []
        data = query.data.split("<!>")
        data[0] = int(data[0])
        data[1] = int(data[1])
        path = saper_game.regenerate_image_with_bomb_checker(point=data, user=update.effective_chat)
        if path == "lose":
            context.bot.send_message(chat_id=user_id, text="Вы проиграли!")
            return
        print(path)
        for i in range(len(saper_game.matrix)):
            button_line = []
            for j in range(len(saper_game.matrix[i])):
                print(saper_game.matrix[i][j])
                button = InlineKeyboardButton(str(j), callback_data=f"{i}<!>{j}")
                button_line.append(button)
            saper_keyboard.append(button_line)

        markup = InlineKeyboardMarkup(saper_keyboard)

        context.bot.send_photo(chat_id=user_id, caption="Saper", photo=open(path, "rb"), reply_markup=markup)
        os.remove(path)
    print(query.data)



def echo(update: Update, context: CallbackContext):
    """Отправить пользователю то, что мы ему написали"""
    user_id = update.effective_chat.id
    message_text = update.message.text
    context.bot.send_message(chat_id=user_id, text=message_text)





def main():
    # сетап
    updater = Updater(
        token="6377435643:AAEzxRszxMagJhpPYnTU8CgJx2h7NmFJ16U", use_context=True
    )
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))


    updater.start_polling()

main()