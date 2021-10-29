import os
import pickle
import random
import unittest

from datetime import datetime, timedelta


from concert import Concert
import concerts_operations
from gui import GUI


class TestGUI(unittest.TestCase):
    def setUp(self):
        self.concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), "12 okt 2001", ["Alex", "Erik"], ""),
                         Concert("Nationalteatern", ("Liseberg", "Göteborg", "Sweden"), "13 jul 2005", [], ""),
                         Concert("Bob Dylan", ("Cirkus", "Stockholm", "Sweden"), "1 mar 2019", ["Tråkig!"], ""),
                         Concert("Britney Spears", ("Globen", "Stockholm", "Sweden"), "17 maj 2016", [], ""),
                         Concert("Blur", ("Ullevi", "Göteborg", "Sweden"), "20 maj 1995", [], "")]

    def test_gui_with_concerts_file(self):
        gui = GUI()
        self.assertTrue(gui.concerts_list)

    def test_gui_without_concerts_file(self):
        os.chdir(r"C:\Users\Britta\Desktop\YH\my_concerts\tests\without_concerts")
        gui = GUI()
        self.assertFalse(gui.concerts_list)

    def test_get_saved_concerts(self):
        os.chdir(r"C:\Users\Britta\Desktop\YH\my_concerts\tests")
        with open("concerts.bin", "wb") as concerts_file:
            pickle.dump(self.concerts, concerts_file)
        concert_strings = [concert.get_concert_long_string() for concert in self.concerts]
        saved_concert_strings = [concert.get_concert_long_string() for concert in
                                 concerts_operations.get_saved_concerts("concerts.bin")]
        self.assertEqual(saved_concert_strings, concert_strings)

    def test_get_concert_string_more_than_one_year_ago(self):
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), "12 okt 2001", [], "")]
        remind_string = "20 YEARS AGO...\n* 2001-10-12 you saw Dipper at Musikens Hus in Göteborg, Sweden."
        gui_remind_string = concerts_operations.get_random_concert_string(concerts)
        self.assertEqual(gui_remind_string, remind_string)

    def test_get_concert_string_one_year_ago(self):
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), "12 okt 2020", [], "")]
        remind_string = "1 YEAR AGO...\n* 2020-10-12 you saw Dipper at Musikens Hus in Göteborg, Sweden."
        gui_remind_string = concerts_operations.get_random_concert_string(concerts)
        self.assertEqual(gui_remind_string, remind_string)

    def test_get_concert_same_month(self):
        concerts_this_month = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"),
                                       datetime.now().strftime("%Y-%m-%d"), [], "")]
        with open("concerts_this_month.bin", "wb") as concerts_file:
            pickle.dump(concerts_this_month, concerts_file)
        self.assertTrue(concerts_operations.get_random_concert_same_month(concerts_this_month))

    def test_get_concert_last_month(self):
        last_month = datetime.today().replace(day=1) - timedelta(days=1)
        concerts_last_month = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"),
                                       last_month.strftime("%Y-%m-%d"), [], "")]
        with open("concerts_last_month.bin", "wb") as concerts_file:
            pickle.dump(concerts_last_month, concerts_file)
        self.assertFalse(concerts_operations.get_random_concert_same_month(concerts_last_month))

    def test_add_concert(self):
        concert = Concert("Björk", ("Roskilde festival, Roskilde, Danmark"), "3 jul 2005", [], "")
        added_concert = concerts_operations.add_concert(["Björk", ("Roskilde festival, Roskilde, Danmark"),
                                                         "3 jul 2005", [], ""],
                                                        self.concerts, "concerts.bin")
        self.assertEqual(concert, added_concert)

    def test_get_search_result(self):
        pass

    def test_get_search_result_date(self):
        pass

    def test_get_country_swedish(self):
        self.assertEqual("Sverige", concerts_operations.get_country("Göteborg"))

    def test_get_country_english(self):
        self.assertEqual("Sverige", concerts_operations.get_country("Gothenburg"))

    def test_change(self):
        pass

    def test_remove_from_list(self):
        concert = self.concerts[random.randint(0, len(self.concerts))]
        self.concerts = concerts_operations.remove(concert, self.concerts, "concerts.bin")
        self.assertNotIn(concert, self.concerts)

    def test_remove_from_file(self):
        concert = self.concerts[random.randint(0, len(self.concerts))]
        concerts_operations.remove(concert, self.concerts, "test_remove_concert.bin")

        with open("test_remove_concert.bin", "rb") as concert_file:
            saved_concerts = pickle.load(concert_file)

        self.assertNotIn(concert, saved_concerts)

    def test_get_all_concerts(self):
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), "12 okt 2001", [], "Kul!"),
                    Concert("Nationalteatern", ("Liseberg", "Göteborg", "Sweden"), "13 jul 2005", ["Erik", "Alex"], "")]
        concerts_string = "2001-10-12: Dipper, Musikens Hus\n" \
                          "2005-07-13: Nationalteatern, Liseberg\n"
        self.assertEqual(concerts_string, concerts_operations.get_all_concerts(concerts))

    def test_get_all_artists(self):
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), "12 okt 2001", [], "Kul!"),
                    Concert("Nationalteatern", ("Liseberg", "Göteborg", "Sweden"), "13 jul 2005", ["Erik", "Alex"], "")]
        all_artists = "* Dipper: 1\n* Nationalteatern: 1\n"
        self.assertEqual(all_artists, concerts_operations.get_all_items("artists", concerts))

    def test_get_all_venues(self):
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), "12 okt 2001", [], "Kul!"),
                    Concert("Nationalteatern", ("Liseberg", "Göteborg", "Sweden"), "13 jul 2005", ["Erik", "Alex"], "")]
        all_venues = "* Liseberg: 1\n* Musikens Hus: 1\n"
        self.assertEqual(all_venues, concerts_operations.get_all_items("venues", concerts))

    def test_get_all_persons(self):
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), "12 okt 2001", [], "Kul!"),
                    Concert("Nationalteatern", ("Liseberg", "Göteborg", "Sweden"), "13 jul 2005", ["Erik", "Alex"], "")]
        all_persons = "* Alex: 1\n* Erik: 1\n"
        self.assertEqual(all_persons, concerts_operations.get_all_items("persons", concerts))

    def test_sort_ignore_case_and_the(self):

        concerts_operations.sort_ignore_case_and_the("The Rolling Stones", 2)


if __name__ == "__main__":
    unittest.main()
