import pickle

from concert import Concert


class Menu:
    def __init__(self):
        self.running = True
        self.concerts = []

    def run(self):
        print("Welcome to My Concerts!")
        while self.running:
            self.display_menu()

    def display_menu(self):
        print("1. Search for a concert")
        print("2. Add a new concert")
        choice = input("What would you like to do (1-2)?: ")
        match choice:
            case '1':
                self.search_menu()
            case '2':
                self.add_concert()
            case 'quit':
                self.running = False
            case _:
                print("Please enter 1 to search a concert or 2 to add a concert")

    def search_menu(self):
        print("1. Artist")
        print("2. Arena")
        print("3. Date")
        print("4. Person")
        choice = int(input("What would you like to base your search on (1-4)?: "))
        match choice:
            case 1:
                self.search_artist()
            case 2:
                self.search_arena()
            case 3:
                self.search_date()
            case 4:
                self.search_person()

    def search_artist(self):
        name = input("What is the name of the artist?: ")
        with open('concerts.bin', 'rb') as concerts_file:
            loaded_data = pickle.load(concerts_file)
        # for concert in self.concerts:
        loaded_data.print_concert()

    def search_arena(self):
        name = input("What is the name of the arena?: ")

    def search_date(self):
        date = input("What date would you like to search for?: ")

    def search_person(self):
        name = input("Did you go with someone to the concert? If yes, please enter one or more names: ")

    def add_concert(self):
        artist = input("What is the name of the artist?: ")
        arena = input("What is the name of the arena?: ")
        date = input("What date was the concert (yy/mm/dd)?: ")
        person = input("Did you go with someone to the concert? If yes, please enter one or more names: ")
        new_concert = Concert(artist, arena, date, person)
        with open('concerts.bin', 'ab') as concerts_file:
            pickle.dump(new_concert, concerts_file)
        self.concerts.append(new_concert)
