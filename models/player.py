__author__ = 'imozerov'


class Player:
    def __init__(self, telegram_id, name):
        self.name = name
        self.telegram_id = telegram_id

    def __str__(self):
        return self.name


