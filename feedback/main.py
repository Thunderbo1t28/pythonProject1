from logging import getLogger

from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import Updater
from telegram.utils.request import Request

from echo.config import TG_TOKEN
from echo.config import TG_URL
from echo.config import FEEDBACK_USER_ID

from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from echo.binanncep2p import BinanceP2P

button_help = 'Курс'
order = 'Заявка'



def button_help_handler(update: Update):
    chat_id = update.message.chat_id
    client = BinanceP2P()
    current_price = client.get_data()
    update.message.reply_text(
        text=current_price,
        #reply_markup=ReplyKeyboardRemove(),
    )
    #update.message.reply_text(
        #text=current_price,
        #reply_markup=ReplyKeyboardRemove(),
    #)
def button_order_handler(update: Update, context: CallbackContext):
    forward_from = update.message
    if forward_from:
        text = 'Сообщение от автора канала:\n\n' + update.message.text
        #context.bot.send_message(
            #chat_id=FEEDBACK_USER_ID,
            #text=text,
        #)
        update.message.forward(
            chat_id=FEEDBACK_USER_ID,
        )
    else:
        error_message = 'Нельзя ответить самому себе'


    update.message.reply_text(
        text='Заявка успешно отправлена, с вами скоро свяжется оператор',
        reply_markup=ReplyKeyboardRemove(),
    )

#config = load_config()

logger = getLogger(__name__)

#debug_requests = logger_factory(logger=logger)



def do_start(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_help), KeyboardButton(text=order),
            ],
        ],
        resize_keyboard=True,
    )
    update.message.reply_text(
        text='Добро пожаловать, обмен производится с карты Российского банка на карту банка Казахстана, актуальный курс можете посмотреть нажав на кнопку Курс',
        reply_markup=reply_markup,
    )



def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    if chat_id == FEEDBACK_USER_ID:
        # Смотрим на реплаи
        error_message = None
        text = update.message.text
        reply = update.message.reply_to_message
        #if reply:
            #forward_from = reply.forward_from
            #if forward_from:
                #text = 'Сообщение от автора канала:\n\n' + update.message.text
                #context.bot.send_message(
                    #chat_id=forward_from.id,
                    #text=text,
                #)
                #update.message.reply_text(
                    #text='Сообщение было отправлено',
                #)
            #else:
                #error_message = 'Нельзя ответить самому себе'
        if text == button_help:
            return button_help_handler(update=update)
        elif text == order:
            return button_order_handler(update=update,context=context)
        else:
            reply_markup = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=button_help), KeyboardButton(text=order),
                    ],
                ],
                resize_keyboard=True,
            )
            reply_text = "Добро пожаловать, обмен производится с карты Российского банка на карту банка Казахстана, актуальный курс можете посмотреть нажав на кнопку Курс"
            update.message.reply_text(
                text=reply_text,
                reply_markup=reply_markup,
            )


         #Отправить сообщение об ошибке если оно есть
        if error_message is not None:
            update.message.reply_text(
                text=reply_text,
            )
    else:
        # Пересылать всё как есть
        #update.message.forward(
            #chat_id=FEEDBACK_USER_ID,
        #)
        #update.message.reply_text(
            #text='Сообщение было отправлено',
        #)
        error_message = None
        text = update.message.text
        reply = update.message.reply_to_message
        # if reply:
        # forward_from = reply.forward_from
        # if forward_from:
        # text = 'Сообщение от автора канала:\n\n' + update.message.text
        # context.bot.send_message(
        # chat_id=forward_from.id,
        # text=text,
        # )
        # update.message.reply_text(
        # text='Сообщение было отправлено',
        # )
        # else:
        # error_message = 'Нельзя ответить самому себе'
        if text == button_help:
            return button_help_handler(update=update)
        elif text == order:
            return button_order_handler(update=update, context=context)
        else:
            reply_markup = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=button_help), KeyboardButton(text=order),
                    ],
                ],
                resize_keyboard=True,
            )
            reply_text = "Добро пожаловать, обмен производится с карты Российского банка на карту банка Казахстана, актуальный курс можете посмотреть нажав на кнопку Курс"
            update.message.reply_text(
                text=reply_text,
                reply_markup=reply_markup,
            )

        # Отправить сообщение об ошибке если оно есть
        if error_message is not None:
            update.message.reply_text(
                text=reply_text,
            )


def main():
    logger.info('Запускаем бота...')

    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        token=TG_TOKEN,
        request=req,
        base_url=TG_URL,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info(f'Bot info: {info}')

    # Навесить обработчики команд
    start_handler = CommandHandler('start', do_start)
    message_handler = MessageHandler(Filters.all, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()

    logger.info('Закончили...')


if __name__ == '__main__':
    main()
