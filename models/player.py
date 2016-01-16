__author__ = 'imozerov'


class Player:
    def __init__(self, telegram_id, name,
                 colour, number_of_guests):
        self.number_of_guests = number_of_guests
        self.colour = colour
        self.name = name
        self.telegram_id = telegram_id
