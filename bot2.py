#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from datetime import datetime
import logging
import json
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

OPERATION, PHOTO, BIO = range(3)



def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Adicionar Produto', 'Remover Produto', 'Ver Lista']]
    with open('products/config/config2.json', 'r') as f:
        data = json.load(f)
    prod_id = datetime.now()
    prod_id = prod_id.strftime('%m%d%Y-%H%M%S')
    update.message.reply_text(
        'Bem-vindo ao sistema de gerenciamento de produtos Oferta Agrícola. '
        'Digite /cancel para cancelar a operação.\n\n'
        'O que gostaria de fazer?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Selecione a operação.'
        ),
    )

    return OPERATION


def operation(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    if update.message.text == 'Adicionar Produto':
        logger.info("Gender of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'I see! Please send me a photo of yourself, '
            'so I know what you look like, or send /skip if you don\'t want to.',
            reply_markup=ReplyKeyboardRemove(),
        )

        return PHOTO
    if update.message.text == 'Ver Lista':
        return BIO


def photo(prod_id, update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(f'products/{prod_id}.jpg')
    logger.info("Photo of %s: %s", user.first_name, f'{prod_id}.jpg')
    update.message.reply_text(
        'Ok! Agora Digite a descrição do produto.'
    )

    return BIO


def skip_photo(update: Update, context: CallbackContext) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'I bet you look great! Now, send me your location please, or send /skip.'
    )

    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("")
    
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            OPERATION: [MessageHandler(Filters.regex('^(Adicionar Produto|Remover Produto|Ver Lista)$'), operation)],
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    print(BIO)
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()