from artist import Artist
from venue import Venue
from date import Date
from person import Person
from terminal_color import color_print


class Concert:
    def __init__(self, artist, venue, date, persons):
        self.artist = Artist(artist)
        self.venue = Venue(venue)
        self.date = Date(date)
        self.persons = []
        if persons[0].lower() != 'no':
            for person in persons:
                self.persons.append(Person(person))

    def print_concert(self):
        color_print('blue', f"* {self.date.date} you saw {self.artist.name} at {self.venue.name} in {self.venue.city}, {self.venue.country}.")
        if len(self.persons) > 0:
            color_print('blue', f"  You were there together with ", end='')
            for i, person in enumerate(self.persons):
                if len(self.persons) == 1:
                    color_print('blue', f'{person.first_name}.', end='')
                elif i == len(self.persons) - 2:
                    color_print('blue', f'{person.first_name}', end=' ')
                elif i == len(self.persons) - 1:
                    color_print('blue', f'and {person.first_name}.')
                else:
                    color_print('blue', person.first_name, end=', ')
        print()
