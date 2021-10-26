from artist import Artist
from venue import Venue
from dateparser import parse
from person import Person
from note import Note


class Concert:
    def __init__(self, artist, venue, date, persons, note):
        self.artist = Artist(artist)

        venue_name, city, country = venue
        self.venue = Venue(venue_name, city, country)

        self.date = parse(date)

        if len(persons) > 0:
            self.persons = [Person(person) for person in persons]
        else:
            self.persons = None

        self.note = Note(note) if note else ""

    def get_concert_long_string(self):
        concert_string = ''
        try:
            date_artist_place_string = f"* {self.date.strftime('%Y-%m-%d')} you saw {self.artist.name} at " \
                                       f"{self.venue.venue_string()}"
        except AttributeError:
            date_artist_place_string = f"* {self.date} you saw {self.artist.name} at {self.venue.venue_string()}"

        if self.persons:
            person_string = f"  You were there with "
            for i, person in enumerate(self.persons):
                if len(self.persons) == 1:
                    person_string += f'{person.first_name}.'
                elif i == len(self.persons) - 2:
                    person_string += f'{person.first_name} '
                elif i == len(self.persons) - 1:
                    person_string += f'and {person.first_name}.'
                else:
                    person_string += f"{person.first_name}, "

            concert_string += date_artist_place_string + '\n' + person_string
        else:
            concert_string += date_artist_place_string

        try:
            if self.note:
                concert_string += '\n' + self.note.note_string()
        except AttributeError:
            pass

        return concert_string

    def get_concert_summary(self):
        try:
            return f"* {self.date.strftime('%Y-%m-%d')}: {self.artist.name}, {self.venue.name} "
        except AttributeError:
            return f"* {self.date}: {self.artist.name}, {self.venue.name} "
