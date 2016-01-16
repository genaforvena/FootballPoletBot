__author__ = 'imozerov'

class Guest:
    def __init__(self, invited_by):
        self.invited_by = invited_by

    def __str__(self):
        return "Чувак от " + self.invited_by.name