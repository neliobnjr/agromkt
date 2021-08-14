import logging
import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import sleep
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
from datetime import datetime

logger  = logging.getLogger(__name__)


def start(update, context):
	##"send a message when the command /start is issued."
	
	update.message.reply_text('Hi!')



def echo(update, context):
	## echo the user message
	update.message.reply_text(update.message.text)

def error(update, context):
	## Log Errors caused by Updates
	logger.warning(f'Update {update} caused error {context.error}')

def main():
	#Start the bot
	updater = Updater("1960156435:AAHDijwe7rJZ_iSxuU84CP8fQMe2Vpkaahw", use_context=True)

	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(MessageHandler(Filters.text, echo))
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()

if __name__=='__main__':
	main()


