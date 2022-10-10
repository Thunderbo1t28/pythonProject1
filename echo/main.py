from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram import Bot
#from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
#from telegram.ext import CommandHandler
#from telegram.ext import ConversationHandler
from echo.binanncep2p import BinanceP2P
from echo.config import TG_TOKEN
from echo.config import TG_URL
from echo.config import FEEDBACK_USER_ID


button_help = 'Курс'
order = 'Заявка'



def log_error(f):
    def inner(*args,**kwargs):
        try:
            return f(*args,**kwargs)
        except Exception as e:
            print(f'Error: {e}')
            raise e

    return inner
def do_start(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    bot.send_message(
        chat_id=chat_id,
        text="Добро пожаловать, обмен производится с карты Российского банка на карту банка Казахстана, актуальный курс можете посмотреть нажав на кнопку Курс",

    )

def button_help_handler(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    client = BinanceP2P()
    current_price = client.get_data()
    bot.send_message(
        chat_id=chat_id,
        text=current_price,
        reply_markup=ReplyKeyboardRemove(),
    )
    #update.message.reply_text(
        #text=current_price,
        #reply_markup=ReplyKeyboardRemove(),
    #)
def button_order_handler(bot: Bot, update: Update):
    client = BinanceP2P()
    current_price = client.get_data()
    update.message.reply_text(
        text=current_price,
        reply_markup=ReplyKeyboardRemove(),
    )



@log_error
def message_handler(bot: Bot, update: Update):
    chat_id = update.message.chat_id

    text = update.message.text
    if text ==button_help:
        return button_help_handler(bot=bot, update=update,)
    elif text ==order:
        return button_order_handler(bot=bot, update=update,)
    else:
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=button_help), KeyboardButton(text=order),
                ],
            ],
            resize_keyboard=True,
        )
        reply_text ="Добро пожаловать, обмен производится с карты Российского банка на карту банка Казахстана, актуальный курс можете посмотреть нажав на кнопку Курс"
        bot.send_message(
            chat_id=chat_id,
            text=reply_text,
            reply_markup=reply_markup,
        )




def main():
    print('Start')
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_URL,
    )
    updater = Updater(
        bot=bot, )

    #conv_handler = ConversationHandler(
        #entry_points=[MessageHandler(Filters.regex(order), start_handler),],
        #states={
            #NAME: [MessageHandler(Filters.all, name_handler, pass_user_data=True),],
            #GENDER: [MessageHandler(Filters.all, age_handler, pass_user_data=True),],
            #AGE: [MessageHandler(Filters.all, finish_handler, pass_user_data=True),],

        #},
        #fallbacks=[CommandHandler('cancel', cancel_handler),],
    #)

    #updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

