import pickle
import random
from collections import Counter
from fuzzywuzzy import fuzz
from datetime import datetime
from dateparser import parse
from os.path import exists
import PySimpleGUI as sg
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import re
from concert import Concert


class GUI:
    def __init__(self):
        self.running = True
        if exists("concerts.bin"):
            self.concerts_list = self.get_saved_concerts()
        else:
            self.concerts_list = []

    @classmethod
    def get_saved_concerts(cls):
        try:
            with open("concerts.bin", "rb") as concerts_file:
                saved_concerts = pickle.load(concerts_file)
                return saved_concerts
        except EOFError:
            return []

    def run(self):
        window = self.display_menu()
        self.process_user_click(window)

    def get_random_concert_prev_year_this_month(self):
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

        return concerts_this_month_prev_years[random.randrange(len(concerts_this_month_prev_years))]

    @classmethod
    def get_remember_concert_string(cls, concert_to_print):
        years_since_concert = datetime.now().year - concert_to_print.date.year
        remind_string = ''

        match years_since_concert:
            case 0:
                remind_string += f"RECENTLY...\n"
            case 1:
                remind_string += f"1 YEAR AGO...\n"
            case _:
                remind_string += f"{years_since_concert} YEARS AGO...\n"
        concert_string = concert_to_print.get_concert_long_string()

        return remind_string + concert_string

    def display_menu(self):
        if len(self.concerts_list) > 0:
            random_concert_prev_year_this_month = self.get_random_concert_prev_year_this_month()
            concert_to_remind_of_string = self.get_remember_concert_string(random_concert_prev_year_this_month)
            welcome_string = "Welcome! My Concerts helps you remember the concerts you have been to.\n\n" + \
                             concert_to_remind_of_string + "\n"
        else:
            welcome_string = "Welcome! My Concerts helps you remember the concerts you have been to.\n"

        layout = [[sg.Text(welcome_string)],
                  [sg.Button("Add concert"), sg.Button("Search for concert"), sg.Button("Random concert")],
                  [sg.Text("SEE ALL:"), sg.Button("Concerts"), sg.Button("Artists"), sg.Button("Venues"),
                   sg.Button("Persons")],
                  [sg.Stretch(), sg.Button("Quit")]]
        window = sg.Window("My Concerts", layout)

        return window

    def process_user_click(self, window):
        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | "Quit":
                    break
                case "Add concert":
                    self.display_add_menu()
                case "Search for concert":
                    self.display_search_menu()
                case "Random concert":
                    sg.popup(self.concerts_list[random.randrange(len(self.concerts_list))].get_concert_long_string(),
                             title="Random Concert", line_width=100)
                case "Concerts":
                    self.display_all_concerts()
                case "Artists":
                    self.display_all("artists", "Number of concerts you have been to with each artist:")
                case "Venues":
                    self.display_all("venues", "Number of concerts you have been to at each venue:")
                case "Persons":
                    self.display_all("persons", "Number of concerts you have been to together with each person:")
        window.close()

    def display_add_menu(self):
        layout = [[sg.Text("Artist"), sg.Input()],
                  [sg.Text("Venue"), sg.Input()],
                  [sg.Text("City"), sg.Input()],
                  [sg.Text("Date"), sg.Input()],
                  [sg.Text("Person/s you went with\n(optional)\n(separate with comma)"), sg.Multiline()],
                  [sg.Text("Note\n(optional)"), sg.Multiline()],
                  [sg.Button("OK"), sg.Button("Back")]]
        window = sg.Window("Add concert", layout, element_justification='r', modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | "Back":
                    break
                case "OK":
                    if values[0] and values[1] and values[2] and values[3]:
                        try:
                            parse(values[3]).strftime("%Y-%m-%d")
                            self.add_concert(values)
                            break
                        except AttributeError:
                            sg.popup("Incorrect date input", "Please enter date in another format")
                    else:
                        sg.popup("Please enter artist, venue, city and date")
        window.close()

    def add_concert(self, values):
        try:
            country = self.get_country(values[2])
        except GeocoderTimedOut:
            country = "Country couldn't be fetched due to a time out error"

        artist = values[0]
        venue = (values[1], values[2], country)
        date = values[3]
        persons = values[4].split(', ') if values[4] != '' else []
        note = values[5]

        new_concert = Concert(artist, venue, date, persons, note)
        self.concerts_list.append(new_concert)
        with open("concerts.bin", "wb") as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)

        sg.popup("The new concert was added to your memory", new_concert.get_concert_long_string())

    @classmethod
    def get_country(cls, city):
        locator = Nominatim(user_agent="geoapiExercises")
        location = locator.geocode(city)
        regex = re.compile(r"[^,]*$")
        return regex.findall(location.raw["display_name"])[0].lstrip()

    def display_search_menu(self):
        layout = [[sg.Text("Search"), sg.Input()],
                  [sg.Radio("Artist", 'RADIO1', default=True, key="ARTIST"),
                   sg.Radio("Venue", 'RADIO1', key="VENUE"),
                   sg.Radio("Person", 'RADIO1', key="PERSON"),
                   sg.Button("Search by date (new window)")],
                  [sg.Stretch(), sg.Button("OK"), sg.Button("Back"), sg.Stretch()]]
        window = sg.Window("Search concert", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | "Back":
                    break
                case "OK":
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
                  [sg.Stretch(), sg.Text("Date  "), sg.Input()],
                  [sg.Text("...or enter two dates for a search between a range of dates here")],
                  [sg.Text("Date 1"), sg.Input()],
                  [sg.Text("Date 2"), sg.Input()],
                  [sg.Button("OK"), sg.Button("Back")]]

        incorrect_string = "Incorrect date input. Please enter date in another format"

        window = sg.Window("Enter date", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | "Back":
                    break
                case "OK":
                    if values[0]:
                        try:
                            parse(values[0])
                            self.display_search_result("date", values)
                        except AttributeError:
                            sg.popup(incorrect_string)
                    elif values[1] and values[2]:
                        try:
                            date1 = parse(values[1], settings={"PREFER_DAY_OF_MONTH": "first"})
                            date2 = parse(values[2], settings={"PREFER_DAY_OF_MONTH": "last"})
                            self.display_search_result("date", (date1, date2))
                            break
                        except AttributeError:
                            sg.popup(incorrect_string)
                    else:
                        sg.popup("Please enter one or two dates")
        window.close()

    def display_search_result(self, search, values):
        found_concerts = []
        search_string = values[0]
        two_dates = False

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
                    if isinstance(values, tuple):
                        two_dates = True
                        if values[0] <= concert.date <= values[1]:
                            found_concerts.append(concert)
                    else:
                        if parse(search_string) == concert.date:
                            found_concerts.append(concert)

                case "person":
                    for saved_person in concert.persons:
                        if fuzz.ratio(search_string.lower(), saved_person.first_name) > 90 or \
                                fuzz.partial_ratio(search_string.lower(), saved_person.first_name.lower()) > 95:
                            found_concerts.append(concert)

        if len(found_concerts) > 0:
            self.display_found(found_concerts)
        else:
            if two_dates:
                self.display_not_found(search, (values[0], values[1]))
            else:
                self.display_not_found(search, search_string)

    def display_found(self, found_concerts):
        print_concerts_string = ''
        for concert in sorted(found_concerts, key=lambda c: c.date):
            print_concerts_string += concert.get_concert_long_string() + '\n\n'
        layout = [[sg.Text(print_concerts_string)],
                  [sg.Button("Back"), sg.Stretch(), sg.Button("Change"), sg.Button("Remove")]]

        window = sg.Window("Search result", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | "Back":
                    break
                case "Change":
                    self.choose_concert(found_concerts, "change")
                case "Remove":
                    self.choose_concert(found_concerts, "remove")
        window.close()

    @classmethod
    def display_not_found(cls, sort_to_search, search_string):
        no_memory_string = ''
        match sort_to_search:
            case "artist":
                no_memory_string = f"Unfortunately you have no recollection of a concert with the artist " \
                                   f"{search_string}."
            case "venue":
                no_memory_string = f"Unfortunately you have no recollection of a concert at the venue {search_string}."

            case "date":
                if isinstance(search_string, tuple):
                    date1 = search_string[0].strftime("%Y-%m-%d")
                    date2 = search_string[1].strftime("%Y-%m-%d")
                    no_memory_string = f"Unfortunately you have no recollection of a concert between the dates " \
                                       f"{date1} and {date2}."
                else:
                    date = parse(search_string).strftime("%Y-%m-%d")
                    no_memory_string = f"Unfortunately you have no recollection of a concert on the date {date}."

            case "person":
                no_memory_string = f"Unfortunately you have no recollection of going to a concert together with the " \
                                   f"person {search_string}."

        layout = [[sg.Text(no_memory_string)],
                  [sg.Text("If you have gotten a new memory you can add it in the main menu.")],
                  [sg.Button("OK")]]

        window = sg.Window("Not found", layout, modal=True)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "OK"):
                break
        window.close()

    def choose_concert(self, concerts, change_or_remove):
        target_concert = None
        if len(concerts) > 1:
            layout = [[sg.Text("Please select a concert:")],
                      *[[sg.Button(concert.get_concert_summary())]
                        for concert in sorted(concerts, key=lambda c: c.date)]]
            window = sg.Window("Choose concert", layout, modal=True)

            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    break
                for concert in concerts:
                    if window[event].get_text() == concert.get_concert_summary():
                        window.close()
                        target_concert = concert
            window.close()

        else:
            target_concert = concerts[0]

        if target_concert:
            if change_or_remove == "change":
                self.facts_to_change(target_concert)
            elif change_or_remove == "remove":
                self.remove(target_concert)

    def facts_to_change(self, concert):
        try:
            persons_list = [person.first_name for person in concert.persons]
        except TypeError:
            persons_list = []
        try:
            note = concert.note.note
        except AttributeError:
            note = ""
        layout = [[sg.Text("Artist"), sg.Input(concert.artist.name)],
                  [sg.Text("Venue"), sg.Input(concert.venue.name)],
                  [sg.Text("City"), sg.Input(concert.venue.city)],
                  [sg.Text("Country"), sg.Input(concert.venue.country)],
                  [sg.Text("Date"), sg.Input(concert.date.strftime("%Y-%m-%d"))],
                  [sg.Text("Person/s you went with"), sg.Multiline(", ".join(persons_list))],
                  [sg.Text("Note"), sg.Multiline(note)],
                  [sg.Button("OK"), sg.Button("Back")]]
        window = sg.Window("Change concert", layout, element_justification="r", modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | "Back":
                    break
                case "OK":
                    window.close()
                    self.change(values, concert)
        window.close()

    def change(self, values, concert):
        artist = values[0]
        venue = values[1]
        city = values[2]
        country = values[3]
        date = values[4]
        persons = values[5].split(", ") if values[5] != "" else []
        note = values[6]

        altered_concert = Concert(artist, (venue, city, country), date, persons, note)
        self.concerts_list.append(altered_concert)
        self.concerts_list.remove(concert)
        with open("concerts.bin", "wb") as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)

        sg.popup("The concert was altered with the new facts:", altered_concert.get_concert_long_string(),
                 line_width=100)

    def remove(self, concert):
        if self.is_sure(concert):
            self.concerts_list.remove(concert)
            with open("concerts.bin", "wb") as concerts_file:
                pickle.dump(self.concerts_list, concerts_file)
            sg.popup("The chosen concert was removed.")

    @classmethod
    def is_sure(cls, concert):
        layout = [[sg.Text("Are you sure you want to remove this concert?:")],
                  [sg.Text(concert.get_concert_summary())],
                  [sg.Button("Yes, REMOVE"), sg.Button("No, cancel")]]
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
                all_concerts += concert.get_concert_summary() + "\n"
        except TypeError:
            pass

        sg.popup("All concerts you have seen:", all_concerts, line_width=100)

    def display_all(self, items, title):
        all_items = []
        for concert in self.concerts_list:
            match items:
                case "artists":
                    all_items.append(concert.artist.name)
                case "venues":
                    all_items.append(concert.venue.name)
                case "persons":
                    try:
                        for person in concert.persons:
                            all_items.append(person.first_name)
                    except TypeError:
                        pass
        all_items_string = ""
        frequencies = list(Counter(all_items).items())
        for item_count in sorted(frequencies, key=self.sort_ignore_case_and_the):
            all_items_string += f"* {item_count[0]}: {item_count[1]}\n"

        sg.popup(title, all_items_string, line_width=100)

    @classmethod
    def sort_ignore_case_and_the(cls, frequency):
        artist = frequency[0]
        if artist.lower().startswith("the"):
            artist = artist[4:]
        return artist.lower()
