import datetime
import argparse
from canteen import *

# TODO: Add logging (the proper way)
# TODO: Add support for choosing canteens and days
WEEKDAYS = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag"]
TODAY = datetime.date.today().weekday()
CANTEEN_LIST = [BioCanteen("Biocenter",    "http://www.biocenter.ku.dk/kantine/menuoversigt/"),
                BioCanteen("August Krogh", "http://www1.bio.ku.dk/akb/kantine/menuoversigt/")]
LOGO = ("""\

███╗   ██╗ ██████╗ ██████╗███╗   ███╗
████╗  ██║██╔════╝██╔════╝████╗ ████║
██╔██╗ ██║██║     ██║     ██╔████╔██║
██║╚██╗██║██║     ██║     ██║╚██╔╝██║
██║ ╚████║╚██████╗╚██████╗██║ ╚═╝ ██║
╚═╝  ╚═══╝ ╚═════╝ ╚═════╝╚═╝     ╚═╝""")

def find_max_len(lst):
    return max([len(x.item_type) for x in lst])

def get_for_a_day(date, items):
    return [x for x in items if x.date == date]

def get_for_a_canteen(canteen, items):
    return [x for x in items if x.canteen == canteen]

def print_for_day(day, lst, canteen_list, max_len):
    items = get_for_a_day(lst, day)
    if items:
        print(items[0].date)
        for canteen in canteen_list:
            cant_items = get_for_a_canteen(canteen.name, items)
            print("  " + cant_items[0].canteen)
            for item in cant_items:
                print("    " +
                      item.item_type[:-1] +
                      (max_len - len(item.item_type)) * " " +
                      ": " + item.item_name)

def print_for_week(items, canteen_list):
    if len(items) > 1:
        print("MENU FOR WEEK " + str(datetime.date.today().isocalendar()[1]))
        for day in WEEKDAYS:
            max_len = find_max_len(items)
            print_for_day(items, day, canteen_list, max_len)

def print_for_today(items, canteen_list):
    if len(items) > 1:
        print("MENU FOR TODAY: " + str(datetime.date.today()))
        weekday = WEEKDAYS[TODAY]
        max_len = find_max_len(items)
        print_for_day(items, weekday, canteen_list, max_len)

def load_all(canteen_list):
    """ Load menu for all canteens in a list, returns a list of MenuItem"""
    pool = []
    active_canteens = []
    max_name_len = max([len(x.name) for x in canteen_list])
    for canteen in canteen_list:
        msg = "Loading from " + canteen.name + (max_name_len - len(canteen.name)) * " "
        try:
            curr_lst = []
            active_canteens.append(canteen)
            canteen.fill_pool(curr_lst)
            if not args.clean:
                print (msg + ": success")
            pool += curr_lst
        except Exception as exception:
            if args.debug:
                print(exception)
            elif not args.clean:
                print(msg + ": failed")
    if not args.clean:
        print("")
    return (pool, active_canteens)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-w", "--week", help="show menu for week and exit",
                       action="store_true")
    group.add_argument("-t", "--today", help="show menu for today and exit (default)",
                       action="store_true")
    parser.add_argument("-c", "--clean", help="reduce the amount of printing to minimum",
                        action="store_true")
    parser.add_argument("-d", "--debug", help="print all error messages",
                        action="store_true")
    args = parser.parse_args()
    if not args.clean:
        print(LOGO)
    if args.week:
        pool, active_canteens = load_all(CANTEEN_LIST)
        print_for_week(pool, active_canteens)
    else:
        if TODAY > 4:
            print("Nothing to load, the canteens are closed for today")
        else:
            pool, active_canteens = load_all(CANTEEN_LIST)
            print_for_today(pool, active_canteens)
