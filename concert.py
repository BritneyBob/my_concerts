from artist import Artist
from venue import Venue
from date import Date
from person import Person
from note import Note
from terminal_color import color_print


class Concert:
    def __init__(self, artist, venue, date, persons, note):
        self.artist = Artist(artist)
        self.venue = Venue(venue)
        self.date = Date(date)
        self.persons = []
        if persons[0].lower() != 'no':
            for person in persons:
                self.persons.append(Person(person))
        if note is not None:
            self.note = Note(note)

    def print_concert(self):
        color_print('blue', f"* {self.date.date} you saw {self.artist.name} at {self.venue.name} in {self.venue.city}, "
                            f"{self.venue.country}.")

        if len(self.persons) > 0:
            color_print('blue', f"  You were there together with ", end='')
            for i, person in enumerate(self.persons):
                if len(self.persons) == 1:
                    color_print('blue', f'{person.first_name}.', end='')
                elif i == len(self.persons) - 2:
                    color_print('blue', f'{person.first_name}', end=' ')
                elif i == len(self.persons) - 1:
                    color_print('blue', f'and {person.first_name}.', end='')
                else:
                    color_print('blue', f"{person.first_name}, ", end='')

        if self.note:
            if len(self.note.note) > 180:
                color_print('blue', f"\nNotes: {self.note.note[:180]}")
                color_print('blue', f"  {self.note.note[180:]}")
            else:
                color_print('blue', f"\n  Notes: {self.note.note}")
        print()
