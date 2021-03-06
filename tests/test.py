import os
import pickle
import random
import unittest

from datetime import datetime, timedelta
from dateparser import parse
from dateutil.relativedelta import relativedelta


from concert import Concert
import concerts_operations
from gui import GUI


class TestGUI(unittest.TestCase):
    def test_gui_with_concerts_file(self):
        gui = GUI()
        self.assertTrue(gui.concerts_list)

    def test_gui_without_concerts_file(self):
        os.chdir(os.getcwd() + "\\without_concerts")
        gui = GUI()
        self.assertFalse(gui.concerts_list)


class TestConcertsOperations(unittest.TestCase):
    def setUp(self):
        self.concerts = [
            Concert("Dipper", ("Musikens Hus", "Göteborg", "Sverige"), "12 okt 2001", ["Alex", "Erik"], ""),
            Concert("Nationalteatern", ("Liseberg", "Göteborg", "Sverige"), "13 jul 2005", [], ""),
            Concert("Bob Dylan", ("Globen", "Stockholm", "Sverige"), "1 mar 2019", [], "Tråkig."),
            Concert("Britney Spears", ("Globen", "Stockholm", "Sverige"), "17 maj 2016", [], "Britney är ett proffs!"),
            Concert("Blur", ("Ullevi", "Göteborg", "Sverige"), "20 maj 1995", ["Tomten", "Jesus"], "Wohoo!"),
            Concert("The Beatles", ("Lisebergshallen", "Göteborg", "Sverige"), "3 feb 1964", ["Dalai Lama"], ""),
            Concert("Blur", ("Roskilde festival", "Roskilde", "Danmark"), "4 jul 2005", ["Julius Caesar", "Tomten"], "")
        ]

    def test_get_saved_concerts(self):
        with open("concerts.bin", "wb") as concerts_file:
            pickle.dump(self.concerts, concerts_file)
        saved_concerts = concerts_operations.get_saved_concerts("concerts.bin")
        self.assertEqual(self.concerts, saved_concerts)

    def test_get_concert_string_more_than_one_year_ago(self):
        twenty_yrs_ago = (datetime.now() - relativedelta(years=20)).strftime('%Y-%m-%d')
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sverige"), twenty_yrs_ago, [], "")]
        remind_string = f"20 YEARS AGO...\n* {twenty_yrs_ago} " \
                        f"you saw Dipper at Musikens Hus in Göteborg, Sverige."
        gui_remind_string = concerts_operations.get_random_concert_string(concerts)
        self.assertEqual(gui_remind_string, remind_string)

    def test_get_concert_string_one_year_ago(self):
        one_year_ago = (datetime.now() - relativedelta(years=1)).strftime('%Y-%m-%d')
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sverige"), one_year_ago, [], "")]
        remind_string = f"1 YEAR AGO...\n* {one_year_ago} " \
                        f"you saw Dipper at Musikens Hus in Göteborg, Sverige."
        gui_remind_string = concerts_operations.get_random_concert_string(concerts)
        self.assertEqual(gui_remind_string, remind_string)

    def test_get_concert_string_this_year(self):
        concerts = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sverige"), datetime.now().strftime("%Y-%m-%d"), [],
                            "")]
        remind_string = f"RECENTLY...\n* {datetime.now().strftime('%Y-%m-%d')} " \
                        f"you saw Dipper at Musikens Hus in Göteborg, Sverige."
        gui_remind_string = concerts_operations.get_random_concert_string(concerts)
        self.assertEqual(gui_remind_string, remind_string)

    def test_get_concert_same_month(self):
        concerts_this_month = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sverige"),
                                       datetime.now().strftime("%Y-%m-%d"), [], "")]
        with open("concerts_this_month.bin", "wb") as concerts_file:
            pickle.dump(concerts_this_month, concerts_file)
        self.assertTrue(concerts_operations.get_random_concert_same_month(concerts_this_month))

    def test_get_concert_last_month(self):
        last_month = datetime.today().replace(day=1) - timedelta(days=1)
        concerts_last_month = [Concert("Dipper", ("Musikens Hus", "Göteborg", "Sverige"),
                                       last_month.strftime("%Y-%m-%d"), [], "")]
        with open("concerts_last_month.bin", "wb") as concerts_file:
            pickle.dump(concerts_last_month, concerts_file)
        self.assertFalse(concerts_operations.get_random_concert_same_month(concerts_last_month))

    def test_add_concert(self):
        concert = Concert("Björk", ("Roskilde festival", "Roskilde", "Danmark"), "3 jul 2005", [], "")
        added_concert, _ = concerts_operations.add_concert(["Björk", "Roskilde festival", "Roskilde", "3 jul 2005", "",
                                                            ""], self.concerts, "concerts.bin")
        self.assertEqual(concert, added_concert)

    def test_add_concert_to_list(self):
        _, concerts_list = concerts_operations.add_concert(["Björk", "Roskilde festival", "Roskilde", "3 jul 2005", "",
                                                            ""], self.concerts, "concerts.bin")
        self.assertEqual(self.concerts, concerts_list)

    def test_add_concert_string(self):
        added_concert, _ = concerts_operations.add_concert(["Björk", "Roskilde festival", "Roskilde", "3 jul 2005", "",
                                                            ""], self.concerts, "concerts.bin")
        expected_string = "* 2005-07-03 you saw Björk at Roskilde festival in Roskilde, Danmark."
        self.assertEqual(expected_string, added_concert.get_concert_long_string())

    def test_add_concert_string_two_persons(self):
        added_concert, _ = concerts_operations.add_concert(["Björk", "Roskilde festival", "Roskilde", "3 jul 2005",
                                                            "John F Kennedy, Mahatma Gandhi", ""],
                                                           self.concerts, "concerts.bin")
        expected_string = "* 2005-07-03 you saw Björk at Roskilde festival in Roskilde, Danmark.\n" \
                          "  You were there with John F Kennedy and Mahatma Gandhi."
        self.assertEqual(expected_string, added_concert.get_concert_long_string())

    def test_add_concert_string_more_persons(self):
        added_concert, _ = concerts_operations.add_concert(["Björk", "Roskilde festival", "Roskilde", "3 jul 2005",
                                                            "John F Kennedy, Mahatma Gandhi, Snoop Dogg", ""],
                                                           self.concerts, "concerts.bin")
        expected_string = "* 2005-07-03 you saw Björk at Roskilde festival in Roskilde, Danmark.\n" \
                          "  You were there with John F Kennedy, Mahatma Gandhi and Snoop Dogg."
        self.assertEqual(expected_string, added_concert.get_concert_long_string())

    def test_add_concert_string_one_person_note(self):
        added_concert, _ = concerts_operations.add_concert(["Björk", "Roskilde festival", "Roskilde", "3 jul 2005",
                                                            "John F Kennedy", "Amazing."],
                                                           self.concerts, "concerts.bin")
        expected_string = "* 2005-07-03 you saw Björk at Roskilde festival in Roskilde, Danmark.\n" \
                          "  You were there with John F Kennedy.\n" \
                          "  Notes: Amazing."
        self.assertEqual(expected_string, added_concert.get_concert_long_string())

    def test_add_concert_string_note(self):
        added_concert, _ = concerts_operations.add_concert(["Björk", "Roskilde festival", "Roskilde", "3 jul 2005",
                                                            "", "Amazing."], self.concerts, "concerts.bin")
        expected_string = "* 2005-07-03 you saw Björk at Roskilde festival in Roskilde, Danmark.\n" \
                          "  Notes: Amazing."
        self.assertEqual(expected_string, added_concert.get_concert_long_string())

    def test_get_search_result_artist_true(self):
        found_concerts, _ = concerts_operations.get_search_result("artist", ["Beatles"], self.concerts)
        expected_concerts = [self.concerts[5]]
        self.assertEqual(expected_concerts, found_concerts)

    def test_get_search_result_artist_false(self):
        found_concerts, _ = concerts_operations.get_search_result("artist", ["Toto"], self.concerts)
        expected_concerts = []
        self.assertEqual(expected_concerts, found_concerts)

    def test_get_search_result_venue_true(self):
        found_concerts, _ = concerts_operations.get_search_result("venue", ["Globen"], self.concerts)
        expected_concerts = [self.concerts[2], self.concerts[3]]
        self.assertEqual(expected_concerts, found_concerts)

    def test_get_search_result_venue_false(self):
        found_concerts, _ = concerts_operations.get_search_result("venue", ["Loppen"], self.concerts)
        expected_concerts = []
        self.assertEqual(expected_concerts, found_concerts)

    def test_get_search_result_person_true(self):
        found_concerts, _ = concerts_operations.get_search_result("person", ["Tomten"], self.concerts)
        expected_concerts = [self.concerts[4], self.concerts[6]]
        self.assertEqual(expected_concerts, found_concerts)

    def test_get_search_result_person_false(self):
        found_concerts, _ = concerts_operations.get_search_result("person", ["Knugen"], self.concerts)
        expected_concerts = []
        self.assertEqual(expected_concerts, found_concerts)

    def test_get_search_result_date_true(self):
        found_concerts, _, _ = concerts_operations.get_search_result_date(["17 maj 2016"], self.concerts)
        expected_concerts = [self.concerts[3]]
        self.assertEqual(expected_concerts, found_concerts)

    def test_get_search_result_date_false(self):
        found_concerts, _, _ = concerts_operations.get_search_result_date(["23 jul 1986"], self.concerts)
        expected_concerts = []
        self.assertEqual(expected_concerts, found_concerts)

    def test_get_search_result_date_range_true(self):
        date1 = parse("2016", settings={"PREFER_DAY_OF_MONTH": "first"})
        date2 = parse("2020", settings={"PREFER_DAY_OF_MONTH": "last"})
        found_concerts, _, _ = concerts_operations.get_search_result_date((date1, date2), self.concerts)
        expected_concerts = [self.concerts[2]]
        self.assertEqual(expected_concerts, found_concerts)

    def test_get_search_result_date_range_false(self):
        date1 = parse("1980", settings={"PREFER_DAY_OF_MONTH": "first"})
        date2 = parse("1989", settings={"PREFER_DAY_OF_MONTH": "last"})
        found_concerts, _, _ = concerts_operations.get_search_result_date((date1, date2), self.concerts)
        expected_concerts = []
        self.assertEqual(expected_concerts, found_concerts)

    def test_get_country_swedish(self):
        self.assertEqual("Sverige", concerts_operations.get_country("Göteborg"))

    def test_get_country_english(self):
        self.assertEqual("Sverige", concerts_operations.get_country("Gothenburg"))

    def test_change(self):
        changed_concert, self.concerts = \
            concerts_operations.change(["The Beatles", "Cirkus", "Stockholm", "Sverige", "4 feb 1964",
                                        "Dalai Lama, Mick Jagger", "Don't believe the hype"],
                                       self.concerts[5], self.concerts, "concerts.bin")
        self.assertEqual(self.concerts[-1], changed_concert)

    def test_change_string(self):
        changed_concert, self.concerts = \
            concerts_operations.change(["The Beatles", "Cirkus", "Stockholm", "Sverige", "4 feb 1964",
                                        "Dalai Lama, Mick Jagger", "Don't believe the hype"],
                                       self.concerts[5], self.concerts, "concerts.bin")
        expected_string = "* 1964-02-04 you saw The Beatles at Cirkus in Stockholm, Sverige.\n" \
                          "  You were there with Dalai Lama and Mick Jagger.\n" \
                          "  Notes: Don't believe the hype"
        self.assertEqual(expected_string, self.concerts[-1].get_concert_long_string())

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
        concerts_string = "* 1964-02-03: The Beatles, Lisebergshallen \n" \
                          "* 1995-05-20: Blur, Ullevi \n" \
                          "* 2001-10-12: Dipper, Musikens Hus \n" \
                          "* 2005-07-04: Blur, Roskilde festival \n" \
                          "* 2005-07-13: Nationalteatern, Liseberg \n" \
                          "* 2016-05-17: Britney Spears, Globen \n" \
                          "* 2019-03-01: Bob Dylan, Globen \n"
        self.assertEqual(concerts_string, concerts_operations.get_all_concerts(self.concerts))

    def test_get_all_artists(self):
        all_artists = "* The Beatles: 1\n" \
                      "* Blur: 2\n" \
                      "* Bob Dylan: 1\n" \
                      "* Britney Spears: 1\n" \
                      "* Dipper: 1\n" \
                      "* Nationalteatern: 1\n"
        self.assertEqual(all_artists, concerts_operations.get_all_items("artists", self.concerts))

    def test_get_all_venues(self):
        all_venues = "* Globen: 2\n" \
                     "* Liseberg: 1\n" \
                     "* Lisebergshallen: 1\n" \
                     "* Musikens Hus: 1\n" \
                     "* Roskilde festival: 1\n" \
                     "* Ullevi: 1\n"
        self.assertEqual(all_venues, concerts_operations.get_all_items("venues", self.concerts))

    def test_get_all_persons(self):
        all_persons = "* Alex: 1\n" \
                      "* Dalai Lama: 1\n" \
                      "* Erik: 1\n" \
                      "* Jesus: 1\n" \
                      "* Julius Caesar: 1\n" \
                      "* Tomten: 2\n"
        self.assertEqual(all_persons, concerts_operations.get_all_items("persons", self.concerts))

    def test_sort_ignore_case_with_the(self):
        self.assertEqual("rolling stones", concerts_operations.sort_ignore_case_and_the(("The Rolling Stones", 2)))

    def test_sort_ignore_case_without_the(self):
        self.assertEqual("therapy?", concerts_operations.sort_ignore_case_and_the(("Therapy?", 1)))


if __name__ == "__main__":
    unittest.main()
