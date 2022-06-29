import telegram.ext as bot
import yfinance
import pandas as pd
from time import time,sleep
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



#function to get minimum no. 3
def get_min_3(df, lenght):
    firstmin = MAX
    secmin = MAX
    thirdmin = MAX
    n = lenght
    arr = df
    for i in range(0, n):

        if arr[i] < firstmin:
            thirdmin = secmin
            secmin = firstmin
            firstmin = arr[i]

        elif arr[i] < secmin:
            thirdmin = secmin
            secmin = arr[i]

        elif arr[i] < thirdmin:
            thirdmin = arr[i]

    firstmin = f"{firstmin:.2f}"
    secmin = f"{secmin:.2f}"
    thirdmin = f"{thirdmin:.2f}"
    return firstmin, secmin, thirdmin


# function to calculate the support and resistance
def findsupportandresistance(stock_name, days, interval):
    ticker_symbol = stock_name + nse_symbol
    ticker = yfinance.Ticker(ticker_symbol)

    if ticker.info['regularMarketPrice'] is None:
        return "Invalid Stock !!"

    elif interval not in lst_interval:
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

        return firsup, secondsup, thirdsup, firres, secondres, thirdres


# get the current price of the stock
def get_current_price(symbol):
    global nse_symbol
    ticker = yfinance.Ticker(symbol + nse_symbol)
    todays_data = ticker.history(period='1d')
    print(todays_data)
    price = f"{todays_data['Close'][0]:.2f}"
    print(f"Price {int(float(price))}")
    return int(float(price))

#to get the live price of stock all the time
def live_current_price(stock_name):
    i = 1
    while i==1:
        global nse_symbol
        ticker = yfinance.Ticker(stock_name + nse_symbol)
        todays_data = ticker.history(period='1m')
        price = f"{todays_data['Close'][0]:.2f}"
        print(f"Updated Price of Stock {int(float(price))}")
        return int(float(price))
        sleep(5)


# start command
def start(update, context):
    global is_bot_started
    if not is_bot_started:
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
    if not is_user_login:
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
            3. Price Alert System For the Stocks.

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

    firsup, secondsup, thirdsup, firres, secondres, thirdres = findsupportandresistance(stock_name, days, interval)
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
    firsup, secondsup, thirdsup, firres, secondres, thirdres = findsupportandresistance(stock_name, days, interval)
    if current_price < int(float(firsup)) and current_price < int(float(secondsup)) and current_price < int(
            float(thirdsup)):
        update.message.reply_text(f"BreakOut Done From Suport Side \n Current Price of Stock {current_price:.2f}")
    elif current_price > int(float(firres)) and current_price > int(float(secondres)) and current_price > int(
            float(thirdres)):
        update.message.reply_text(f"Breakout Done From Resistance Side \n Current Price of Stock {current_price:.2f}")
    else:
        update.message.reply_text(f"I will notify you  \n Current Price of Stock {current_price:.2f}")


# option for the stock
def choosefromhelp(update, context):
    user_option = context.args[0]
    if user_option == '1':
        update.message.reply_text("You Choose Support & Resistance")
        sleep(1)
        update.message.reply_text("""
            Rules To Follow

            Use /stock + stockname + days + interval

         """)
    elif user_option == '2':
        update.message.reply_text("You Choose breakout")
        sleep(1)
        update.message.reply_text("""
            Rules To Follow

            Use /breakout + stockname + days + interval
         """)
    elif user_option == '3':
        update.message.reply_text("System Activating...")
        sleep(1)
        update.message.reply_text("""
                    Rules To Follow

                    Use /pricealert + stockname + price
                 """)
    else:
        update.message.reply_text("Wrong Option Try Again !! ")


# handle the text message without the slash
def handlemessage(update, context):
    text = update.message.text
    update.message.reply_text("Invalid Command \n Use /help to know more.")


# function for creating the price alert system
def price_alert_system(update, context):
    global nse_symbol
    stock_name = context.args[0]
    price = context.args[1]
    ticker_symbol = stock_name + nse_symbol
    ticker = yfinance.Ticker(ticker_symbol)
    price = int(price)
    if ticker.info['regularMarketPrice'] is None:
        update.message.reply_text("Wrong Stock Name")
    elif  isinstance(price, int) == False :
        update.message.reply_text("Wrong Price Given")
    else :
        update.message.reply_text("Alert System Activated.")
        i = 1
        while i == 1:
            live_stock_price = live_current_price(stock_name)
            print(f"The value inside the variable  {live_stock_price}")
            if (price == live_stock_price) :
                j=1
                while j <= 5:
                    update.message.reply_text(f"Price Reached For Your Stock {stock_name} \n Current Price of Stock {live_stock_price}")
                    j+=1
                break
            else :
                sleep(5)




# for handling all the error related to the bot
def error(update, context):
    logging.error(f"Error Caused By {context.error}")

if __name__ == '__main__':
    updater = bot.Updater(TOKEN, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(bot.CommandHandler("start", start))
    disp.add_handler(bot.CommandHandler("user", user))
    disp.add_handler(bot.CommandHandler("help", Help))
    disp.add_handler(bot.CommandHandler("option", choosefromhelp))
    disp.add_handler(bot.CommandHandler("stock", getsupportandresist_ind))
    disp.add_handler(bot.CommandHandler("breakout", breakoutstock))
    disp.add_handler(bot.CommandHandler("pricealert", price_alert_system))
    disp.add_handler(bot.MessageHandler(bot.Filters.text, handlemessage))
    disp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
