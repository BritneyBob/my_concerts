import random

from dateparser import parse
import PySimpleGUI as sg

import concerts_operations


class GUI:
    def __init__(self):
        self.running = True
        self.concerts_file = "concerts.bin"
        self.concerts_list = concerts_operations.get_saved_concerts(self.concerts_file)

    def run_window(self):
        random_concert_to_display = concerts_operations.get_random_concert_string(self.concerts_list)
        window = self.display_main_menu(random_concert_to_display)
        self.process_user_click(window)

    def display_main_menu(self, concert_to_remind_of_string):
        if len(self.concerts_list) > 0:
            welcome_string = "Welcome! My Concerts helps you remember the concerts you have been to.\n\n" + \
                             concert_to_remind_of_string + "\n"
        else:
            welcome_string = "Welcome! My Concerts helps you remember the concerts you have been to.\n"

        layout = [[sg.Text(welcome_string)],
                  [sg.Button("Add concert"), sg.Button("Search for concert"), sg.Button("Random concert")],
                  [sg.Text("SEE ALL:"), sg.Button("Concerts"), sg.Button("Artists"), sg.Button("Venues"),
                   sg.Button("Persons")],
                  [sg.Stretch(), sg.Button("Quit")]]

        return sg.Window("My Concerts", layout)

    def process_user_click(self, window):
        while True:
            event, values = window.read()

            match event:
                case sg.WIN_CLOSED | "Quit":
                    break

                case "Add concert":
                    new_concert, self.concerts_list = self.display_add_menu()
                    sg.popup("The new concert was added to your memory", new_concert.get_concert_long_string())

                case "Search for concert":
                    self.display_search_menu()

                case "Random concert":
                    sg.popup(self.concerts_list[random.randrange(len(self.concerts_list))].get_concert_long_string(),
                             title="Random Concert", line_width=100)

                case "Concerts":
                    all_concerts = concerts_operations.get_all_concerts(self.concerts_list)
                    sg.popup("All concerts you have seen:", all_concerts, line_width=100)

                case "Artists":
                    all_artists = concerts_operations.get_all_items("artists", self.concerts_list)
                    sg.popup("Number of concerts you have been to with each artist:", all_artists, line_width=100)

                case "Venues":
                    all_venues = concerts_operations.get_all_items("venues", self.concerts_list)
                    sg.popup("Number of concerts you have been to at each venue:", all_venues, line_width=100)

                case "Persons":
                    all_persons = concerts_operations.get_all_items("persons", self.concerts_list)
                    sg.popup("Number of concerts you have been to together with each person:", all_persons,
                             line_width=100)
        window.close()

    def display_add_menu(self):
        layout = [[sg.Text("Artist"), sg.Input()],
                  [sg.Text("Venue"), sg.Input()],
                  [sg.Text("City"), sg.Input()],
                  [sg.Text("Date"), sg.Input()],
                  [sg.Text("Person/s you went with\n(optional)\n(separate with comma)"), sg.Multiline()],
                  [sg.Text("Note\n(optional)"), sg.Multiline()],
                  [sg.Button("OK"), sg.Button("Back")]]
        window = sg.Window("Add concert", layout, element_justification="r", modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | "Back":
                    break

                case "OK":
                    if values[0] and values[1] and values[2] and values[3]:
                        try:
                            parse(values[3]).strftime("%Y-%m-%d")
                            window.close()
                            return concerts_operations.add_concert(values, self.concerts_list, self.concerts_file)
                        except AttributeError:
                            sg.popup("Incorrect date input", "Please enter date in another format")

                    else:
                        sg.popup("Please enter artist, venue, city and date")
        window.close()

    def display_search_menu(self):
        layout = [[sg.Text("Search"), sg.Input()],
                  [sg.Radio("Artist", "RADIO1", default=True, key="ARTIST"),
                   sg.Radio("Venue", "RADIO1", key="VENUE"),
                   sg.Radio("Person", "RADIO1", key="PERSON"),
                   sg.Button("Search by date (new window)")],
                  [sg.Stretch(), sg.Button("OK"), sg.Button("Back"), sg.Stretch()]]

        window = sg.Window("Search concert", layout, modal=True)

        search = ""
        search_string = ""
        found_concerts = []

        while True:
            event, window_values = window.read()
            match event:
                case sg.WIN_CLOSED | "Back":
                    break

                case "OK":
                    search = list(window_values.keys())[list(window_values.values()).index(True)].lower()
                    found_concerts, search_string = \
                        concerts_operations.get_search_result(search, window_values, self.concerts_list)

                case "Search by date (new window)":
                    search = "date"
                    values = self.display_date_search_menu()
                    found_concerts, search_string, two_dates = \
                        concerts_operations.get_search_result_date(values, self.concerts_list)
                    if two_dates:
                        search_string = values

            if len(found_concerts) > 0:
                self.display_found(found_concerts)
            else:
                self.display_not_found(search, search_string)

        window.close()

    @classmethod
    def display_date_search_menu(cls):
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
                            window.close()
                            return values
                        except AttributeError:
                            sg.popup(incorrect_string)

                    elif values[1] and values[2]:
                        try:
                            date1 = parse(values[1], settings={"PREFER_DAY_OF_MONTH": "first"})
                            date2 = parse(values[2], settings={"PREFER_DAY_OF_MONTH": "last"})
                            window.close()
                            return date1, date2
                        except AttributeError:
                            sg.popup(incorrect_string)

                    else:
                        sg.popup("Please enter one or two dates")

    def display_found(self, found_concerts):
        print_concerts_string = ""
        for concert in sorted(found_concerts, key=lambda c: c.date):
            print_concerts_string += concert.get_concert_long_string() + "\n\n"
        layout = [[sg.Text(print_concerts_string)],
                  [sg.Button("Back"), sg.Stretch(), sg.Button("Change"), sg.Button("Remove")]]

        window = sg.Window("Search result", layout, modal=True)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED | "Back":
                    break
                case "Change":
                    self.display_choose_concert(found_concerts, "change")
                case "Remove":
                    self.display_choose_concert(found_concerts, "remove")
        window.close()

    @classmethod
    def display_not_found(cls, sort_to_search, search_string):
        no_memory_string = ""
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

    def display_choose_concert(self, found_concerts, change_or_remove):
        target_concert = None

        if len(found_concerts) > 1:
            layout = [[sg.Text("Please select a concert:")],
                      *[[sg.Button(str(concert))]
                        for concert in sorted(found_concerts, key=lambda c: c.date)]]
            window = sg.Window("Choose concert", layout, modal=True)

            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    break

                for concert in found_concerts:
                    if window[event].get_text() == str(concert):
                        window.close()
                        target_concert = concert
            window.close()

        else:
            target_concert = found_concerts[0]

        if target_concert:
            if change_or_remove == "change":
                self.display_change(target_concert)

            elif change_or_remove == "remove":
                if self.display_is_sure(target_concert):
                    sg.popup("The chosen concert was removed.")
                    self.concerts_list = \
                        concerts_operations.remove(target_concert, self.concerts_list, self.concerts_file)

    def display_change(self, concert):
        try:
            persons_list = [person for person in concert.persons]
        except TypeError:
            persons_list = []
        try:
            note = concert.note.note
        except AttributeError:
            note = ""

        layout = [[sg.Text("Artist"), sg.Input(concert.artist)],
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
                    changed_concert, self.concerts_list = \
                        concerts_operations.change(values, concert, self.concerts_list, self.concerts_file)
                    sg.popup("The concert was altered with the new facts:", changed_concert.get_concert_long_string(),
                             line_width=100)
        window.close()

    @classmethod
    def display_is_sure(cls, concert):
        layout = [[sg.Text("Are you sure you want to remove this concert?:")],
                  [sg.Text(str(concert))],
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
