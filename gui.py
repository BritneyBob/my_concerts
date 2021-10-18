import pickle
import random
from fuzzywuzzy import fuzz
from datetime import datetime
from dateparser import parse
from os.path import exists
from concert import Concert
from terminal_color import color_print
import PySimpleGUI as sg
from geopy.geocoders import Nominatim
import re


class GUI:
    def __init__(self):
        self.running = True
        if exists('concerts.bin'):
            self.concerts_list = self.get_saved_concerts()
        else:
            self.concerts_list = []

    def run(self):
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
                    self.display_add_concert()
                case 'Search concert':
                    self.display_search_menu()
                case 'Random concert':
                    self.display_random()
                case 'All concerts':
                    self.display_all_concerts()
                case 'All artists':
                    self.display_all_artists()
                case 'All venues':
                    self.display_all_venues()
                case 'All persons':
                    self.display_all_persons()
        window.close()

    # def display_menu(self):
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

    def display_add_concert(self):
        layout = [[sg.Text("Add a new concert to your memory", key="new")],
                  [sg.Text("Artist"), sg.Input()],
                  [sg.Text("Venue"), sg.Input()],
                  [sg.Text("City"), sg.Input()],
                  [sg.Text("Date"), sg.Input()],
                  [sg.Text("Person/s you went with (optional)"), sg.Multiline()],
                  [sg.Text("Note (optional)"), sg.Multiline()],
                  [sg.Button("OK")],
                  [sg.Button("Back")]]
        window = sg.Window("Add concert", layout, modal=True)
        # choice = None
        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case 'OK':
                    self.add_concert(values)
                case 'Back':
                    break
        window.close()

    def add_concert(self, values):
        country = self.get_country(values[2])

        artist = values[0]
        venue = (values[1], values[2], country)
        date = values[3]
        # TODO: Kanske be om komma mellan namnen och sen split på komma, så går det att lägga till efternamn
        #       om två heter samma förnamn.
        persons = values[4].split()
        note = values[5]

        new_concert = Concert(artist, venue, date, persons, note)
        self.concerts_list.append(new_concert)
        with open('concerts.bin', 'wb') as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)

        layout = [[sg.Text("The new concert was added to your memory:")],
                  [sg.Text(new_concert.return_concert_string())],
                  [sg.Button('OK')]]
        window = sg.Window("New concert", layout, modal=True)
        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case 'OK':
                    break
        window.close()

    def get_country(self, city):
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        regex = re.compile(r'[^,]*$')
        return regex.findall(location.raw['display_name'])[0].lstrip()

    def display_search_menu(self):
        layout = ([[sg.Text("Search"), sg.Input()],
                   [sg.Radio("Artist", 'RADIO1', default=True, key="ARTIST")],
                   [sg.Radio("Venue", 'RADIO1', key="VENUE")],
                   [sg.Radio("Date", 'RADIO1', key="DATE")],
                   [sg.Radio("Person", 'RADIO1', key="PERSON")],
                   [sg.Button('OK')],
                   [sg.Button('Back')]])
        window = sg.Window("Search concert", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case 'OK':
                    if values["ARTIST"]:
                        self.display_artist_search_result(values)
                    elif values["VENUE"]:
                        self.display_venue_search_result(values)
                    elif values["DATE"]:
                        self.display_date_search_result(values)
                    elif values["PERSON"]:
                        self.display_person_search_result(values)
                case 'Back':
                    break
        window.close()

    def display_artist_search_result(self, values):
        found_concerts = []
        artist = values[0]

        for concert in self.concerts_list:
            if fuzz.ratio(artist.lower(), concert.artist.name.lower()) > 90 or \
               fuzz.partial_ratio(artist.lower(), concert.artist.name.lower()) > 95:
                found_concerts.append(concert)

        if len(found_concerts) > 0:
            print_concerts_string = ''
            # for concert in sorted(found_concerts, key=lambda c: c.date.date):
            for concert in found_concerts:
                print_concerts_string += concert.return_concert_string() + '\n\n'
            layout = [[sg.Text(print_concerts_string)],
                      [sg.Button('Change')],
                      [sg.Button('Remove')],
                      [sg.Button('Back')],
                      [sg.Button('Main menu')]]
        else:
            layout = [[sg.Text(f"Unfortunately you have no recollection of a concert with the artist {artist}.")],
                      [sg.Text(f"If you have gotten a new memory you can add it in the main menu.")]]

        self.display_search_result(layout, found_concerts)

    def display_venue_search_result(self, values):
        venue = values[0]
        found_concerts = []

        for concert in self.concerts_list:
            if fuzz.ratio(venue.lower(), concert.venue.name.lower()) > 90:
                found_concerts.append(concert)

        if len(found_concerts) > 0:
            print_concerts_string = ''
            # for concert in sorted(found_concerts, key=lambda c: c.date.date):
            for concert in found_concerts:
                print_concerts_string += concert.return_concert_string() + '\n\n'
            layout = [[sg.Text(print_concerts_string)],
                      [sg.Button('Change')],
                      [sg.Button('Remove')],
                      [sg.Button('Back')],
                      [sg.Button('Main menu')]]
        else:
            layout = [[sg.Text(f"Unfortunately you have no recollection of a concert at the venue {venue}.")],
                      [sg.Text(f"If you have gotten a new memory you can add it in the main menu.")]]

        self.display_search_result(layout, found_concerts)

    def display_date_search_result(self, values):
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

    def display_person_search_result(self, values):
        person = values[0]
        found_concerts = []

        for concert in self.concerts_list:
            for saved_person in concert.persons:
                if fuzz.ratio(person.lower(), saved_person.first_name) > 90 or \
                   fuzz.partial_ratio(person.lower(), saved_person.first_name.lower()) > 95:
                    found_concerts.append(concert)

        if len(found_concerts) > 0:
            print_concerts_string = ''
            # for concert in sorted(found_concerts, key=lambda c: c.date.date):
            for concert in found_concerts:
                print_concerts_string += concert.return_concert_string() + '\n\n'
            layout = [[sg.Text(print_concerts_string)],
                      [sg.Button('Change')],
                      [sg.Button('Remove')],
                      [sg.Button('Back')],
                      [sg.Button('Main menu')]]
        else:
            layout = [[sg.Text(f"Unfortunately you have no recollection of going to a concert together with the person "
                               f"{person}.")],
                      [sg.Text(f"If you have gotten a new memory you can add it in the main menu.")]]

        self.display_search_result(layout, found_concerts)

    def display_search_result(self, layout, found_concerts):
        window = sg.Window("Search result", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case 'Change':
                    self.concert_to_change(found_concerts)
                case 'Remove':
                    self.remove_is_sure(found_concerts)
                case 'Back':
                    break
                case 'Main menu':
                    break
            window.close()

    def concert_to_change(self, concerts):
        if len(concerts) > 1:
            # buttons_text = []
            # for concert in concerts:
            #     buttons_text.append(concert.print_concert_summary())
            #
            # layout = [[sg.Text("Please click on the concert you want to change:")],
            #           [sg.Button(buttons_text[0])]]
            # window = sg.Window("Choose concert", layout, modal=True)
            #
            # while True:
            #     event, values = window.read()
            #     match event:
            #         case sg.WIN_CLOSED:
            #             break
            #         case buttons_text[0]:
            #             concert = concerts[0]
            #
            #     window.close()
            concert = concerts[0]

        else:
            concert = concerts[0]

        self.change(concert)

    def change(self, concert):
        persons_list = [person.first_name for person in concert.persons]

        layout = [[sg.Text("Add a new concert to your memory", key="new")],
                  [sg.Text("Artist"), sg.Input(concert.artist.name)],
                  [sg.Text("Venue"), sg.Input(concert.venue.name)],
                  [sg.Text("Date"), sg.Input(concert.date.strftime('%Y-%m-%d'))],
                  [sg.Text("Person/s you went with"), sg.Multiline(' '.join(persons_list))],  # TODO: join med komma?
                  [sg.Text("Note"), sg.Multiline(concert.note.note)],
                  [sg.Button("OK")],
                  [sg.Button("Back")]]
        window = sg.Window("Change concert", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case 'OK':
                    self.change_concert(values)
                case 'Back':
                    break
        window.close()

    def change_concert(self, values):
        artist = values[0]
        venue = values[1]
        date = values[2]
        persons = values[3].split()
        note = values[4]

        altered_concert = Concert(artist, venue, date, persons, note)
        self.concerts_list.append(altered_concert)
        with open('concerts.bin', 'wb') as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)

        layout = [[sg.Text("The concert was altered with the new facts:")],
                  [sg.Text(altered_concert.return_concert_string())],
                  [sg.Button('OK')]]
        window = sg.Window("Changed concert", layout, modal=True)
        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case 'OK':
                    break
        window.close()

    def remove_is_sure(self, concerts):
        if len(concerts) > 1:
            # buttons_text = []
            # for concert in concerts:
            #     buttons_text.append(concert.print_concert_summary())
            #
            # layout = [[sg.Text("Please click on the concert you want to change:")],
            #           [sg.Button(buttons_text[0])]]
            # window = sg.Window("Choose concert", layout, modal=True)
            #
            # while True:
            #     event, values = window.read()
            #     match event:
            #         case sg.WIN_CLOSED:
            #             break
            #         case buttons_text[0]:
            #             concert = concerts[0]
            #
            #     window.close()
            concert = concerts[0]
        else:
            concert = concerts[0]

        layout = [[sg.Text("Are you sure you want to remove this concert?:")],
                  [sg.Text(concert.print_concert_summary())],
                  [sg.Button("Yes, REMOVE")],
                  [sg.Button("No, cancel")]]
        window = sg.Window("Remove concert", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case "Yes, REMOVE":
                    self.remove(concert)
                case "No, cancel":
                    break
        window.close()

    def remove(self, concert):
        self.concerts_list.remove(concert)
        with open('concerts.bin', 'wb') as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)
        layout = [[sg.Text("The chosen concert was removed.")],
                  [sg.Button("OK")]]
        window = sg.Window("Removed concert", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case "OK":
                    break
        window.close()

    def display_random(self):
        concert_string = self.concerts_list[random.randrange(len(self.concerts_list))].return_concert_string()
        layout = [[sg.Text(concert_string)], [sg.Button("OK")]]
        window = sg.Window("Random concert", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case "OK":
                    break
        window.close()

    def display_all_concerts(self):
        all_concerts = ""
        for concert in self.concerts_list:
            all_concerts += concert.print_concert_summary() + "\n"
        # all_artists = []
        # for artist in sorted(list(set(all_artists)), key=str.casefold):

        layout = [[sg.Text(all_concerts)], [sg.Button("OK")]]
        window = sg.Window("All concerts you have seen", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case "OK":
                    break
        window.close()

    def display_all_artists(self):
        all_artists = []
        for concert in self.concerts_list:
            all_artists.append(concert.artist.name)
        artists = ""
        for artist in sorted(list(set(all_artists)), key=str.casefold):
            artists += "* " + artist + "\n"

        layout = [[sg.Text(artists)], [sg.Button("OK")]]
        window = sg.Window("Artists you have seen", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case "OK":
                    break
        window.close()

    def display_all_venues(self):
        all_venues = []
        for concert in self.concerts_list:
            all_venues.append(concert.venue.name)
        venues = ""
        for venue in sorted(list(set(all_venues)), key=str.casefold):
            venues += "* " + venue + "\n"

        layout = [[sg.Text(venues)], [sg.Button("OK")]]
        window = sg.Window("Venues you have been to", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case "OK":
                    break
        window.close()

    def display_all_persons(self):
        all_persons = []
        for concert in self.concerts_list:
            for person in concert.persons:
                all_persons.append(person.first_name)
        persons = ""
        for person in sorted(list(set(all_persons))):
            persons += "* " + person + "\n"

        layout = [[sg.Text(persons)], [sg.Button("OK")]]
        window = sg.Window("Persons you have been to concerts with", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case "OK":
                    break
        window.close()
