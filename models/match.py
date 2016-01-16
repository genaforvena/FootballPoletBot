__author__ = 'imozerov'


class Match:
    def __init__(self, place, time):
        self.place = place
        self.time = time
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def will_take_place_as_known_for_now(self):
        return self.players_number() > 10

    def players_number(self):
        known_players_number = len(self.players)
        guests_number = 0
        for player in self.players:
            guests_number += player.number_of_guests
        return known_players_number + guests_number