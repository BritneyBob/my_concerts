from artist import Artist
from venue import Venue
from dateparser import parse
from person import Person
from note import Note
from terminal_color import color_print


class Concert:
    def __init__(self, artist, venue, date, persons, note):
        self.artist = Artist(artist)

        if isinstance(venue, str):
            self.venue = Venue(venue)
        elif isinstance(venue, tuple):
            venue_name, city, country = venue
            self.venue = Venue(venue_name, city, country)

        self.date = parse(date)

        self.persons = []
        if persons[0].lower() != 'no':
            for person in persons:
                self.persons.append(Person(person))

        self.note = Note(note)

    def print_concert(self):
        color_print('blue', f"* {self.date.strftime('%Y-%m-%d')} you saw {self.artist.name} at {self.venue.name} in {self.venue.city}, "
                            f"{self.venue.country}.")

        if len(self.persons) > 0:
            color_print('blue', f"  You were there with ", end='')
            for i, person in enumerate(self.persons):
                if len(self.persons) == 1:
                    color_print('blue', f'{person.first_name}.', end='')
                elif i == len(self.persons) - 2:
                    color_print('blue', f'{person.first_name}', end=' ')
                elif i == len(self.persons) - 1:
                    color_print('blue', f'and {person.first_name}.', end='')
                else:
                    color_print('blue', f"{person.first_name}, ", end='')

        if len(self.note.note) > 0:
            if len(self.note.note) > 165:
                color_print('cyan', f"\n  Notes: {self.note.note[:165]}")
                color_print('cyan', f"  {self.note.note[165:]}")
            else:
                color_print('cyan', f"\n  Notes: {self.note.note}")
        print()

    def return_concert_string(self):
        concert_string = ''
        date_artist_place_string = f"* {self.date.strftime('%Y-%m-%d')} you saw {self.artist.name} at {self.venue.name} " \
                                   f"in {self.venue.city}, {self.venue.country}.\n"

        if len(self.persons) > 0:
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

        concert_string += date_artist_place_string + person_string

        if len(self.note.note) > 0:
            if len(self.note.note) > 165:
                note_string = f"\n  Notes: {self.note.note[:80]}\n"
                note_string += f"  {self.note.note[80:]}"
            else:
                note_string = f"\n  Notes: {self.note.note}"
            concert_string += note_string

        return concert_string

    def print_concert_summary(self):
        return f"* {self.date.strftime('%Y-%m-%d')}: {self.artist.name}, {self.venue.name} "
