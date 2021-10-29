import pickle

from dateparser import parse

from venue import Venue
from note import Note
from artist import Artist
from person import Person


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
                                       f"{str(self.venue)}"
        except AttributeError:
            date_artist_place_string = f"* {self.date} you saw {self.artist.name} at {str(self.venue)}"

        if self.persons:
            person_string = f"  You were there with "
            for i, person in enumerate(self.persons):
                if len(self.persons) == 1:
                    person_string += f"{person.first_name}."
                elif i == len(self.persons) - 2:
                    person_string += f"{person.first_name} "
                elif i == len(self.persons) - 1:
                    person_string += f"and {person.first_name}."
                else:
                    person_string += f"{person.first_name}, "

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
            return f"* {self.date.strftime('%Y-%m-%d')}: {self.artist.name}, {self.venue.name} "
        except AttributeError:
            return f"* {self.date}: {self.artist.name}, {self.venue.name} "


with open("concerts.bin", "rb") as old_concert_file:
    old_concerts = pickle.load(old_concert_file)


from concert import Concert


def convert():
    new_concerts = []
    for concert_obj in old_concerts:
        try:
            persons = [person.first_name for person in concert_obj.persons]
        except TypeError:
            persons = []
        new_concert = Concert(
            concert_obj.artist.name,
            (concert_obj.venue.name, concert_obj.venue.city, concert_obj.venue.country),
            concert_obj.date.strftime('%m/%d/%Y'),
            persons,
            concert_obj.note)
        new_concerts.append(new_concert)
        with open("new_concerts.bin", "wb") as new_concert_file:
            pickle.dump(new_concerts, new_concert_file)


def main():
    convert()
    with open("new_concerts.bin", "rb") as new_concert_file:
        new_concerts = pickle.load(new_concert_file)
    for concert in new_concerts:
        print(concert.get_concert_long_string())


if __name__ == '__main__':
    main()
