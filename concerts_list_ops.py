from collections import Counter
from os.path import exists
import pickle
import random
import re

from datetime import datetime
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

from concert import Concert


def get_saved_concerts():
    if exists("concerts.bin"):
        with open("concerts.bin", "rb") as concerts_file:
            saved_concerts = pickle.load(concerts_file)
            return saved_concerts
    else:
        return []


def get_random_concert_string(concerts_list):
    concert_to_print = get_random_concert_same_month(concerts_list)
    years_since_concert = datetime.now().year - concert_to_print.date.year
    remind_string = ''

    match years_since_concert:
        case 0:
            remind_string += f"RECENTLY...\n"
        case 1:
            remind_string += f"1 YEAR AGO...\n"
        case _:
            remind_string += f"{years_since_concert} YEARS AGO...\n"
    concert_string = concert_to_print.get_concert_long_string()

    return remind_string + concert_string


def get_random_concert_same_month(concerts_list):
    current_month = datetime.now().month
    concerts_this_month_prev_years = []

    for concert in concerts_list:
        try:
            if current_month == concert.date.month:
                concerts_this_month_prev_years.append(concert)
        except AttributeError:
            pass

    if len(concerts_this_month_prev_years) == 0:
        return None

    return concerts_this_month_prev_years[random.randrange(len(concerts_this_month_prev_years))]


def get_country(city):
    locator = Nominatim(user_agent="geoapiExercises")
    location = locator.geocode(city)
    regex = re.compile(r"[^,]*$")
    return regex.findall(location.raw["display_name"])[0].lstrip()


def add_concert(values, concerts_list):
    try:
        country = get_country(values[2])
    except GeocoderTimedOut:
        country = "Country couldn't be fetched due to a time out error"

    artist = values[0]
    venue = (values[1], values[2], country)
    date = values[3]
    persons = values[4].split(', ') if values[4] != '' else []
    note = values[5]

    new_concert = Concert(artist, venue, date, persons, note)
    concerts_list.append(new_concert)
    with open("concerts.bin", "wb") as concerts_file:
        pickle.dump(concerts_list, concerts_file)

    return new_concert, concerts_list


def change(values, concert, concerts_list):
    artist = values[0]
    venue = values[1]
    city = values[2]
    country = values[3]
    date = values[4]
    persons = values[5].split(", ") if values[5] != "" else []
    note = values[6]

    changed_concert = Concert(artist, (venue, city, country), date, persons, note)
    concerts_list.append(changed_concert)
    concerts_list.remove(concert)

    with open("concerts.bin", "wb") as concerts_file:
        pickle.dump(concerts_list, concerts_file)

    return changed_concert, concerts_list


def remove(concert, concerts_list):
    concerts_list.remove(concert)

    with open("concerts.bin", "wb") as concerts_file:
        pickle.dump(concerts_list, concerts_file)

    return concerts_list


def get_all_concerts(concerts_list):
    all_concerts = ""
    try:
        for concert in sorted(concerts_list, key=lambda c: c.date):
            all_concerts += str(concert) + "\n"
    except TypeError:
        pass

    return all_concerts


def get_all_items(items, concerts_list):
    all_items = []
    for concert in concerts_list:
        match items:
            case "artists":
                all_items.append(concert.artist.name)
            case "venues":
                all_items.append(concert.venue.name)
            case "persons":
                try:
                    for person in concert.persons:
                        all_items.append(person.first_name)
                except TypeError:
                    pass
    all_items_string = ""
    frequencies = list(Counter(all_items).items())
    for item_count in sorted(frequencies, key=sort_ignore_case_and_the):
        all_items_string += f"* {item_count[0]}: {item_count[1]}\n"

    return all_items_string


def sort_ignore_case_and_the(frequency):
    artist = frequency[0]
    if artist.lower().startswith("the"):
        artist = artist[4:]
    return artist.lower()
