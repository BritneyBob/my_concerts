from concerts import Concerts


class Menu:
    def __init__(self):
        self.concerts = Concerts()

    def run(self):
        self.display()

    def display(self):
        print("Welcome to My Concerts!")
        print("1. Search for a concert")
        print("2. Add a new concert")
        choice = int(input("What would you like to do (1-2)?: "))
        match choice:
            case 1:
                self.concerts.search()
            case 2:
                self.concerts.add()
