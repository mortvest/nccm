from html.parser import HTMLParser
import requests
import re

ITEM_OFFSET = 11
NUM_DAYS = 5

class MenuItem:
    def __init__(self, item_type, item_name, date, canteen):
        self.item_type = item_type
        self.item_name = item_name
        self.date = date
        self.canteen = canteen
    def __str__ (self):
        return ("    " +
                self.item_type[:-1] +
                (ITEM_OFFSET - len(self.item_type)) * " " +
                ": " + self.item_name)

class MyHTMLParser(HTMLParser):
    lst = []
    def handle_data(self, data):
        if data not in ["\n",'\xa0',"\r","\r\n"]:
            self.lst.append(data.replace('\xa0', ''))
    def get_list(self):
        new_lst = self.lst.copy()
        MyHTMLParser.lst = []
        return new_lst

class Canteen():
    """ Abstract class. Implement an instance for each type of canteen menu """
    def __init__(self, name, url):
        self.name = name
        self.url = url
    def fill_pool(self, pool):
        """ Method for returning a list of menu items from a page """

class BioCanteen(Canteen):
    def __pop_item(self, lst, pool, date):
        item_type = lst.pop(0)
        item_name = lst.pop(0)
        pool.append(MenuItem(item_type, item_name, date, self.name))

    def fill_pool(self, pool):
        html_parser = MyHTMLParser()
        r = requests.get(self.url)
        page = "\n".join(re.findall("^.*tr height=.*$", r.text, re.MULTILINE))
        # with open('bio_fail.html', 'r') as myfile:
        #     page = "\n".join(re.findall("^.*tr height=.*$", myfile.read(), re.MULTILINE))
        html_parser.feed(page)
        lst = html_parser.get_list()
        for j in range(NUM_DAYS):
            date = re.match(r"(Uge.*) (.*) - (.*)", lst.pop(0), flags=0).group(3)
            # first menu item
            self.__pop_item(lst, pool, date)
            # second menu item
            self.__pop_item(lst, pool, date)
