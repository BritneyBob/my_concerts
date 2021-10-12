import pickle
import random
from datetime import datetime
from os.path import exists
from concert import Concert
from terminal_color import color_print


class Menu:
    def __init__(self):
        self.running = True
        if exists('concerts.bin'):
            self.concerts_list = self.get_saved_concerts()
        else:
            self.concerts_list = []

    def run(self):
        color_print('cyan', f"Welcome! My Concerts helps you remember the concerts you have been to.\n")
        if len(self.concerts_list) > 0:
            self.print_concert_prev_year_same_month()
        while self.running:
            self.display_menu()

    def get_saved_concerts(self):
        try:
            with open('concerts.bin', 'rb') as concerts_file:
                x = pickle.load(concerts_file)
                return x
        except EOFError:
            return []

    def print_concert_prev_year_same_month(self):
        current_month = datetime.now().month
        concerts_this_month_prev_years = []

        for concert in self.concerts_list:
            if current_month == concert.date.month:
                concerts_this_month_prev_years.append(concert)

        if len(concerts_this_month_prev_years) == 0:
            return None

        concert_to_remind_of = concerts_this_month_prev_years[random.randrange(len(concerts_this_month_prev_years))]
        years = datetime.now().year - concert_to_remind_of.date.year
        if years == 0:
            color_print('magenta', f'RECENTLY...')
        else:
            color_print('magenta', f'{years} YEARS AGO...')
        concert_to_remind_of.print_concert()

    def display_menu(self):
        color_print('cyan', f"\nMAIN MENU")
        color_print('magenta', f"1. Add a new concert to your memory")
        color_print('green', f"2. Search for one or more concerts")
        color_print('magenta', f"3. Be reminded of a random concert")
        color_print('green', f"4. Be reminded of all concerts you have been to")
        color_print('magenta', f"5. Be reminded of all artists you have seen")
        color_print('green', f"6. Be reminded of all venues you have been to concerts in")
        color_print('magenta', f"7. Be reminded of all persons you have been to concerts with")
        color_print('green', f"8. Remove a concert from your memory")
        color_print('magenta', f"9. Change facts about a concert in your memory")
        choice = input("What would you like to do (1-9)?: ")
        print()
        match choice:
            case '1':
                self.add_concert()
            case '2':
                self.search_menu()
            case '3':
                self.concerts_list[random.randrange(len(self.concerts_list))].print_concert()
            case '4':
                color_print('magenta', f"ALL CONCERTS YOU REMEMBER")
                for concert in sorted(self.concerts_list, key=lambda c: c.date.date):
                    concert.print_concert()
            case '5':
                color_print('magenta', f"ARTISTS YOU HAVE SEEN")
                all_artists = []
                for concert in self.concerts_list:
                    all_artists.append(concert.artist.name)
                for artist in sorted(list(set(all_artists)), key=str.casefold):
                    color_print('blue', f'* {artist}')
            case '6':
                color_print('magenta', f"VENUES YOU HAVE SEEN CONCERTS IN")
                all_venues = []
                for concert in self.concerts_list:
                    all_venues.append(concert.venue.name)
                for artist in sorted(list(set(all_venues))):
                    color_print('blue', f'* {artist}')
            case '7':
                color_print('magenta', f"PEOPLE YOU HAVE BEEN TO CONCERTS WITH")
                all_persons = []
                for concert in self.concerts_list:
                    for person in concert.persons:
                        all_persons.append(person.first_name)
                for person in sorted(list(set(all_persons))):
                    color_print('blue', f'* {person}')
            case '8':
                pass
            case '9':
                pass
            case 'quit':
                self.running = False
            case _:
                color_print('red', f"Please enter a choice 1-7")

    def search_menu(self):
        color_print('cyan', f"SEARCH MENU")
        color_print('magenta', f"1. Artist")
        color_print('green', f"2. Venue")
        color_print('magenta', f"3. Date")
        color_print('green', f"4. Person")
        choice = int(input("What would you like search for (1-4)?: "))
        print()
        match choice:
            case 1:
                self.search_artist()
            case 2:
                self.search_venue()
            case 3:
                self.search_date()
            case 4:
                self.search_person()
            case _: color_print('red', f"Please enter a digit 1-4")

    # def search(self, search_string):
    #     found_concerts = []
    #     for concert in self.concerts_list:
    #         if search_string == concert.artist.name:
    #             found_concerts.append(concert)
    #     if len(found_concerts) > 0:
    #         for concert in found_concerts:
    #             concert.print_concert()
    #     else:
    #         print((f"Unfortunately you have no recollection of a concert with the artist {search_string}. If you "
    #                f"have gotten a new memory you can add it by choosing 1 in the main menu.")

    def search_artist(self):
        artist = input("Please enter the name of an artist: ")
        found_concerts = []
        for concert in self.concerts_list:
            if artist == concert.artist.name:
                found_concerts.append(concert)
        if len(found_concerts) > 0:
            for concert in sorted(self.found_concerts, key=lambda c: c.date.date):
                concert.print_concert()
        else:
            color_print('red', f"Unfortunately you have no recollection of a concert with the artist {artist}.")
            color_print('red', f"If you have gotten a new memory you can add it by choosing 1 in the main menu.")

    def search_venue(self):
        venue = input("Please enter the name of a venue: ")
        found_concerts = []
        for concert in self.concerts_list:
            if venue == concert.venue.name.lower():
                found_concerts.append(concert)
        if len(found_concerts) > 0:
            for concert in sorted(self.found_concerts, key=lambda c: c.date.date):
                concert.print_concert()
        else:
            color_print('red', f"Unfortunately you have no recollection of a concert at the venue {venue}.")
            color_print('red', f"If you have gotten a new memory you can add it by choosing 1 in the main menu.")

    def search_date(self):
        date = input("Please enter a date: ")
        found_concerts = []
        for concert in self.concerts_list:
            if date == concert.date.date:
                found_concerts.append(concert)
        if len(found_concerts) > 0:
            for concert in sorted(self.found_concerts, key=lambda c: c.date.date):
                concert.print_concert()
        else:
            color_print('red', f"Unfortunately you have no recollection of a concert on the date {date}.")
            color_print('red', f"If you have gotten a new memory you can add it by choosing 1 in the main menu.")

    def search_person(self):
        person = input("Please enter the name of a person: ")
        found_concerts = []
        for concert in self.concerts_list:
            for saved_person in concert.persons:
                if person == saved_person.first_name:
                    found_concerts.append(concert)
        if len(found_concerts) > 0:
            for concert in sorted(self.found_concerts, key=lambda c: c.date.date):
                concert.print_concert()
        else:
            color_print('red', f"Unfortunately you have no recollection of a concert that you went to with someone "
                               f"called {person}.")
            color_print('red', f"If you have gotten a new memory you can add it by choosing 1 in the main menu.")

    def add_concert(self):
        artist = input("What is the name of the artist?: ")
        venue_name = input("What is the name of the venue?: ")
        is_default_location = input(f"Is {venue_name} located in Gothenburg, Sweden? ")
        if is_default_location.lower() == 'no':
            city = input(f"In what city is {venue_name} located?: ")
            country = input(f"In what country is {city} located?: ")
            venue = (venue_name, city, country)
        elif is_default_location.lower() == 'yes':
            venue = venue_name
        date = input("What date was the concert (yy/mm/dd)?: ")
        persons = input("Did you go with someone to the concert? If yes, please enter one or more names: ").split()
        is_note = input("Would you like to add a note about this concert?")
        if is_note.lower() == 'yes':
            note = input("Please enter your notes about the concert: ")
        elif is_note.lower() == 'no':
            note = None
        new_concert = Concert(artist, venue, date, persons, note)
        self.concerts_list.append(new_concert)
        with open('concerts.bin', 'wb') as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)
