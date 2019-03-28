import datetime
import argparse
import config
from canteen import *

# TODO: Add logging (the proper way)
# TODO: Add support for choosing canteens and days
CANTEEN_LIST = [BioCanteen("Biocenter",    "http://www.biocenter.ku.dk/kantine/menuoversigt/"),
                BioCanteen("August Krogh", "http://www1.bio.ku.dk/akb/kantine/menuoversigt/"),
                HumCanteen("HUM", "https://hum.ku.dk/kontakt/gaest/kantinen/menuer/2019/hum/")]
LOGO = ("""\

███╗   ██╗ ██████╗ ██████╗███╗   ███╗
████╗  ██║██╔════╝██╔════╝████╗ ████║
██╔██╗ ██║██║     ██║     ██╔████╔██║
██║╚██╗██║██║     ██║     ██║╚██╔╝██║
██║ ╚████║╚██████╗╚██████╗██║ ╚═╝ ██║
╚═╝  ╚═══╝ ╚═════╝ ╚═════╝╚═╝     ╚═╝""")

def shorten(string, max_len):
    ellipsis = "..."
    comb_len = max_len - len(ellipsis)
    if len(string) <= max_len:
        return string
    else:
        return string[:comb_len] + ellipsis

def find_max_len(lst):
    return max([len(x.item_type) for x in lst])

def get_for_a_day(weekday, items):
    return [x for x in items if x.weekday == weekday]

def get_for_a_canteen(canteen, items):
    return [x for x in items if x.canteen == canteen]

def print_for_day(day, lst, canteen_list, max_len):
    items = get_for_a_day(lst, day)
    acc = []
    if items:
        acc.append(items[0].weekday)
        for canteen in canteen_list:
            try:
                cant_items = get_for_a_canteen(canteen.name, items)
                acc.append("  " + cant_items[0].canteen)
                for item in cant_items:
                    max_item_name = 80
                    item_name = shorten(item.item_name, max_item_name)
                    acc.append("    " +
                               item.item_type +
                               (max_len - len(item.item_type)) * " " +
                               ": " + item_name)
            except Exception as exception:
                if args.debug:
                    print(exception)
    return "\n".join(acc)

def print_for_week(items, canteen_list):
    acc = []
    if len(items) > 1:
        print("MENU FOR WEEK " + str(datetime.date.today().isocalendar()[1]))
        for day in config.WEEKDAYS:
            max_len = find_max_len(items)
            acc.append(print_for_day(items, day, canteen_list, max_len))
    return "\n".join(acc)

def print_for_today(items, canteen_list):
    if len(items) > 1:
        header = "MENU FOR TODAY: " + str(datetime.date.today())
        weekday = config.WEEKDAYS[config.TODAY]
        max_len = find_max_len(items)
        return header + "\n" + print_for_day(items, weekday, canteen_list, max_len)

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
                print (msg + ": done")
            pool += curr_lst
        except Exception as exception:
            if args.debug:
                print(exception)
            elif not args.clean:
                print(msg + ": failed")
    if not args.clean:
        print("")
    return (pool, active_canteens)


def print_for_today_web():
    pool_w, active_canteens_w = load_all(CANTEEN_LIST)
    return print_for_today(pool_w, active_canteens_w)


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
        print(print_for_week(pool, active_canteens))
    else:
        if config.TODAY > 4:
            print("Nothing to load, the canteens are closed for today")
        else:
            pool, active_canteens = load_all(CANTEEN_LIST)
            print(print_for_today(pool, active_canteens))
