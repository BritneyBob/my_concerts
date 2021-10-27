import os
import pickle
from datetime import datetime, timedelta
import unittest
from gui import GUI
from concert import Concert


class TestGUI(unittest.TestCase):

    def test_create_gui_with_concerts_file(self):
        gui = GUI()
        self.assertTrue(gui.concerts_list)

    def test_create_gui_without_concerts_file(self):
        os.chdir(r"C:\Users\Britta\Desktop\YH\my_concerts\without_concerts")
        gui = GUI()
        self.assertFalse(gui.concerts_list)

    def test_get_saved_concerts(self):
        os.chdir(r"C:\Users\Britta\Desktop\YH\my_concerts")
        gui = GUI()
        with open("concerts.bin", "rb") as concerts_file:
            concerts = pickle.load(concerts_file)
        concert_strings = [concert.get_concert_long_string() for concert in concerts]
        saved_concert_strings = [concert.get_concert_long_string() for concert in gui.get_saved_concerts()]
        self.assertEqual(saved_concert_strings, concert_strings)

    def test_get_remember_concert_string_more_than_one_year_ago(self):
        gui = GUI()
        concert = Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), "12 okt 2001", [], "")
        remind_string = "20 YEARS AGO...\n* 2001-10-12 you saw Dipper at Musikens Hus in Göteborg, Sweden."
        gui_remind_string = gui.get_remember_concert_string(concert)
        self.assertEqual(gui_remind_string, remind_string)

    def test_get_remember_concert_string_one_year_ago(self):
        gui = GUI()
        concert = Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), "12 okt 2020", [], "")
        remind_string = "1 YEAR AGO...\n* 2020-10-12 you saw Dipper at Musikens Hus in Göteborg, Sweden."
        gui_remind_string = gui.get_remember_concert_string(concert)
        self.assertEqual(gui_remind_string, remind_string)

    def test_get_random_concert_prev_year_this_month(self):
        os.chdir(r"C:\Users\Britta\Desktop\YH\my_concerts\concert_this_month")
        gui = GUI()
        concerts_this_month = []
        concert = Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), datetime.now().strftime("%Y-%m-%d"), [], "")
        concerts_this_month.append(concert)
        with open("concerts.bin", "wb") as concerts_file:
            pickle.dump(concerts_this_month, concerts_file)
        self.assertTrue(gui.get_random_concert_prev_year_this_month())

    def test_get_random_concert_prev_year_last_month(self):
        os.chdir(r"C:\Users\Britta\Desktop\YH\my_concerts\concert_not_this_month")
        gui = GUI()
        concerts_last_month = []
        last_month = datetime.today().replace(day=1) - timedelta(days=1)
        concert = Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), last_month.strftime("%Y-%m-%d"), [], "")
        concerts_last_month.append(concert)
        with open("concerts.bin", "wb") as concerts_file:
            pickle.dump(concerts_last_month, concerts_file)
        self.assertFalse(gui.get_random_concert_prev_year_this_month())

    # def test_add_concert(self):
    #     pass
    #
    # def test_get_country(self):
    #     pass
    #
    # def test_change(self):
    #     pass
    #
    # def test_remove(self):
    #     pass


if __name__ == "__main__":
    unittest.main()
