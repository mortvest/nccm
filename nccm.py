import datetime
import argparse
from canteen import *
# TODO Add support for printing tables
# TODO Finish exception handling

WEEKDAYS = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag"]
TODAY = datetime.date.today().weekday()
CANTEEN_LIST = [BioCanteen("Biocenter",    "http://www.biocenter.ku.dk/kantine/menuoversigt/"),
                BioCanteen("August Krogh", "http://www1.bio.ku.dk/akb/kantine/menuoversigt/")]

def get_for_a_day(date, dishes):
    return [x for x in dishes if (x.date == date)]

def get_for_a_canteen(canteen, dishes):
    return [x for x in dishes if (x.canteen == canteen)]

def print_for_day(day,lst):
    dishes = get_for_a_day(lst,day)
    print("* " + dishes[0].date)
    for canteen in CANTEEN_LIST:
        foo = get_for_a_canteen(canteen.name, dishes)
        print("** " + foo[0].canteen)
        for dish in foo:
            print(str(dish))

def print_for_week(dishes):
    if len(dishes)>1:
        print("Week menu:")
        for day in WEEKDAYS:
            print_for_day(dishes, day)

def print_for_today(dishes):
    if len(dishes)>1:
        print("Menu for today:")
        weekday = WEEKDAYS[TODAY]
        print_for_day(dishes,weekday)

def load_all(canteen_list):
    pool = []
    for canteen in canteen_list:
        try:
            canteen.fill_pool(pool)
        except:
            print("Failed loading menu from " + canteen.name)
    return pool

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-w", "--week", help="show menu for week and exit",
                    action="store_true")
    group.add_argument("-t", "--today", help="show menu for today and exit (default)",
                    action="store_true")
    args = parser.parse_args()
    if args.week:
        print_for_week(load_all(CANTEEN_LIST))
    else:
        if TODAY > 4:
            print("Nothing to load, the canteens are closed for today")
        else:
            print_for_today(load_all(CANTEEN_LIST))
    # TODO add support for choosing canteens and days
