from coins import *
import logging
import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import sleep
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
from datetime import datetime
from doge import *
logger  = logging.getLogger(__name__)


def start(update, context):
	##"send a message when the command /start is issued."

	update.message.reply_text('Hi!')


def getBtc(update, context):
	## Send a message when the commmand help is issued.
	b = bitcoin()
	result = f' O ultimo preco do BTC esta em {b}'
	update.message.reply_text(result)

def getEth(update, context):
	e = eth()
	result = f'O ultimo preco de ETH esta em {e}'
	update.message.reply_text(result)
def monitora(update,context):
    with open('crypto.csv', 'a') as f:
        f.write('time,btc,eth,dolC,dolT\n')
        while True:
            now = datetime.now()
            now = now.strftime('%H:%M:%S %d/%m/%Y')
            try:
                x = bitcoin()
                s = eth()
                d = btcDolar()
                r = xrp()
                c = chz()
                dogeBtc = doge('btc')
                dogeUsd = doge('usd')
                dogeBrl = doge('brl')
                dolar = getDollar()
                dolarC = dolar['dolarC']
                dolarT = dolar['dolarT']
                f.write(f'{now},{x},{d},{s},{dolarC},{dolarT}\n')
                situation = f'''
						Situacao:
							DOGE(BTC): {dogeBtc[0]},
							DOGE(BRL): {dogeBrl[0]},
							DOGE(Dollar): {dogeUsd[0]},
							CHZ(Real):{c},
							BTC(Real): {x},
							BTC(Dollar): {d},
							Dolar Turismo: {dolarT},
							Dolar Comercial: {dolarC},
							XRP(Real): {r},
							ETH: {s}'''
                update.message.reply_text(situation)
                
                sleep(300)
            except:
                update.message.reply_text('Situation offline.')
                sleep(300)
def echo(update, context):
	## echo the user message
	update.message.reply_text(update.message.text)

def error(update, context):
	## Log Errors caused by Updates
	logger.warning(f'Update {update} caused error {context.error}')

def main():
	#Start the bot
	updater = Updater("1452135026:AAEyBtC41tk3_hAmWLMOFZqIRaUMovDhSJs", use_context=True)

	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("bitcoin", getBtc))
	dp.add_handler(CommandHandler("eth", getEth))
	dp.add_handler(CommandHandler("monitora", monitora))
	dp.add_handler(MessageHandler(Filters.text, echo))
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()

if __name__=='__main__':
	main()


