
import telegram.ext as bot
import yfinance
import pandas as pd
import numpy as np
import mplfinance
from datetime import datetime, timedelta

TOKEN = '5487092264:AAHcqAcf3q31Z0Dn35-o2FUfGpYQfYDdzvI'
is_bot_started = False
is_user_login = False
MAX = 100000
lst_interval = ['1m', '2m', '5m', '15m', '30m', '60m',
                '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']


# start command
def start(update, context):
    global is_bot_started
    if is_bot_started != True:
        update.message.reply_text(
            "Enter Your Username : \n Use /user+username")
        is_bot_started = True
    else:
        update.message.reply_text("Already Executed")


# user command
def user(update, context):
    global is_user_login
    given_by_user = context.args[0]
    list_user = ['abc', 'bad']
    if is_user_login != True:
        if given_by_user in list_user:
            update.message.reply_text(
                "Welcome to the bot 😁 \n Use /help to know more about me 😊")
            is_user_login = True
        else:
            update.message.reply_text("Invalid User :( \n Try Again")
    else:
        update.message.reply_text("Command Already Executed")

# help command


def Help(update, context):
    update.message.reply_text("""

                `OUR SERVICES`

            1. Find Support & Resistance For the Stock.
                || Rules ||
                || Use /stock + stockname(capital) + days + interval ||

            2. Find Breakout of the stock.

        """)


def get_min_3(df, lenght):

    firstmin = MAX
    secmin = MAX
    thirdmin = MAX
    n = lenght
    arr = df
    for i in range(0, n):

        # Check if current element
        # is less than firstmin,
        # then update first,second
        # and third

        if arr[i] < firstmin:
            thirdmin = secmin
            secmin = firstmin
            firstmin = arr[i]

        # Check if current element is
        # less than secmin then update
        # second and third
        elif arr[i] < secmin:
            thirdmin = secmin
            secmin = arr[i]

        # Check if current element is
        # less than,then update third
        elif arr[i] < thirdmin:
            thirdmin = arr[i]
    return firstmin, secmin, thirdmin

# getting the support and resistance for the stock


def getsupportandresist(update, context):
    stock_name = context.args[0]
    days = context.args[1]
    interval = context.args[2]
    global lst_interval

    ticker_symbol = stock_name
    ticker = yfinance.Ticker(ticker_symbol)

    if (ticker.info['regularMarketPrice'] == None):
        update.message.reply_text("Invalid Stock !!")

    elif (interval not in lst_interval):
        update.message.reply_text(
            f"Invalid Interval!! \n Valid Interval are {lst_interval}")
    else:
        start_date = datetime.now() - \
            timedelta(days=int(days))
        end_date = datetime.now()

        df = ticker.history(interval=interval, start=start_date, end=end_date)

        df['Date'] = pd.to_datetime(df.index)
        #[12 ,10 ,13,26] [10,12,13,26]
        #df['Date'] = df['Date'].apply(mpl_dates.date2num)
        df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

        firsup, secondsup, thirdsup = get_min_3(df['Low'], len(df['Low']))
        firres, secondres, thirdres = get_min_3(df['High'], len(df['High']))

        update.message.reply_text(
            f"Supports For the Current Stock \n {firsup:.2f} \n {secondsup:.2f} \n {thirdsup:.2f} \n\n Resistance For the Current Stock \n {firres:.2f} \n {secondres:.2f} \n {thirdres:.2f}")


updater = bot.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(bot.CommandHandler("start", start))
disp.add_handler(bot.CommandHandler("user", user))
disp.add_handler(bot.CommandHandler("help", Help))
disp.add_handler(bot.CommandHandler("stock", getsupportandresist))


updater.start_polling()
updater.idle()
