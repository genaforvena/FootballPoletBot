# -*- coding: utf-8 -*-
import config
import telebot
import shelve
from models.match import Match
from models.player import Player
from utils.markup_utils import generate_plus_minus_markup

bot = telebot.TeleBot(config.token)

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
        markup = None
        if "да матч" in message.text or "да игра" in message.text:
            response = match.annotate()
            if player.telegram_id not in match.players.keys():
                markup = generate_plus_minus_markup()
        elif message.text == "+" or message.text == "Я +" or message.text == "я +" or message.text == "плюс":
            match.add_player(player)
            response = "Нас " + str(match.players_number())
            if match.players_number() == 10:
                send_message_to(match.players.values(), "Нас точно 10, играем")
        elif message.text == "-" or message.text == "Я -" or message.text == "я -" or message.text == "минус":
            match.remove_player(player)
            response = "("
            if match.players_number() < 10:
                send_message_to(match.players.values(), "Один -. Нас теперь " + str(match.players_number()))
        elif "мной +" in message.text:
            match.add_guests(player, 1)
            response = "Нас " + str(match.players_number())
            if match.players_number() == 10:
                send_message_to(match.players.values(), "Нас точно 10, играем")
        elif "мной -" in message.text:
            match.remove_guest(player)
            response = "((("
            if match.players_number() < 10:
                send_message_to(match.players.values(), "Один -. Нас теперь " + str(match.players_number()))
        elif "ы игра" in message.text:
            if match.players_number() >= 10:
                response = "Да \nНас " + str(match.players_number())
            else:
                response = "Нас пока " + str(match.players_number())
        elif "Создать матч" in message.text:
            match = Match("Полет", "Понедельник 20-30")
            store["match"] = match
            response = "Следующий матч: \n" + match.annotate() + "\n\nИдешь?"
            send_message_to(all_users.values(), response, generate_plus_minus_markup())
        elif "то ид" in message.text or "олько на" in message.text:
            response = "Нас " + str(match.players_number()) + "\nТочно идут: \n" + match.annotate_players()
        elif "Прив" in message.text or "Как дела?" in message.text:
            response = "Иди нахуй"
        elif "дрес" in message.text:
            response = "ул. Чаадаева, 20А"
        elif "то подписан" in message.text:
            response = "На уведомления подписаны:\n"
            for user in all_users.values():
                response += user.name + "\n"
        else:
            response = "Я понимаю команды:" \
                       "\nКогда матч?" \
                       "\nКакой адрес?" \
                       "\n+" \
                       "\n-" \
                       "\nСо мной +" \
                       "\nСо мной -" \
                       "\nКто идет?"
        store.sync()
    if markup is None:
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, response, reply_markup=markup)


def send_message_to(players, message, markup = None):
    for player in players:
        if markup is None:
            bot.send_message(player.telegram_id, message)
        else:
            bot.send_message(player.telegram_id, message, reply_markup=markup)

if __name__ == '__main__':
     bot.polling(none_stop=True)
