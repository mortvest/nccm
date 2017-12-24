from html.parser import HTMLParser
import datetime
import re
import requests
import argparse

WEEKDAYS = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag"]
CANTEEN_NAMES = ["Biocenter", "August Krogh"]
PAGE_URLS = ["http://www.biocenter.ku.dk/kantine/menuoversigt/",
             "http://www1.bio.ku.dk/akb/kantine/menuoversigt/"]
# TODAY = datetime.date.today().weekday() - 3
TODAY = datetime.date.today().weekday()
# TODO Add support for printing tables
# TODO Add error handlers

class MyHTMLParser(HTMLParser):
    lst = []
    def handle_data(self, data):
        if data not in ["\n",'\xa0',"\r","\r\n"]:
            self.lst.append(data.replace('\xa0', ''))
    def get_list(self):
        return self.lst

class Dish:
    def __init__(self, dish_type, dish_name, date, canteen):
        self.dish_type = dish_type
        self.dish_name = dish_name
        self.date = date
        self.canteen = canteen
    def __str__ (self):
        return ((4 - len(self.dish_type))*" " + self.dish_type + " ret: " + self.dish_name)
        # return (self.dish_name)

def get_for_a_day(date, dishes):
    return [x for x in dishes if (x.date == date)]

def get_for_a_canteen(canteen, dishes):
    return [x for x in dishes if (x.canteen == canteen)]

def print_for_day(day,lst):
    dishes = get_for_a_day(lst,day)
    print("* " + dishes[0].date)
    for canteen in CANTEEN_NAMES:
        foo = get_for_a_canteen(canteen, dishes)
        print("** " + foo[0].canteen)
        for dish in foo:
            print(str(dish))

def print_for_week(dishes):
    print("Week menu:")
    for day in WEEKDAYS:
        print_for_day(dishes, day)

def print_for_today(dishes):
    print("Menu for today:")
    weekday = WEEKDAYS[TODAY]
    print_for_day(dishes,weekday)

def load_list_for_canteen(url, pool, canteen_name):
    parser = MyHTMLParser()
    r = requests.get(url)
    page = "\n".join(re.findall("^.*tr height=.*$", r.text, re.MULTILINE))
    # page = ""
    # with open('test1.html', 'r') as myfile:
    #     page = myfile.read()
    parser.feed(page)
    var = parser.get_list()
    if len(var) < 25:
        print("ABORTED, " + canteen_name + " - menu inclomlete")
    else:
        for j in range(5):
            date = re.match(r"(.*) (.*) - (.*)", var.pop(0), flags=0).group(3)
            dish_type = re.match(r"(.*) (.*)", var.pop(0), flags=0).group(1)
            dish_name = var.pop(0)
            pool.append(Dish(dish_type, dish_name, date, canteen_name))
            dish_type = re.match(r"(.*) (.*):", var.pop(0), flags=0).group(1)
            dish_name = var.pop(0)
            pool.append(Dish(dish_type, dish_name, date, canteen_name))

def load_all():
    pool = []
    for nr in range(len(CANTEEN_NAMES)):
        load_list_for_canteen(PAGE_URLS[nr], pool, CANTEEN_NAMES[nr])
    return pool

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-w", "--week", help="show menu for week and exit",
                    action="store_true")
group.add_argument("-t", "--today", help="show menu for today and exit (default)",
                   action="store_true")

args = parser.parse_args()
if args.week:
    print_for_week(load_all())
else:
    print_for_today(load_all())
# TODO add support for choosing canteens and days
