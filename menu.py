import pickle
import random
from os.path import exists
from concert import Concert


class Menu:
    def __init__(self):
        self.running = True
        if exists('concerts.bin'):
            self.concerts_list = self.get_saved_concerts()
        else:
            self.concerts_list = []

    def run(self):
        print("Welcome! My Concerts helps you remember the concerts you have been to")
        while self.running:
            self.display_menu()

    #@staticmethod
    def get_saved_concerts(self):
        try:
            with open('concerts.bin', 'rb') as concerts_file:
                x = pickle.load(concerts_file)
                return x
        except EOFError:
            return []

    def display_menu(self):
        print("\nMAIN MENU")
        print("1. Add a new concert to your memory")
        print("2. Find a specific concert")
        print("3. Be reminded of a random concert")
        print("4. Be reminded of all concerts you have been to")
        print("5. Be reminded of all artists you have seen")
        print("6. Be reminded of all venues you have been to concerts in")
        print("7. Be reminded of all persons you have been to concerts with")
        choice = input("What would you like to do (1-7)?: ")
        print()
        match choice:
            case '1':
                self.add_concert()
            case '2':
                self.search_menu()
            case '3':
                self.concerts_list[random.randrange(len(self.concerts_list))].print_concert()
            case '4':
                print("ALL CONCERTS YOU REMEMBER")
                for concert in self.concerts_list:
                    concert.print_concert()
            case '5':
                print("ARTISTS YOU HAVE SEEN")
                all_artists = []
                for concert in self.concerts_list:
                    all_artists.append(concert.artist.name)
                for artist in set(all_artists):
                    print('*', artist)
            case '6':
                print("VENUES YOU HAVE SEEN CONCERTS IN")
                all_venues = []
                for concert in self.concerts_list:
                    all_venues.append(concert.arena.name)
                for artist in set(all_venues):
                    print('*', artist)
            case '7':
                print("PEOPLE YOU HAVE BEEN TO CONCERTS WITH")
                all_persons = []
                for concert in self.concerts_list:
                    all_persons.append(concert.person.first_name)
                for person in set(all_persons):
                    print('*', person)
            case 'quit':
                self.running = False
            case _:
                print("Please enter a choice 1-7")

    def search_menu(self):
        print("1. Artist")
        print("2. Venue")
        print("3. Date")
        print("4. Person")
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
            case _: print("Please enter a digit 1-4")

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
            for concert in found_concerts:
                concert.print_concert()
        else:
            print(f"Unfortunately you have no recollection of a concert with the artist {artist}. If you have gotten a "
                  f"new memory you can add it by choosing 1 in the main menu.")

    def search_venue(self):
        venue = input("Please enter the name of a venue: ")
        found_concerts = []
        for concert in self.concerts_list:
            if venue == concert.arena.name:
                found_concerts.append(concert)
        if len(found_concerts) > 0:
            for concert in found_concerts:
                concert.print_concert()
        else:
            print(f"Unfortunately you have no recollection of a concert at the venue {venue}. If you have gotten a new"
                  f"memory you can add it by choosing 1 in the main menu.")

    def search_date(self):
        date = input("Please enter a date: ")
        found_concerts = []
        for concert in self.concerts_list:
            if date == concert.date.date:
                found_concerts.append(concert)
        if len(found_concerts) > 0:
            for concert in found_concerts:
                concert.print_concert()
        else:
            print(f"Unfortunately you have no recollection of a concert on the date {date}. If you have gotten a new"
                  f"memory you can add it by choosing 1 in the main menu.")

    def search_person(self):
        person = input("Please enter the name of a person: ")
        found_concerts = []
        for concert in self.concerts_list:
            if person == concert.person.first_name:
                found_concerts.append(concert)
        if len(found_concerts) > 0:
            for concert in found_concerts:
                concert.print_concert()
        else:
            print(f"Unfortunately you have no recollection of a concert that you went to with someone called {person}. "
                  f"If you have gotten a new memory you can add it by choosing 1 in the main menu.")

    def add_concert(self):
        artist = input("What is the name of the artist?: ")
        venue_name = input("What is the name of the venue?: ")
        is_default_location = input(f"Is {venue_name} located in Gothenburg, Sweden? ")
        if is_default_location.lower() == 'no':
            city = input(f"In what city is {venue_name} located?: ")
            country = input(f"In what country is {city} located?: ")
            arena = (venue_name, city, country)
        elif is_default_location.lower() == 'yes':
            venue = venue_name
        date = input("What date was the concert (yy/mm/dd)?: ")
        persons = input("Did you go with someone to the concert? If yes, please enter one or more names: ").split()
        new_concert = Concert(artist, venue, date, persons)
        self.concerts_list.append(new_concert)
        with open('concerts.bin', 'wb') as concerts_file:
            pickle.dump(self.concerts_list, concerts_file)
