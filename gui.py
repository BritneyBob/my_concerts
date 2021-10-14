import pickle
import random
from fuzzywuzzy import fuzz
from datetime import datetime
from dateparser import parse
from os.path import exists
from concert import Concert
from terminal_color import color_print
import PySimpleGUI as sg


class Menu:
    def __init__(self):
        self.running = True
        if exists('concerts.bin'):
            self.concerts_list = self.get_saved_concerts()
        else:
            self.concerts_list = []

    def run(self):
        #while self.running:
            #self.display_menu()
        window = self.display()
        self.process_user_click(window)

    def display(self):
        if len(self.concerts_list) > 0:
            concert_to_remind_of = self.print_concert_prev_year_same_month()
            welcome_string = 'Welcome! My Concerts helps you remember the concerts you have been to.\n\n\n' + \
                             concert_to_remind_of + '\n\n'
        else:
            welcome_string = 'Welcome! My Concerts helps you remember the concerts you have been to.\n\n\n'

        layout = [[sg.Text(welcome_string)],
                  [sg.Button('Add concert')],
                  [sg.Button('Search concert')],
                  [sg.Button('Random concert')],
                  [sg.Button('All concerts')],
                  [sg.Button('All artists')],
                  [sg.Button('All venues')],
                  [sg.Button('All persons')],
                  [sg.Button('Quit')]]
        window = sg.Window("My Concerts", layout)

        return window

    def process_user_click(self, window):
        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | 'Quit':
                    break
                case 'Add concert':
                    pass
                case 'Search concert':
                    pass
                case 'Random concert':
                    pass
                case 'All concerts':
                    pass
                case 'All artists':
                    pass
                case 'All venues':
                    pass
                case 'All persons':
                    pass
        window.close()

    # Går det att få bort varningen för static method här?
    def get_saved_concerts(self):
        try:
            with open('concerts.bin', 'rb') as concerts_file:
                saved_concerts = pickle.load(concerts_file)
                return saved_concerts
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
        years_since_concert = datetime.now().year - concert_to_remind_of.date.year
        remind_string = ''
        match years_since_concert:
            case 0:
                remind_string += f'RECENTLY...\n'
            case 1:
                remind_string += f'1 YEAR AGO...\n'
            case _:
                remind_string += f'{years_since_concert} YEARS AGO...\n'
        concert_string = concert_to_remind_of.return_concert_string()
        return remind_string + concert_string

    # def display_menu(self):
    #     color_print('cyan', f"\nMAIN MENU")
    #     color_print('magenta', f"1. Add a new concert to your memory")
    #     color_print('green', f"2. Search for one or more concerts")
    #     color_print('magenta', f"3. Be reminded of a random concert")
    #     color_print('green', f"4. Be reminded of all concerts you have been to")
    #     color_print('magenta', f"5. Be reminded of all artists you have seen")
    #     color_print('green', f"6. Be reminded of all venues you have been to concerts in")
    #     color_print('magenta', f"7. Be reminded of all persons you have been to concerts with")
    #     choice = input("What would you like to do (1-7 or quit)?: ")
    #     print()
    #     match choice:
    #         case '1':
    #             self.add_concert()
    #         case '2':
    #             self.search_menu()
    #         case '3':
    #             self.concerts_list[random.randrange(len(self.concerts_list))].print_concert()
    #         case '4':
    #             color_print('magenta', f"ALL CONCERTS YOU REMEMBER")
    #             for concert in sorted(self.concerts_list, key=lambda c: c.date):
    #                 concert.print_concert()
    #         # Kan man lägga 5-7 i en (samma) metod?
    #         case '5':
    #             color_print('magenta', f"ARTISTS YOU HAVE SEEN")
    #             all_artists = []
    #             for concert in self.concerts_list:
    #                 all_artists.append(concert.artist.name)
    #             for artist in sorted(list(set(all_artists)), key=str.casefold):
    #                 color_print('blue', f'* {artist}')
    #         case '6':
    #             color_print('magenta', f"VENUES YOU HAVE SEEN CONCERTS IN")
    #             all_venues = []
    #             for concert in self.concerts_list:
    #                 all_venues.append(concert.venue.name)
    #             for artist in sorted(list(set(all_venues))):
    #                 color_print('blue', f'* {artist}')
    #         case '7':
    #             color_print('magenta', f"PEOPLE YOU HAVE BEEN TO CONCERTS WITH")
    #             all_persons = []
    #             for concert in self.concerts_list:
    #                 for person in concert.persons:
    #                     all_persons.append(person.first_name)
    #             for person in sorted(list(set(all_persons))):
    #                 color_print('blue', f'* {person}')
    #         case 'quit':
    #             self.running = False
    #         case _:
    #             color_print('red', f"Please enter a choice 1-7")

    def search_menu(self):
        color_print('cyan', f"SEARCH MENU")
        color_print('magenta', f"1. Artist")
        color_print('green', f"2. Venue")
        color_print('magenta', f"3. Date")
        color_print('green', f"4. Person")
        choice = int(input("What would you like to search for (1-4)?: "))
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

    # ett försök till en gemensam sökmetod, vet inte om det går att göra, men så här funkar det inte.
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
            if fuzz.ratio(artist.lower(), concert.artist.name.lower()) > 90 or \
               fuzz.partial_ratio(artist.lower(), concert.artist.name.lower()) > 95:
                found_concerts.append(concert)
        if len(found_concerts) > 0:
            for concert in sorted(found_concerts, key=lambda c: c.date.date):
                concert.print_concert()
            remove_change = input("Would you like to change facts about a concert or remove a concert (enter 'change', "
                                  "'remove' or 'no')? ")
            if remove_change == 'change':
                self.change(found_concerts)
            elif remove_change == 'remove':
                self.remove(found_concerts)
        else:
            color_print('red', f"Unfortunately you have no recollection of a concert with the artist {artist}.")
            color_print('red', f"If you have gotten a new memory you can add it by choosing 1 in the main menu.")

    def search_venue(self):
        venue = input("Please enter the name of a venue: ")
        found_concerts = []
        for concert in self.concerts_list:
            if fuzz.ratio(venue.lower(), concert.venue.name.lower()) > 90:
                found_concerts.append(concert)
        if len(found_concerts) > 0:
            for concert in sorted(found_concerts, key=lambda c: c.date.date):
                concert.print_concert()
            remove_change = input("Would you like to change facts about a concert or remove a concert (enter 'change', "
                                  "'remove' or 'no')? ")
            if remove_change == 'change':
                self.change(found_concerts)
            elif remove_change == 'remove':
                self.remove(found_concerts)
        else:
            color_print('red', f"Unfortunately you have no recollection of a concert at the venue {venue}.")
            color_print('red', f"If you have gotten a new memory you can add it by choosing 1 in the main menu.")

    def search_date(self):
        found_concerts = []
        while True:
            kind_of_date_search = \
                input("Enter 1 to search for a specific date or 2 to search for a range between dates: ")
            match kind_of_date_search:
                case '1':
                    date = input("Please enter a date: ")
                    date = parse(date)
                    for concert in self.concerts_list:
                        if date == concert.date:
                            found_concerts.append(concert)
                    break
                case '2':
                    first_date = input("Please enter the first date: ")
                    second_date = input("Please enter the second date: ")
                    first_date = parse(first_date, settings={'PREFER_DAY_OF_MONTH': 'first'})
                    second_date = parse(second_date, settings={'PREFER_DAY_OF_MONTH': 'last'})
                    for concert in self.concerts_list:
                        if first_date <= concert.date <= second_date:
                            found_concerts.append(concert)
                    break

        if self.print_search_result(found_concerts):
            self.print_search_result(found_concerts)
        else:
            color_print('red', f"Unfortunately you have no recollection of a concert on the date "
                               f"{date.strftime('%Y-%m-%d')}.")
            color_print('red', f"If you have gotten a new memory you can add it by choosing 1 in the main menu.")

    def search_person(self):
        person = input("Please enter the name of a person: ")
        found_concerts = []
        for concert in self.concerts_list:
            for saved_person in concert.persons:
                if fuzz.ratio(person.lower(), saved_person.first_name) > 90 or \
                   fuzz.partial_ratio(person.lower(), saved_person.name.lower()) > 95:
                    found_concerts.append(concert)
        if self.print_search_result(found_concerts):
            self.print_search_result(found_concerts)
        else:
            color_print('red', f"Unfortunately you have no recollection of going to a concert together with the person "
                               f"{person}.")
            color_print('red', f"If you have gotten a new memory you can add it by choosing 1 in the main menu.")

    def print_search_result(self, found_concerts):
        if len(found_concerts) > 0:
            for concert in sorted(found_concerts, key=lambda c: c.date):
                concert.print_concert()

            while True:
                remove_change = input("Would you like to change facts about a concert or remove a concert "
                                      "(enter 'change', 'remove' or 'no')? ")
                match remove_change:
                    case 'change':
                        self.change(found_concerts)
                        break
                    case 'remove':
                        self.remove(found_concerts)
                        break
        else:
            return False

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

        date = input("What date was the concert?: ")

        persons = input("Did you go with someone to the concert? If yes, please enter one or more names: ").split()

        is_note = input("Would you like to add a note about this concert? ")
        if is_note.lower() == 'yes':
            note = input("Please enter your notes about the concert: ")
        elif is_note.lower() == 'no':
            note = ''

        new_concert = Concert(artist, venue, date, persons, note)
        self.concerts_list.append(new_concert)
        with open('concerts.bin', 'wb') as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)
        print()
        color_print('cyan', f"The new concert was added:\n")
        new_concert.print_concert()

    def change(self, concerts):
        if len(concerts) > 1:
            for i, concert in enumerate(concerts):
                print(f"{i+1}.", end=' ')
                concert.print_concert()
            concert_choice = int(input(f"Which of the concerts would you like to change facts about "
                                       f"(1-{len(concerts)})?: "))
            concert = concerts[concert_choice-1]
        else:
            concert = concerts[0]

        # Här skrivs samma meny ut som där man söker, borde gå att lägga detta i en printmetod
        color_print('magenta', f"1. Artist")
        color_print('green', f"2. Venue")
        color_print('magenta', f"3. Date")
        color_print('green', f"4. Person")
        color_print('magenta', f"5. Note")
        fact_to_change = input("Which fact would you like to change? (1-5): ")
        persons_list = []
        for person in concert.persons:
            persons_list.append(person.first_name)
        match fact_to_change:
            case '1':
                changed_artist = input("Please enter the altered name of the artist: ")
                changed_concert = Concert(changed_artist, concert.venue.name, concert.date.strftime('%Y-%m-%d'),
                                          persons_list, concert.note.note)
            case '2':
                changed_venue = input("Please enter the altered name of the venue: ")
                changed_concert = Concert(concert.artist.name, changed_venue, concert.date.strftime('%Y-%m-%d'),
                                          persons_list, concert.note.note)
            case '3':
                changed_date = input("Please enter the altered date: ")
                changed_concert = Concert(concert.artist.name, concert.venue.name, changed_date, persons_list,
                                          concert.note.note)
            case '4':
                changed_persons = input("Please enter the altered name/s of the person/s: ").split()
                changed_concert = Concert(concert.artist.name, concert.venue.name, concert.date.strftime('%Y-%m-%d'),
                                          changed_persons, concert.note.note)
            case '5':
                changed_note = input("Please enter the new note: ")
                changed_concert = Concert(concert.artist.name, concert.venue.name, concert.date.strftime('%Y-%m-%d'),
                                          persons_list, changed_note)

        self.concerts_list.append(changed_concert)
        self.concerts_list.remove(concert)
        with open('concerts.bin', 'wb') as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)
        color_print('cyan', f"\nThe concert was altered with the new facts:\n")
        changed_concert.print_concert()

    def remove(self, concerts):
        if len(concerts) > 1:
            for i, concert in enumerate(concerts):
                print(f"{i+1}.", end=' ')
                concert.print_concert()
            concert_choice = int(input(f"Which of the concerts would you like to remove (1-{len(concerts)})?: "))
            concert = concerts(concert_choice-1)
        else:
            concert = concerts[0]

        while True:
            is_sure = input("Are you sure you want to remove the concert (Y for yes, N for no)?")
            match is_sure:
                case 'Y':
                    self.concerts_list.remove(concert)
                    with open('concerts.bin', 'wb') as concerts_file:
                        pickle.dump(self.concerts_list, concerts_file)
                    color_print('cyan', f"The chosen concert was removed.")
                    break
                case 'N':
                    color_print('cyan', f"The concert was not removed. Going back to Main menu.")
                    break
                case _:
                    continue

