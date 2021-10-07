from artist import Artist
from arena import Arena
from date import Date
from person import Person


class Concert:
    def __init__(self, artist, arena, date, person):
        self.name_artist = Artist(artist)
        self.name_arena = Arena(arena)
        self.date = Date(date)
        if person.lower() == 'no':
            self.person = None
        else:
            self.person = Person(person)

