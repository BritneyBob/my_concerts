import os
import pickle
import unittest

from datetime import datetime, timedelta

from concert import Concert
import concerts_list_ops
from gui import GUI


class TestGUI(unittest.TestCase):

    def test_gui_with_concerts_file(self):
        gui = GUI()
        self.assertTrue(gui.concerts_list)

    def test_gui_without_concerts_file(self):
        os.chdir(r"C:\Users\Britta\Desktop\YH\my_concerts\without_concerts")
        gui = GUI()
        self.assertFalse(gui.concerts_list)

    def test_get_saved_concerts(self):
        os.chdir(r"C:\Users\Britta\Desktop\YH\my_concerts")
        with open("concerts.bin", "rb") as concerts_file:
            concerts = pickle.load(concerts_file)
        concert_strings = [concert.get_concert_long_string() for concert in concerts]
        saved_concert_strings = [concert.get_concert_long_string() for concert in
                                 concerts_list_ops.get_saved_concerts()]
        self.assertEqual(saved_concert_strings, concert_strings)

    def test_get_concert_string_more_than_one_year_ago(self):
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), "12 okt 2001", [], "")]
        remind_string = "20 YEARS AGO...\n* 2001-10-12 you saw Dipper at Musikens Hus in Göteborg, Sweden."
        gui_remind_string = concerts_list_ops.get_random_concert_string(concerts)
        self.assertEqual(gui_remind_string, remind_string)

    def test_get_concert_string_one_year_ago(self):
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), "12 okt 2020", [], "")]
        remind_string = "1 YEAR AGO...\n* 2020-10-12 you saw Dipper at Musikens Hus in Göteborg, Sweden."
        gui_remind_string = concerts_list_ops.get_random_concert_string(concerts)
        self.assertEqual(gui_remind_string, remind_string)

    def test_get_concert_same_month(self):
        os.chdir(r"C:\Users\Britta\Desktop\YH\my_concerts\concert_this_month")
        concerts_this_month = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"),
                                       datetime.now().strftime("%Y-%m-%d"), [], "")]
        with open("concerts.bin", "wb") as concerts_file:
            pickle.dump(concerts_this_month, concerts_file)
        self.assertTrue(concerts_list_ops.get_random_concert_same_month(concerts_this_month))

    def test_get_concert_last_month(self):
        os.chdir(r"C:\Users\Britta\Desktop\YH\my_concerts\concert_not_this_month")
        last_month = datetime.today().replace(day=1) - timedelta(days=1)
        concerts_last_month = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"),
                                       last_month.strftime("%Y-%m-%d"), [], "")]
        with open("concerts.bin", "wb") as concerts_file:
            pickle.dump(concerts_last_month, concerts_file)
        self.assertFalse(concerts_list_ops.get_random_concert_same_month(concerts_last_month))

    def test_add_concert(self):
        pass

    def test_get_search_result(self):
        pass

    def test_get_search_result_date(self):
        pass

    def test_get_country_swedish(self):
        self.assertEqual("Sverige", concerts_list_ops.get_country("Göteborg"))

    def test_get_country_english(self):
        self.assertEqual("Sverige", concerts_list_ops.get_country("Gothenburg"))

    def test_change(self):
        pass

    def test_remove(self):
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sweden"), datetime.now().strftime("%Y-%m-%d"), [],
                            "")]
        with open("test_concert.bin", "wb") as concert_file:
            pickle.dump(concerts, concert_file)
        concerts_list_ops.remove(concerts[0], concerts)
        self.assertFalse(concerts)

    def test_get_all_concerts(self):
        pass

    def test_get_all_items(self):
        pass

    def test_sort_ignore_case_and_the(self):
        pass


if __name__ == "__main__":
    unittest.main()
