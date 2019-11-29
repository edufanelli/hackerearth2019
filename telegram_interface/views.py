from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from ibm_watson_interface.views import ask_watson
import os  
import signal  
import sys  

#References:
#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API
#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! My name is PAM and I am glad to be here to help. How can I assist you?")

def non_command(update, context):
    #Echo:
    #context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    watson_response = ask_watson(update.message.text)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=watson_response['output']['text'][0])

def start_bot():
    print('Starting Telegram Bot...')
    updater = Updater(token='1014628280:AAH6ho-7UizwyZavgyu9x6bjSxZqTKzmbWM', use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    #handlers
    start_handler = CommandHandler('start', start)

    non_command_handler = MessageHandler(Filters.text, non_command) #always last
    dispatcher.add_handler(start_handler)
    
    dispatcher.add_handler(non_command_handler) #always last

    #start!
    updater.start_polling()
    return updater

def stop_bot():
    global updater
    updater.stop()
    #updater.idle()

#updater = start_bot()

def my_signal_handler(*args):  
    if os.environ.get('RUN_MAIN') == 'true':  
        print('Stopping Telegram Bot...')  
        stop_bot()
    sys.exit(0) 

signal.signal(signal.SIGINT, my_signal_handler)  