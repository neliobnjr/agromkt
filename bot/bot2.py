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
from keys.telekey import teleKey
from datetime import datetime
import logging
import os
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

OPERATION, PHOTO, PRODNOME, LISTA, EDITAR, REMOVER, VENDNOME, VENDPHONE, PHOTO2, PHOTO3= range(10)



def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Adicionar Produto', 'Ver Lista']]
    with open('../products/config/config2.json', 'r') as f:
        data = json.load(f)
    global prod_id
    prod_id = datetime.now()
    prod_id = prod_id.strftime('%m%d%Y-%H%M%S')
    update.message.reply_text(
        'Bem-vindo ao sistema de gerenciamento de produtos Oferta Agrícola. '
        'Digite /cancela para cancelar a operação.\n\n'
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
        logger.info("Action of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            f'OK! Agora me envie 3 fotos do produto que quer adicionar. Caso tenha apenas 1, utilize a mesma. O id do produto para referência é: {prod_id}, '
            'Então poderei adicionar no site!',
            reply_markup=ReplyKeyboardRemove(),
        )

        return PHOTO
    elif update.message.text == "Ver Lista":
        logger.info("Gender of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'Ok. aqui está a lista de produtos que estão postados na página, '
            ,
            reply_markup=ReplyKeyboardRemove(),
        )
        with open('../products/config/config2.json', 'r') as f:
            global data
            data = json.load(f)
            data = data['features']
            for i in data:
                update.message.reply_text(
                f"""Produto: {i['product']},\nVendedor Responsável: {i['vendedor_nome']},\nPhone do Vendedor: {i['vendedor_phone']}"""
            )
        reply_keyboard = [['Remover Produto', '/cancela']]
        update.message.reply_text(
            'O que gostaria de fazer?'
            ,
            reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Selecione a operação.'
        ))

        return LISTA


def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(f'../products/{prod_id}-1.jpg')
    logger.info("Photo of %s: %s", user.first_name, f'{prod_id}-1.jpg')
    update.message.reply_text(
        'Ok! Agora Me envie uma segunda foto. Caso tenha apenas 1 imagem do produto, use a mesma...'
    )

    return PHOTO2

