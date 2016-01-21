# -*- coding: utf-8 -*-
import time
import config
import telebot
import shelve
from models.match import Match
from models.player import Player
from utils.markup_utils import generate_plus_minus_markup

bot = telebot.TeleBot(config.token)


def dispatch_message_and_respond(all_users, match, message, player, store):
    if "да матч" in message.text or "да игра" in message.text:
        response = match.annotate()
        if player.telegram_id not in match.players.keys():
            markup = generate_plus_minus_markup()
            bot.send_message(message.chat.id, response, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, response)

    elif message.text == "+" or message.text == "Я +" or message.text == "я +" or message.text == "плюс":
        match.add_player(player)
        send_message_to(match.players.values(), "Нас " + str(match.players_number()))

    elif message.text == "-" or message.text == "Я -" or message.text == "я -" or message.text == "минус":
        match.remove_player(player)
        response = "("
        bot.send_message(message.chat.id, response)
        if player.telegram_id in match.players.keys() and match.players_number() < 10:
            send_message_to(match.players.values(), "Один -. Нас теперь " + str(match.players_number()))

    elif "мной +" in message.text:
        match.add_guests(player, 1)
        send_message_to(match.players.values(), "Нас " + str(match.players_number()))

    elif "мной -" in message.text:
        match.remove_guest(player)
        response = "((("
        bot.send_message(message.chat.id, response)
        if match.players_number() < 10:
            send_message_to(match.players.values(), "Один -. Нас теперь " + str(match.players_number()))

    elif "ы игра" in message.text:
        if match.players_number() >= 10:
            response = "Да \nНас " + str(match.players_number())
        else:
            response = "Нас пока " + str(match.players_number())
        bot.send_message(message.chat.id, response)

    elif "Создать матч" in message.text:
        match = Match("Полет", "Понедельник 20-30")
        store["match"] = match
        response = "Следующий матч: \n" + match.annotate() + "\n\nИдешь?"
        send_message_to(all_users.values(), response, generate_plus_minus_markup())

        bot.send_message(message.chat.id, response)

    elif "то ид" in message.text or "олько на" in message.text:
        response = "Нас " + str(match.players_number()) + "\nТочно идут: \n" + match.annotate_players()
        bot.send_message(message.chat.id, response)

    elif "Прив" in message.text or "Как дела?" in message.text:
        response = "Иди нахуй"
        bot.send_message(message.chat.id, response)

    elif "Позвать всех" == message.text:
        response = "Ок. Зову всех, кто пока не поставил + на матч."
        bot.send_message(message.chat.id, response)

        broadcast = "Следующий матч: \n" + match.annotate() + "\n\nИдешь?"
        send_message_to(all_users.values(), broadcast, generate_plus_minus_markup())

    elif "дрес" in message.text:
        response = "ул. Чаадаева, 20А"
        bot.send_message(message.chat.id, response)

    elif "дали меня" in message.text:
        try:
            del all_users[player.telegram_id]
            response = "Больше никаких уведомлений на твой номер."
            if player.telegram_id in match.players.keys():
                match.remove_player(player)
                if match.players_number() < 10:
                    send_message_to(match.players.values(), "Один -. Нас теперь " + str(match.players_number()))
        except:
            # i know that this is bad but
            pass
        bot.send_message(message.chat.id, response)

    elif "то подписан" in message.text:
        response = "На уведомления подписаны:\n"
        for user in all_users.values():
            response += user.name + "\n"
        bot.send_message(message.chat.id, response)

    else:
        response = "Я понимаю команды:" \
                   "\nКогда матч?" \
                   "\nКакой адрес?" \
                   "\n+" \
                   "\n-" \
                   "\nСо мной +" \
                   "\nСо мной -" \
                   "\nКто идет?" \
                   "\nУдали меня из списка уведомлений"
        bot.send_message(message.chat.id, response)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    with shelve.open(config.shelve_file, writeback=True) as store:
        try:
            match = store["match"]
        except:
            pass
        try:
            all_users = store["users"]
        except:
            all_users = {}

        player = Player(message.chat.id, message.chat.first_name + " " + message.chat.last_name)
        all_users[player.telegram_id] = player
        store["users"] = all_users

        dispatch_message_and_respond(all_users, match, message, player, store)
        store.sync()


def send_message_to(players, message, markup = None):
    for player in players:
        if markup is None:
            bot.send_message(player.telegram_id, message)
        else:
            bot.send_message(player.telegram_id, message, reply_markup=markup)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(timeout=20, none_stop=True)
        except:
            pass
        time.sleep(60)
