# TODO: Check where there needs to be back to main menu-buttons and fix that feature

import pickle
import random
from fuzzywuzzy import fuzz
from datetime import datetime
from dateparser import parse
from os.path import exists
from concert import Concert
import PySimpleGUI as sg
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import re


class GUI:
    def __init__(self):
        self.running = True
        if exists('concerts.bin'):
            self.concerts_list = self.get_saved_concerts()
        else:
            self.concerts_list = []

    # TODO: How to remove static method warning here and on row 146 (get_country())?
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
            try:
                if current_month == concert.date.month:
                    concerts_this_month_prev_years.append(concert)
            except AttributeError:
                pass

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
            welcome_string = 'Welcome! My Concerts helps you remember the concerts you have been to.\n'

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
                    sg.popup("Random concert",
                             self.concerts_list[random.randrange(len(self.concerts_list))].return_concert_string())
                case 'All concerts':
                    self.display_all_concerts()
                case 'All artists':
                    self.display_all("artists", "All artists you have seen:")
                case 'All venues':
                    self.display_all("venues", "All venues you have been to concerts in:")
                case 'All persons':
                    self.display_all("persons", "All persons you have been to concerts with:")
        window.close()

    def display_add_menu(self):
        layout = [[sg.Text("Add a new concert to your memory", key="new")],
                  [sg.Text("Artist"), sg.Input()],
                  [sg.Text("Venue"), sg.Input()],
                  [sg.Text("City"), sg.Input()],
                  [sg.Text("Date"), sg.Input()],
                  [sg.Text("Person/s you went with (optional) (separate persons with comma)"), sg.Multiline()],
                  [sg.Text("Note (optional)"), sg.Multiline()],
                  [sg.Button("OK")],
                  [sg.Button("Back")]]
        window = sg.Window("Add concert", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | "Back":
                    break
                case 'OK':
                    try:
                        parse(values[3]).strftime('%Y-%m-%d')
                        self.add_concert(values)
                        break
                    except AttributeError:
                        # TODO: Fix so that the concert is not added if this happens
                        sg.popup("Incorrect date input", "Please enter date in another format")
        window.close()

    def add_concert(self, values):
        try:
            country = self.get_country(values[2])
        except GeocoderTimedOut:
            country = "Country couldn't be fetched due to a time out error"

        artist = values[0]
        venue = (values[1], values[2], country)
        date = values[3]
        persons = values[4].split(', ')
        note = values[5]

        new_concert = Concert(artist, venue, date, persons, note)
        self.concerts_list.append(new_concert)
        with open('concerts.bin', 'wb') as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)

        sg.popup("The new concert was added to your memory", new_concert.return_concert_string())

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
                case sg.WIN_CLOSED | "Back":
                    break
                case 'OK':
                    if values["ARTIST"]:
                        self.display_search_result("artist", values)
                        break
                    elif values["VENUE"]:
                        self.display_search_result("venue", values)
                        break
                    elif values["PERSON"]:
                        self.display_search_result("person", values)
                        break
                case "Search by date (new window)":
                    self.date_search()
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
                case sg.WIN_CLOSED | "Back":
                    break
                case 'OK':
                    self.display_search_result("date", values)
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
                        # TODO: Check that input is a date
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
                  [sg.Button('Back')]]

        window = sg.Window("Search result", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                # TODO: Back button doesn't work - why?
                case sg.WIN_CLOSED | "Back":
                    break
                case 'Change':
                    self.change(found_concerts)
                    break
                case 'Remove':
                    self.remove(found_concerts)
                    break
            window.close()

    def display_not_found(self, sort_to_search, search_string):
        no_memory_string = ''
        match sort_to_search:
            case "artist":
                no_memory_string = "Unfortunately you have no recollection of a concert with the artist", \
                                   search_string, "."
            case "venue":
                no_memory_string = "Unfortunately you have no recollection of a concert at the venue", search_string, \
                                   "."
            case "date":
                date = parse(search_string)
                no_memory_string = "Unfortunately you have no recollection of a concert on the date", \
                                   date.strftime('%Y-%m-%d'), "."
            case "person":
                no_memory_string = "Unfortunately you have no recollection of going to a concert together with the " \
                                   "person", search_string, "."

        layout = [[sg.Text(no_memory_string)],
                  [sg.Text(f"If you have gotten a new memory you can add it in the main menu.")],
                  [sg.Button("OK")]]

        window = sg.Window("Not found", layout, modal=True)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'OK'):
                break
        window.close()

    def change(self, concerts):
        values, concert = self.facts_to_change(concerts)
        artist = values[0]
        venue = values[1]
        city = values[2]
        country = values[3]
        date = values[4]
        persons = values[5].split(', ')
        note = values[6]

        altered_concert = Concert(artist, (venue, city, country), date, persons, note)
        self.concerts_list.append(altered_concert)
        self.concerts_list.remove(concert)
        with open('concerts.bin', 'wb') as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)

        sg.popup("The concert was altered with the new facts:", altered_concert.return_concert_string())

    def facts_to_change(self, concerts):
        concert = self.choose_concert(concerts)
        persons_list = [person.first_name for person in concert.persons]

        layout = [[sg.Text("Artist"), sg.Input(concert.artist.name)],
                  [sg.Text("Venue"), sg.Input(concert.venue.name)],
                  [sg.Text("City"), sg.Input(concert.venue.city)],
                  [sg.Text("Country"), sg.Input(concert.venue.country)],
                  [sg.Text("Date"), sg.Input(concert.date.strftime('%Y-%m-%d'))],
                  [sg.Text("Person/s you went with"), sg.Multiline(', '.join(persons_list))],
                  [sg.Text("Note"), sg.Multiline(concert.note.note)],
                  [sg.Button("OK")],
                  [sg.Button("Back")]]
        window = sg.Window("Change concert", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | "Back":
                    break
                case 'OK':
                    window.close()
                    return values, concert
        window.close()

    def choose_concert(self, concerts):
        if len(concerts) > 1:
            layout = [[sg.Text("Please select a concert:")],
                      *[[sg.Button(concert.print_concert_summary())]
                        for concert in sorted(concerts, key=lambda c: c.date)]]
            window = sg.Window("Choose concert", layout, modal=True)

            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    break
                for concert in concerts:
                    if window[event].get_text() == concert.print_concert_summary():
                        window.close()
                        return concert
            window.close()

        else:
            return concerts[0]

    def remove(self, concerts):
        concert = self.choose_concert(concerts)
        if self.is_sure(concert):
            self.concerts_list.remove(concert)
            with open('concerts.bin', 'wb') as concerts_file:
                pickle.dump(self.concerts_list, concerts_file)

            sg.popup("The chosen concert was removed.")

    def is_sure(self, concert):
        layout = [[sg.Text("Are you sure you want to remove this concert?:")],
                  [sg.Text(concert.print_concert_summary())],
                  [sg.Button("Yes, REMOVE")],
                  [sg.Button("No, cancel")]]
        window = sg.Window("Remove concert", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | "No, cancel":
                    break
                case "Yes, REMOVE":
                    window.close()
                    return True
        window.close()

    def display_all_concerts(self):
        all_concerts = ""
        try:
            for concert in sorted(self.concerts_list, key=lambda c: c.date):
                all_concerts += concert.print_concert_summary() + "\n"
        except TypeError:
            pass

        sg.popup("All concerts you have seen:", all_concerts)

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

        sg.popup(title, all_items_string)
