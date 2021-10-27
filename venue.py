class Venue:
    def __init__(self, name, city, country):
        self.name = name
        self.city = city
        self.country = country

    def __str__(self):
        return f"{self.name} in {self.city}, {self.country}."
