from dateparser import parse

from note import Note
from venue import Venue


class Concert:
    def __init__(self, artist, venue, date, persons, note):
        self.artist = artist

        venue_name, city, country = venue
        self.venue = Venue(venue_name, city, country)

        self.date = parse(date)

        if len(persons) > 0:
            self.persons = persons
        else:
            self.persons = None

        self.note = Note(note) if note else ""

    def __eq__(self, other):
        return self.artist == other.artist and \
               self.venue == other.venue and \
               self.date.strftime("%Y-%m-%d") == other.date.strftime("%Y-%m-%d") and \
               self.persons == other.persons and \
               self.note == other.note

    def get_concert_long_string(self):
        concert_string = ""
        try:
            date_artist_place_string = f"* {self.date.strftime('%Y-%m-%d')} you saw {self.artist} at " \
                                       f"{str(self.venue)}"
        except AttributeError:
            date_artist_place_string = f"* {self.date} you saw {self.artist} at {str(self.venue)}"

        if self.persons:
            person_string = f"  You were there with "
            for i, person in enumerate(self.persons):
                if len(self.persons) == 1:
                    person_string += f"{person}."
                elif i == len(self.persons) - 2:
                    person_string += f"{person} "
                elif i == len(self.persons) - 1:
                    person_string += f"and {person}."
                else:
                    person_string += f"{person}, "

            concert_string += date_artist_place_string + "\n" + person_string
        else:
            concert_string += date_artist_place_string

        try:
            if self.note:
                concert_string += "\n" + str(self.note)
        except AttributeError:
            pass

        return concert_string

    def __str__(self):
        try:
            return f"* {self.date.strftime('%Y-%m-%d')}: {self.artist}, {self.venue.name} "
        except AttributeError:
            return f"* {self.date}: {self.artist}, {self.venue.name} "
