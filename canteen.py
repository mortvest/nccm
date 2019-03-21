from html.parser import HTMLParser
import re
import requests

class MenuItem:
    def __init__(self, item_type, item_name, date, canteen):
        self.item_type = item_type
        self.item_name = item_name
        self.date = date
        self.canteen = canteen

class MyHTMLParser(HTMLParser):
    lst = []
    def handle_data(self, data):
        """ Remove unused symbols """
        if data not in ["\n", "\xa0", "\r", "\r\n"]:
            self.lst.append(data.replace("\xa0", ""))
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
        """ Method for filling the list of menu items from a page """

class BioCanteen(Canteen):
    def __pop_item(self, lst, pool, date):
        item_type = lst.pop()
        item_name = lst.pop()
        pool.append(MenuItem(item_type, item_name, date, self.name))

    def fill_pool(self, pool):
        html_parser = MyHTMLParser()
        request = requests.get(self.url)
        page = "\n".join(re.findall("^.*tr height=.*$", request.text, re.MULTILINE))
        # with open('bio_fail.html', 'r') as myfile:
        #     page = "\n".join(re.findall("^.*tr height=.*$", myfile.read(), re.MULTILINE))
        html_parser.feed(page)
        # lst = html_parser.get_list()
        lst = html_parser.get_list()
        lst.reverse()
        while lst:
            # pop the first item
            fst = lst.pop()
            try:
                # is it a date?
                maybe_date = re.match(r"(Uge.*) (.*) - (.*)", fst, flags=0).group(3)
                date = maybe_date
            except:
                # if not a date - append the first item back to the list
                lst.append(fst)
                self.__pop_item(lst, pool, date)
        lst.reverse()
