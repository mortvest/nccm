from html.parser import HTMLParser
from datetime import date
import pyparsing
import re
# TODO: Add support of multiple canteens
ADRESS="./page.html"

# TODO: Add terminal interface

class MyHTMLParser(HTMLParser):
    lst = []
    def handle_data(self, data):
        if data not in ["\n",'\xa0']:
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

def get_for_a_day(date, dishes):
    return [x for x in dishes if (x.date == date)]

def get_for_a_canteen(date, dishes):
    return [x for x in dishes if (x.date == canteen)]

parser = MyHTMLParser()
page = ""
dishes = []
with open(ADRESS, 'r') as myfile:
    page=myfile.read()

parser.feed(page)
var = parser.get_list()
lst = []
for j in range(5):
    date = re.match(r"(.*) (.*) - (.*)", var.pop(0), flags=0).group(3)
    dish_type = re.match(r"(.*) (.*)", var.pop(0), flags=0).group(1)
    dish_name = var.pop(0)
    lst.append(Dish(dish_type, dish_name, date, "August Krogh"))
    dish_type = re.match(r"(.*) (.*):", var.pop(0), flags=0).group(1)
    dish_name = var.pop(0)
    lst.append(Dish(dish_type, dish_name, date, "August Krogh"))

for dish in lst:
    print(str(dish))
