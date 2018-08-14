from html.parser import HTMLParser
import requests
import re

class MenuItem:
    def __init__(self, item_type, item_name, date, canteen):
        self.item_type = item_type
        self.item_name = item_name
        self.date = date
        self.canteen = canteen
    def __str__ (self):
        # return ("*** " + (4 - len(self.item_type))*" " + self.item_type + " ret: " + self.item_name)
        return ("    " + self.item_type + (4 - len(self.item_type))*" " + " ret: " + self.item_name)

class MyHTMLParser(HTMLParser):
    lst = []
    def handle_data(self, data):
        if data not in ["\n",'\xa0',"\r","\r\n"]:
            self.lst.append(data.replace('\xa0', ''))
    def get_list(self):
        new_lst = self.lst.copy()
        # print(new_lst)
        MyHTMLParser.lst = []
        return new_lst

class Canteen():
    def __init__(self, name, url):
        self.name = name
        self.url = url
    # Abstract method for reutrning a list of items from a page
    def fill_pool(self, pool):
        pass

class BioCanteen(Canteen):
    def repair(self, foo):
        if foo == "Lun ret:" or re.search(r"Uge [1-9].*", foo):
            return ["", foo]
        else:
            return [foo]

    def fill_pool(self, pool):
        html_parser = MyHTMLParser()
        r = requests.get(self.url)
        page = "\n".join(re.findall("^.*tr height=.*$", r.text, re.MULTILINE))
        # with open('test_fail.html', 'r') as myfile:
        #     page = "\n".join(re.findall("^.*tr height=.*$", myfile.read(), re.MULTILINE))
        html_parser.feed(page)
        lst = html_parser.get_list()
        num_days = 5
        for j in range(num_days):
            date = re.match(r"(Uge.*) (.*) - (.*)", lst.pop(0), flags=0).group(3)
            lst.pop(0)
            lst = self.repair(lst.pop(0)) + lst
            item_name = lst.pop(0)
            pool.append(MenuItem("Varm", item_name, date, self.name))
            lst.pop(0)
            lst = self.repair(lst.pop(0)) + lst
            item_name = lst.pop(0)
            pool.append(MenuItem("Lun", item_name, date, self.name))