def photo2(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(f'../products/{prod_id}-2.jpg')
    logger.info("Photo of %s: %s", user.first_name, f'{prod_id}-2.jpg')
    update.message.reply_text(
        'Beleza! Agora me envie mais uma foto para termos 3 fotos, caso tenha apenas 1 utilize a mesma.'
    )

    return PHOTO3

def photo3(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(f'../products/{prod_id}-3.jpg')
    logger.info("Photo of %s: %s", user.first_name, f'{prod_id}-3.jpg')
    update.message.reply_text(
        'Ok! Agora Digite o nome do produto.'
    )

    return PRODNOME

def lista(update: Update, context: CallbackContext) -> int:
    """Mostra a lista de produtos"""
    user = update.message.from_user
    logger.info("Photo of %s: %s", user.first_name, f'{prod_id}.jpg')
    if update.message.text == 'Remover Produto':
        logger.info("Reply of %s: %s", user.first_name, update.message.text)
        reply_keyboard = [[]]
        for i in data:
            prodName = i['product']
            reply_keyboard[0].append(prodName)
        reply_keyboard[0].append('/cancela')
        update.message.reply_text(
            'Ok! Escolha o produto que quer editar, '
            ,
            reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Selecione a operação.'),
        )
        return REMOVER

def remover(update: Update, context: CallbackContext) -> int:
    """REMOVE PRODUTO"""
    user = update.message.from_user
    logger.info("Photo of %s: %s", user.first_name, f'{prod_id}.jpg')
    toRemove = update.message.text
    logger.info("Reply of %s: %s", user.first_name, update.message.text)
    with open('../products/config/config2.json', 'r') as d:
        dataRem = json.load(d)
        dataRem = dataRem['features']
        for i in dataRem:
            if i['product'] == toRemove:
                try:
                    filename1 = i['photo_location1']
                    filename2 = i['photo_location2']
                    filename3 = i['photo_location3']
                    os.remove(f'../{filename1}')
                    os.remove(f'../{filename2}')
                    os.remove(f'../{filename3}')
                    dataRem.remove(i)
                except:
                    dataRem.remove(i)
        dataFull = {
                    "type": "FeatureCollection",
                    "features": dataRem
                    }
        with open('../products/config/config2.json','w') as s:
            s.write(json.dumps(dataFull, indent=4))
        update.message.reply_text(
        f'Pronto! O produto: {toRemove} foi removido com sucesso!')
    os.system('py updater.py')
    return ConversationHandler.END

def skip_photo(update: Update, context: CallbackContext) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'I bet you look great! Now, send me your location please, or send /skip.'
    )

    return PRODNOME
##AQUI COMECA A ADICAO DE PRODUTOS
## Here is where we end the talk and stores the json config file.
def prodNome(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    global prod_nome
    prod_nome = update.message.text
    user = update.message.from_user
    logger.info("Product Name %s: %s", user.first_name, update.message.text)
    update.message.reply_text(f'Obrigado! o produto {prod_nome} foi adicionado com sucesso.')
    update.message.reply_text(f'Agora digite alguma informacao extra sobre o produto: ')
    return VENDNOME

def vendNome(update: Update, context: CallbackContext) -> int:
    """Armazena globalmente o nome do vendedor"""
    global vend_nome
    vend_nome = update.message.text
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(f'Obrigado! A descricao {vend_nome} foi adicionada com sucesso.')
    update.message.reply_text(f'Agora me diga o fone(zap) do Vendedor responsável pelo produto. Por favor, digite de acordo com o modelo ex: 5534999991234')
    return VENDPHONE

def vendPhone(update: Update, context: CallbackContext) -> int:
    """Armazena o phone do vendedor"""
    global vend_phone
    vend_phone = update.message.text
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(f'Obrigado! o Phone do Vendedor rasponsável é {vend_phone} foi adicionado com sucesso. E seu produto foi registrado. Digite /menu para uma nova operacao.')
    with open('../products/config/config2.json', 'r') as g:
        dataG = json.load(g)
        dataG = dataG['features']
        dataProdG = {
                    "product": prod_nome,
                    "ID": prod_id,
                    "photo_location1": f"products/{prod_id}-1.jpg",
                    "photo_location2": f"products/{prod_id}-2.jpg",
                    "photo_location3": f"products/{prod_id}-3.jpg",
                    "vendedor_phone": vend_phone,
                    "vendedor_nome": vend_nome
                    }
        dataG.append(dataProdG)
        dataFull = {
                    "type": "FeatureCollection",
                    "features": dataG
                    }
        with open('../products/config/config2.json', 'w') as x:
            x.write(json.dumps(dataFull, indent=4))
    os.system('py updater.py')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Ok! Operação Cancelada. digite /menu para recomecar', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(teleKey)
    
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('menu', start)],
        states={
            OPERATION: [MessageHandler(Filters.regex('^(Adicionar Produto|Ver Lista)$'), operation)],
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            PHOTO2:[MessageHandler(Filters.photo, photo2), CommandHandler('skip', skip_photo)],
            PHOTO3:[MessageHandler(Filters.photo, photo3), CommandHandler('skip', skip_photo)],
            PRODNOME: [MessageHandler(Filters.text & ~Filters.command, prodNome)],
            LISTA: [MessageHandler(Filters.text & ~Filters.command, lista)],
            REMOVER: [MessageHandler(Filters.text & ~Filters.command, remover)],
            VENDNOME: [MessageHandler(Filters.text & ~Filters.command, vendNome)],
            VENDPHONE: [MessageHandler(Filters.text & ~Filters.command, vendPhone)]
        },
        fallbacks=[CommandHandler('cancela', cancel)],
    )
    
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

    #start checking what is going on with the session