from concerts import Concerts


class Menu:
    def __init__(self):
        self.concerts = Concerts()
        self.running = True

    def run(self):
        while self.running:
            self.display_menu()

    def display_menu(self):
        print("Welcome to My Concerts!")
        print("1. Search for a concert")
        print("2. Add a new concert")
        choice = input("What would you like to do (1-2)?: ")
        match choice:
            case '1':
                self.search_menu()
            case '2':
                self.concerts.add()
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
                self.concerts.search_artist()
            case 2:
                self.concerts.search_arena()
            case 3:
                self.concerts.search_date()
            case 4:
                self.concerts.search_person()
