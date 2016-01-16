# -*- coding: utf-8 -*-
import types
import config
import telebot
import shelve
from models.match import Match
from models.player import Player
from utils.markup_utils import generate_plus_minus_markup

bot = telebot.TeleBot(config.token)


def getOrCreatePlayer(message, store):
    try:
        player = store[message.chat.id]
    except:
        player = Player(str(message.chat.id), message.chat.first_name + " " + message.chat.last_name)
    return player


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    response = "Что-то пошло не так"
    markup = None
    with shelve.open(config.shelve_file) as store:
        match = store["match"]
        if "да матч" in message.text:
            response = match.annotate()
            markup = generate_plus_minus_markup()
        elif message.text == "+":
            player = getOrCreatePlayer(message, store)
            match.add_player(player)
            response = "Нас " + str(match.players_number())
        elif message.text == "-":
            player = getOrCreatePlayer(message, store)
            match.remove_player(player)
            response = "("
        elif "мной +" in message.text:
            player = getOrCreatePlayer(message, store)
            match.add_guests(player, 1)
            response = "Нас " + str(match.players_number())
        elif "мной -" in message.text:
            player = getOrCreatePlayer(message, store)
            match.add_guests(player, 1)
            response = "Нас " + str(match.players_number())
        elif "аем?" in message.text:
            if match.players_number() >= 10:
                response = "Да \Нас " + str(match.players_number())
            else:
                response = "Нас пока" + str(match.players_number())
        elif "Создать матч" in message.text:
            store["match"] = Match("Полет", "Понедельник 20-30")
            response = "Создан матч: " + match.annotate()
        else:
            response = "Написать, какие команды есть."
        store.sync()
    if markup is None:
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, response, reply_markup=markup)

if __name__ == '__main__':
     bot.polling(none_stop=True)
