class Date:
    def __init__(self, date):
        self.date = date
        # self.year = None
        # self.month = None
        # self.day = None

    def get_year(self):
        return self.date.split('/')[0]

    def get_month(self):
        return self.date.split('/')[1]

    def get_day(self):
        return self.date.split('/')[0]
