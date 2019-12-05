from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from knn.PI_V import get_results_for_id
import telegram
import logging
import os
import re

TOKEN='1047348604:AAHil1ytnjkxj_SBZgfGKl1tsmwpoHXPm6w'

logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

env = os.environ.get('ENV', 'development')

def get_anime_id(url):
    regex = re.compile('.*myanimelist\.net\/anime\/(\d+)')
    result = re.match(regex, url)
    if result is None:
        return 0
    return int(result[1])


try:
    def echo(bot, update):
        msg = update.message.text
        print(msg)
        if "help" in msg or "ajuda" in msg:
            response = bot.send_photo(chat_id=update.message.chat_id, photo='AgADAQADVqgxG8GdSEcp1xKxcYP6YrbrawYABAEAAwIAA20AA_2rAQABFgQ', parse_mode=telegram.ParseMode.HTML)
            resposta = "Me envie um link de um anime do MyAnimeList, tipo https://myanimelist.net/anime/450"
            bot.send_message(chat_id=update.message.chat_id, text=resposta, parse_mode=telegram.ParseMode.HTML)
            return
        id = get_anime_id(msg)
        print(id)
        if id < 1:
            resposta = "Perdão meu fã de loli, ou a url está errada ou não reconheço esse id :("
            bot.send_message(chat_id=update.message.chat_id, text=resposta, parse_mode=telegram.ParseMode.HTML)
            response = bot.send_photo(chat_id=update.message.chat_id, photo='AgADAQADVqgxG8GdSEcp1xKxcYP6YrbrawYABAEAAwIAA20AA_2rAQABFgQ', parse_mode=telegram.ParseMode.HTML)
            resposta = "Me envie um link de um anime do MyAnimeList, tipo https://myanimelist.net/anime/450"
            bot.send_message(chat_id=update.message.chat_id, text=resposta, parse_mode=telegram.ParseMode.HTML)
        else:
            recomendations = get_results_for_id(id)
            for rec in recomendations:
                response = "Tu vai curtir essa parada aqui: " + rec
                bot.send_message(chat_id=update.message.chat_id, text=response, parse_mode=telegram.ParseMode.HTML)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    if(env == 'production'):
        PORT = int(os.environ.get('PORT', '5000'))
        HEROKU_APP = os.environ.get('HEROKU_APP')
        logger.info("PORT: " + str(PORT))
        logger.info("HEROKU_APP: " + HEROKU_APP)
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://"+ HEROKU_APP +".herokuapp.com/" + TOKEN)
        updater.idle()
    else:
        updater.start_polling()
except Exception as e:
    print(e)
