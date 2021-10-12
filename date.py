class Date:
    def __init__(self, date):
        self.date = date
        split_date = self.date.split('/')
        self.year = split_date[0]
        self.month = split_date[1]
        self.day = split_date[2]

    def get_month(self):
        return self.month

