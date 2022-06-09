
import telegram.ext as bot

TOKEN = '5487092264:AAHcqAcf3q31Z0Dn35-o2FUfGpYQfYDdzvI'
is_bot_started = False
is_user_login = False

#start command
def start(update , context) :
    global is_bot_started
    if is_bot_started != True :
        update.message.reply_text("Enter Your Username : \n Use /user+username")
        is_bot_started = True
    else:
        update.message.reply_text("Already Executed")


#user command
def user(update , context):
    global is_user_login
    given_by_user = context.args[0]
    list_user = ['abc' , 'bad']
    if is_user_login != True:
        if given_by_user in list_user :
            update.message.reply_text("Welcome to the bot 😁 \n Use /help to know more about me 😊")
            is_user_login = True
        else :
            update.message.reply_text("Invalid User :( \n Try Again")
    else:
        update.message.reply_text("Command Already Executed")

#help command
def Help(update ,context):
        update.message.reply_text("""

                `OUR SERVICES`

            1. Find Support & Resistance For the Stock.
                || Rules ||
                || Use /stock + stockname(capital) + days + interval ||

            2. Find Breakout of the stock.

        """)




updater = bot.Updater(TOKEN , use_context=True)
disp = updater.dispatcher

disp.add_handler(bot.CommandHandler("start", start))
disp.add_handler(bot.CommandHandler("user", user))
disp.add_handler(bot.CommandHandler("help", Help))


updater.start_polling()
updater.idle()