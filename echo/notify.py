from telegram import Bot

from echo.binanncep2p import BinanceP2P

NOTIFY_USER_ID = 5582758793
def main():
    client = BinanceP2P()
    current_price = client.get_data()

    #bot = Bot(
        #token='5582758793:AAGT3S6MO97BOp1jvhpmZOpBWMX7iU0NRGk',
        #base_url="https://telegg.ru/orig/bot")
    #bot.send_message(chat_id=NOTIFY_USER_ID, text=current_price,)

    print(current_price)
    pass

if __name__ =='__main__':
    main()