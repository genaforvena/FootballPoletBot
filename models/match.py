from models.guest import Guest

__author__ = 'imozerov'


class Match:
    def __init__(self, place, time):
        self.place = place
        self.time = time
        self.players = {}
        self.guests = list()

    def add_player(self, player):
        self.players[player.telegram_id] = player

    def remove_player(self, player):
        try:
            self.players.pop(player.telegram_id)
        except:
            pass

    def add_guests(self, invited_player, guests_number):
        for i in range(guests_number):
            self.guests.append(Guest(invited_player))

    def remove_guest(self, invited_player):
        guest_to_remove = None
        for guest in self.guests:
            if guest.invited_by.telegram_id == invited_player.telegram_id:
                guest_to_remove = guest
                break
        if guest_to_remove is not None:
            self.guests.remove(guest_to_remove)

    def will_take_place_as_known_for_now(self):
        return self.players_number() > 10

    def players_number(self):
        known_players_number = len(self.players)
        guests_number = len(self.guests)
        return known_players_number + guests_number

    def annotate_players(self):
        players_str = ""
        guests_str = ""

        j = 0
        for i, player in self.players.items():
            j += 1
            players_str += str(j) + ") " + player.name + "\n"
        for guest in self.guests:
            j += 1
            guests_str += str(j) + ") " + str(guest) + "\n"
        return players_str + guests_str

    def annotate(self):
        return self.place + ". " + self.time \
               + "\nНас пока: " + str(self.players_number())