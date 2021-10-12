class Date:
    def __init__(self, date):
        self.date = date
        split_date = self.date.split('/')
        self.year = int(split_date[0])
        if 0 <= self.year <= 90:
            self.year = int('20' + str(self.year))
        else:
            self.year = int('19' + str(self.year))
        self.month = int(split_date[1])
        self.day = int(split_date[2])
