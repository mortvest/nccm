from html.parser import HTMLParser
import datetime
import re
import requests

WEEKDAYS = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag"]
CANTEENS = ["August Krogh", "Biocenter"]
PAGE_URLS = ["http://www.biocenter.ku.dk/kantine/menuoversigt/",
             "http://www1.bio.ku.dk/akb/kantine/menuoversigt/"]
# TODO: Add terminal interface
TODAY = datetime.date.today().weekday()

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
    for canteen in CANTEENS:
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
    # r = requests.get(url)
    parser = MyHTMLParser()
    # page = "\n".join(re.findall("^.*tr height=.*$", r.text, re.MULTILINE))
    page = ""
    with open('test1.html', 'r') as myfile:
        page = myfile.read()
    parser.feed(page)
    var = parser.get_list()
    if len(var) < 25:
        print("ABORTED, " + canteen_name + " - menu inclomlete")
    elif TODAY > 4:
        print("ABORTED, " + canteen_name + " - the canteens are closed today!")
    else:
        for j in range(5):
            date = re.match(r"(.*) (.*) - (.*)", var.pop(0), flags=0).group(3)
            dish_type = re.match(r"(.*) (.*)", var.pop(0), flags=0).group(1)
            dish_name = var.pop(0)
            pool.append(Dish(dish_type, dish_name, date, canteen_name))
            dish_type = re.match(r"(.*) (.*):", var.pop(0), flags=0).group(1)
            dish_name = var.pop(0)
            pool.append(Dish(dish_type, dish_name, date, canteen_name))

pool = []
for nr in range(len(CANTEENS)):
    load_list_for_canteen(PAGE_URLS[nr], pool, CANTEENS[nr])
# print_for_today(pool)
print_for_week(pool)
