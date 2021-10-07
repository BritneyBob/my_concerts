from artist import Artist
from arena import Arena
from date import Date
from person import Person


class Concert:
    def __init__(self, artist, arena, date, person):
        self.artist = Artist(artist)
        self.arena = Arena(arena)
        self.date = Date(date)
        if person.lower() == 'no':
            self.person = None
        else:
            self.person = Person(person)

    def print_concert(self):
        print(f"{self.date.date} you saw {self.artist.name} at {self.arena.name}")
        if self.person:
            print(f"You were there together with {self.person.first_name}")



