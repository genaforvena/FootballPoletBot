from telebot import types

__author__ = 'imozerov'


def generate_plus_minus_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("+")
    markup.add("-")
    return markup

def generate_number_of_guests_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("0")
    markup.add("1")
    markup.add("2")
    markup.add("3")
    return markup