import pickle
import random
from fuzzywuzzy import fuzz
from datetime import datetime
from dateparser import parse
from os.path import exists
from concert import Concert
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

    # TODO: How to remove static method warning here and on row 146 (get_country()) and on row 452 (read_window...())?
    def get_saved_concerts(self):
        try:
            with open('concerts.bin', 'rb') as concerts_file:
                saved_concerts = pickle.load(concerts_file)
                return saved_concerts
        except EOFError:
            return []

    def run(self):
        window = self.display_menu()
        self.process_user_click(window)

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

    def display_menu(self):
        if len(self.concerts_list) > 0:
            concert_to_remind_of = self.print_concert_prev_year_same_month()
            welcome_string = 'Welcome! My Concerts helps you remember the concerts you have been to.\n\n\n' + \
                             concert_to_remind_of + '\n\n'
        else:
            welcome_string = 'Welcome! My Concerts helps you remember the concerts you have been to.\n\n\n'

        layout = [[sg.Text(welcome_string)],
                  [sg.Button('Add concert')],
                  [sg.Button('Search for concert')],
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
                    self.display_add_menu()
                case 'Search for concert':
                    self.display_search_menu()
                case 'Random concert':
                    self.display_random_concert()
                case 'All concerts':
                    self.display_all_concerts()
                case 'All artists':
                    self.display_all("artists", "All artists you have seen")
                case 'All venues':
                    self.display_all("venues", "All venues you have been to concerts in")
                case 'All persons':
                    self.display_all("persons", "All persons you have been to concerts with")
        window.close()

    def display_add_menu(self):
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

        self.read_window_ok_button(window)

    def get_country(self, city):
        locator = Nominatim(user_agent="geoapiExercises")
        location = locator.geocode(city)
        regex = re.compile(r'[^,]*$')
        return regex.findall(location.raw['display_name'])[0].lstrip()

    def display_search_menu(self):
        layout = ([[sg.Text("Search"), sg.Input()],
                   [sg.Radio("Artist", 'RADIO1', default=True, key="ARTIST")],
                   [sg.Radio("Venue", 'RADIO1', key="VENUE")],
                   [sg.Radio("Person", 'RADIO1', key="PERSON")],
                   [sg.Button("Search by date (new window)")],
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
                        self.display_search_result("artist", values)
                    elif values["VENUE"]:
                        self.display_search_result("venue", values)
                    # elif values["DATE"]:
                    #     self.display_search_result("date", values)
                    elif values["PERSON"]:
                        self.display_search_result("person", values)
                case "Search by date (opens in a new window)":
                    self.date_search()
                case 'Back':
                    break
        window.close()

    def date_search(self):
        layout = [[sg.Text("Enter a specific date here...")],
                  [sg.Text("Date"), sg.Input()],
                  [sg.Text("...or enter two dates for a search between a range of dates here")],
                  [sg.Text("Date 1"), sg.Input()],
                  [sg.Text("Date 2"), sg.Input()],
                  [sg.Button("OK")],
                  [sg.Button("Back")]]

        window = sg.Window("Enter date", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case 'OK':
                    self.display_search_result("date", values)
                case 'Back':
                    break
        window.close()

    def display_search_result(self, search, values):
        found_concerts = []
        search_string = values[0]

        for concert in self.concerts_list:
            match search:
                case "artist":
                    if fuzz.ratio(search_string.lower(), concert.artist.name.lower()) > 90 or \
                            fuzz.partial_ratio(search_string.lower(), concert.artist.name.lower()) > 95:
                        found_concerts.append(concert)

                case "venue":
                    if fuzz.ratio(search_string.lower(), concert.venue.name.lower()) > 90:
                        found_concerts.append(concert)

                case "date":
                    if values[0] != '':
                        date = parse(values[0])
                        if date == concert.date:
                            found_concerts.append(concert)
                    else:
                        first_date = parse(values[1], settings={'PREFER_DAY_OF_MONTH': 'first'})
                        second_date = parse(values[2], settings={'PREFER_DAY_OF_MONTH': 'last'})
                        if first_date <= concert.date <= second_date:
                            found_concerts.append(concert)

                case "person":
                    for saved_person in concert.persons:
                        if fuzz.ratio(search_string.lower(), saved_person.first_name) > 90 or \
                                fuzz.partial_ratio(search_string.lower(), saved_person.first_name.lower()) > 95:
                            found_concerts.append(concert)

        if len(found_concerts) > 0:
            self.display_found(found_concerts)
        else:
            self.display_not_found(search, search_string)

    def display_found(self, found_concerts):
        print_concerts_string = ''
        for concert in sorted(found_concerts, key=lambda c: c.date):
            print_concerts_string += concert.return_concert_string() + '\n\n'
        layout = [[sg.Text(print_concerts_string)],
                  [sg.Button('Change')],
                  [sg.Button('Remove')],
                  [sg.Button('Back')],
                  [sg.Button('Main menu')]]

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

    def display_not_found(self, sort_to_search, search_string):
        layout = None
        match sort_to_search:
            case "artist":
                layout = [[sg.Text(f"Unfortunately you have no recollection of a concert with the artist "
                                   f"{search_string}.")],
                          [sg.Text(f"If you have gotten a new memory you can add it in the main menu.")],
                          [sg.Button("OK")]]
            case "venue":
                layout = [[sg.Text(f"Unfortunately you have no recollection of a concert at the venue "
                                   f"{search_string}.")],
                          [sg.Text(f"If you have gotten a new memory you can add it in the main menu.")],
                          [sg.Button("OK")]]
            case "date":
                # TODO: Print date with strftime?
                layout = [[sg.Text(f"Unfortunately you have no recollection of a concert on the date "
                                   f"{search_string}.")],
                          [sg.Text(f"If you have gotten a new memory you can add it in the main menu.")],
                          [sg.Button("OK")]]

            case "person":
                layout = [[sg.Text(f"Unfortunately you have no recollection of going to a concert together with "
                                   f"the person {search_string}.")],
                          [sg.Text(f"If you have gotten a new memory you can add it in the main menu.")],
                          [sg.Button("OK")]]

        window = sg.Window("Not found", layout, modal=True)

        self.read_window_ok_button(window)

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
                    self.change_concert(values, concert)
                case 'Back':
                    break
        window.close()

    def change_concert(self, values, concert):
        artist = values[0]
        venue = values[1]
        date = values[2]
        persons = values[3].split()
        note = values[4]

        altered_concert = Concert(artist, venue, date, persons, note)
        self.concerts_list.append(altered_concert)
        self.concerts_list.remove(concert)
        with open('concerts.bin', 'wb') as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)

        layout = [[sg.Text("The concert was altered with the new facts:")],
                  [sg.Text(altered_concert.return_concert_string())],
                  [sg.Button('OK')]]
        window = sg.Window("Changed concert", layout, modal=True)

        self.read_window_ok_button(window)

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

        self.read_window_ok_button(window)

    def display_random_concert(self):
        concert_string = self.concerts_list[random.randrange(len(self.concerts_list))].return_concert_string()
        layout = [[sg.Text(concert_string)], [sg.Button("OK")]]
        window = sg.Window("Random concert", layout, modal=True)

        self.read_window_ok_button(window)

    def display_all_concerts(self):
        all_concerts = ""
        for concert in sorted(self.concerts_list, key=lambda c: c.date):
            all_concerts += concert.print_concert_summary() + "\n"

        layout = [[sg.Text(all_concerts)], [sg.Button("OK")]]
        window = sg.Window("All concerts you have seen", layout, modal=True)

        self.read_window_ok_button(window)

    def display_all(self, items, title):
        all_items = []
        for concert in self.concerts_list:
            match items:
                case "artists":
                    all_items.append(concert.artist.name)
                case "venues":
                    all_items.append(concert.venue.name)
                case "persons":
                    for person in concert.persons:
                        all_items.append(person.first_name)
        all_items_string = ""
        for x in sorted(list(set(all_items)), key=str.casefold):
            all_items_string += "* " + x + "\n"

        layout = [[sg.Text(all_items_string)], [sg.Button("OK")]]
        window = sg.Window(title, layout, modal=True)

        self.read_window_ok_button(window)

    def read_window_ok_button(self, window):
        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case "OK":
                    break
        window.close()
