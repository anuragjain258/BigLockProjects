import telegram.ext as bot
import yfinance
import pandas as pd
import numpy as np
import mplfinance
import time
import logging
from datetime import datetime, timedelta

TOKEN = '5487092264:AAHcqAcf3q31Z0Dn35-o2FUfGpYQfYDdzvI'
is_bot_started = False
is_user_login = False
MAX = 100000
nse_symbol = ".NS"
is_breakout_started = False
user_option = 0

lst_interval = ['1m', '2m', '5m', '15m', '30m', '60m',
                '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']


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

    firstmin = f"{firstmin:.2f}"
    secmin = f"{secmin:.2f}"
    thirdmin = f"{thirdmin:.2f}"
    return firstmin, secmin, thirdmin

#function to calculate the support and resistance
def findsupportandresistance(stock_name , days , interval) :
    ticker_symbol = stock_name + nse_symbol
    ticker = yfinance.Ticker(ticker_symbol)

    if (ticker.info['regularMarketPrice'] == None):
        return "Invalid Stock !!"

    elif (interval not in lst_interval):
        return f"Invalid Interval!! \n Valid Interval are {lst_interval}"
    else:
        start_date = datetime.now() - \
                     timedelta(days=int(days))
        end_date = datetime.now()

        df = ticker.history(interval=interval, start=start_date, end=end_date)

        df['Date'] = pd.to_datetime(df.index)
        # [12 ,10 ,13,26] [10,12,13,26]
        # df['Date'] = df['Date'].apply(mpl_dates.date2num)
        df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

        firsup, secondsup, thirdsup = get_min_3(df['Low'], len(df['Low']))
        firres, secondres, thirdres = get_min_3(df['High'], len(df['High']))

        print(f"Support {firsup}")

        return firsup , secondsup,thirdsup ,firres , secondres , thirdres


# get the current price of the stock
def get_current_price(symbol):
    global nse_symbol
    ticker = yfinance.Ticker(symbol+nse_symbol)
    todays_data = ticker.history(period='1d')
    print(todays_data)
    price = f"{todays_data['Close'][0]:.2f}"
    print(f"Price {int(float(price))}")
    return int(float(price))


# start command
def start(update, context):
    global is_bot_started
    if is_bot_started != True:
        update.message.reply_text(
            "Welcome to the bot 😁 \n Use /help to know more about me 😊")
        is_bot_started = True
    else:
        update.message.reply_text("Already Executed")


# user command
def user(update, context):
    global is_user_login
    given_by_user = context.args[0]
    list_user = ['chetan', 'nithin', 'harvinder']
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
            2. Find Breakout of the stock.

            Use /option with your choice number
        """)


# taking the min 3 support ans resistance



# invalid stock - faltu name , nse belong
#                             .ns
# getting the support and resistance for the indian stock
def getsupportandresist_ind(update, context):
    global nse_symbol
    stock_name = context.args[0]
    days = context.args[1]
    interval = context.args[2]
    global lst_interval

    firsup , secondsup , thirdsup , firres , secondres , thirdres = findsupportandresistance(stock_name ,days , interval)
    update.message.reply_text(
                f"Supports For the Current Stock \n {firsup} \n {secondsup} \n {thirdsup} \n\n Resistance For the Current Stock \n {firres} \n {secondres} \n {thirdres}")


# get the breakout for the stock
def breakoutstock(update, context):
    global nse_symbol, firsup, secondsup, thirdsup, firres, secondres, thirdres
    stock_name = context.args[0]
    days = context.args[1]
    interval = context.args[2]
    global lst_interval
    current_price = get_current_price(stock_name)
    firsup , secondsup , thirdsup , firres, secondres ,thirdres = findsupportandresistance(stock_name , days , interval)
    if current_price < int(float(firsup)) and current_price < int(float(secondsup)) and current_price < int(float(thirdsup)):
        update.message.reply_text(f"BreakOut Done From Suport Side \n Current Price of Stock {current_price:.2f}")
    elif current_price > int(float(firres)) and current_price > int(float(secondres)) and current_price > int(float(thirdres)):
        update.message.reply_text(f"Breakout Done From Resistance Side \n Current Price of Stock {current_price:.2f}")
    else:
        update.message.reply_text(f"I will notify you  \n Current Price of Stock {current_price:.2f}")


# option for the stock
def choosefromhelp(update, context):
    user_option = context.args[0]
    if user_option == '1':
        update.message.reply_text("You Choose Support & Resistance")
        time.sleep(1)
        update.message.reply_text("""
            Rules To Follow
            
            Use /stock + stockname + days + interval

         """)
    elif user_option == '2':
        update.message.reply_text("You Choose breakout")
        time.sleep(1)
        update.message.reply_text("""
            Rules To Follow

            Use /option + stockname + days + interval
         """)

    else:
        update.message.reply_text("Wrong Option Try Again !! ")


# handle the text message without the slash
def handlemessage(update, context):
    text = update.message.text
    """if text == "start" or text == "Start":
        start(update, context)
    elif text == "help" or text == "Help":
        Help(update, context)
    elif text == "1" :
        user_option = 1
        time.sleep(1)
        choosefromhelp(update , context)
    elif text == "2" :
        user_option = 2
        time.sleep(1)
        choosefromhelp(update , context)
    elif text == "stock" :
        update.message.reply_text("Enter the Stock Name !")
        stock_name = update.message.text
        time.sleep(2)
        update.message.reply_text("Your stock name is ")"""

    update.message.reply_text("Invalid Command \n Use /help to know more.")


# for handling all the error related to the bot
def error(update, context):
    logging.error(f"Error Caused By {context.error}")


updater = bot.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(bot.CommandHandler("start", start))
disp.add_handler(bot.CommandHandler("user", user))
disp.add_handler(bot.CommandHandler("help", Help))
disp.add_handler(bot.CommandHandler("option", choosefromhelp))
disp.add_handler(bot.CommandHandler("stock", getsupportandresist_ind))
disp.add_handler(bot.CommandHandler("breakout", breakoutstock))
disp.add_handler(bot.MessageHandler(bot.Filters.text, handlemessage))
disp.add_error_handler(error)

updater.start_polling()
updater.idle()
