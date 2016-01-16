from models.guest import Guest

__author__ = 'imozerov'


class Match:
    def __init__(self, place, time):
        self.place = place
        self.time = time
        self.players = set()
        self.guests = list()

    def add_player(self, player):
        self.players.add(player)

    def remove_player(self, player):
        try:
            self.players.remove(player)
        except:
            pass

    def add_guests(self, invited_player, guests_number):
        for i in range(guests_number):
            self.guests.append(Guest(invited_player))

    def remove_guest(self, invited_player):
        self.guests.remove(Guest(invited_player))

    def will_take_place_as_known_for_now(self):
        return self.players_number() > 10

    def players_number(self):
        known_players_number = len(self.players)
        guests_number = len(self.guests)
        return known_players_number + guests_number

    def annotate_players(self):
        players_str = "\n".join(map(lambda x: x.name, self.players))
        guests_str = "\n".join(map(str, self.guests))
        return players_str + guests_str

    def annotate(self):
        return "Место: " + self.place + "\n Время: " + self.time \
               + "\nНас пока: " + str(self.players_number())