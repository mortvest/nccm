from html.parser import HTMLParser
import datetime
import re
import requests

# TODO: Add support of multiple canteens
ADRESS="./page.html"
WEEKDAYS = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag"]
CANTEENS = ["August Krogh"]
PAGE_URLS = ["http://www1.bio.ku.dk/akb/kantine/menuoversigt/"]
# PAGE_URLS = ["http://www.biocenter.ku.dk/kantine/menuoversigt/"]
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
    print(dishes[0].date)
    for canteen in CANTEENS:
        foo = get_for_a_canteen(canteen, dishes)
        print(foo[0].canteen)
        for dish in foo:
            print(str(dish))

def print_for_week(dishes):
    print("Week menu:")
    for day in WEEKDAYS:
        print_for_day(dishes, day)

def print_for_today(dishes):
    print("Menu for today:")
    weekday = WEEKDAYS[datetime.date.today().weekday()]
    print_for_day(dishes,weekday)

r = requests.get(PAGE_URLS[0])
parser = MyHTMLParser()
page = r.text
# print(page)
# page = ""
# dishes = []
# with open(ADRESS, 'r') as myfile:
#     page=myfile.read()
page=re.findall("^.*tr height=.*$",page,re.MULTILINE)
page = "\n".join(page)
parser.feed(page)
var = parser.get_list()

if len(var) < 25:
    print("ABORTED, menu inclomlete")
elif TODAY > 4:
    print("ABORTED, the canteens are closed today!")
else:
    lst = []
    for j in range(5):
        date = re.match(r"(.*) (.*) - (.*)", var.pop(0), flags=0).group(3)
        dish_type = re.match(r"(.*) (.*)", var.pop(0), flags=0).group(1)
        dish_name = var.pop(0)
        lst.append(Dish(dish_type, dish_name, date, "August Krogh"))
        dish_type = re.match(r"(.*) (.*):", var.pop(0), flags=0).group(1)
        dish_name = var.pop(0)
        lst.append(Dish(dish_type, dish_name, date, "August Krogh"))
    # print_for_week(lst)
    print_for_today(lst)
