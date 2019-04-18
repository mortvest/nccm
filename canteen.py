import re
import datetime
import shutil
import os
from html.parser import HTMLParser
import requests
import PyPDF2
import config


class MenuItem:
    def __init__(self, item_type, item_name, weekday, canteen):
        self.item_type = item_type
        self.item_name = item_name
        self.weekday = weekday
        self.canteen = canteen


# TODO: REWRITE THIS
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
    def __pop_item(self, lst, pool, weekday):
        item_type = lst.pop()
        item_name = lst.pop()
        pool.append(MenuItem(item_type[:-1], item_name, weekday, self.name))

    def fill_pool(self, pool):
        html_parser = MyHTMLParser()
        request = requests.get(self.url)
        page = "\n".join(re.findall("^.*tr height=.*$", request.text, re.MULTILINE))
        # with open('bio_fail.html', 'r') as myfile:
        #     page = "\n".join(re.findall("^.*tr height=.*$", myfile.read(), re.MULTILINE))
        html_parser.feed(page)
        lst = html_parser.get_list()
        lst.reverse()
        while lst:
            # pop the first item
            fst = lst.pop()
            try:
                # is it a date?
                maybe_weekday = re.match(r"(Uge.*) (.*) - (.*)", fst, flags=0).group(3)
                weekday = maybe_weekday
            except:
                # if not a date - append the first item back to the list
                lst.append(fst)
                self.__pop_item(lst, pool, weekday)
        lst.reverse()


class HumCanteen(Canteen):
    def __download_pdf(self, pdf_name):
        url = self.url + pdf_name
        base_dir = "/tmp/"
        local_filename = base_dir + pdf_name
        request = requests.get(url, stream=True)
        content = ""
        with open(local_filename, 'wb') as curr_file:
            shutil.copyfileobj(request.raw, curr_file)
            read_pdf = PyPDF2.PdfFileReader(local_filename)
            page = read_pdf.getPage(0)
            content = page.extractText()
        # os.remove(local_filename)
        return content

    @staticmethod
    def __gen_regex(weekdays):
        lst = ["{} (.*) ".format(i) for i in weekdays]
        return ".* " + "".join(lst)

    def fill_pool(self, pool):
        week_nr = datetime.date.today().isocalendar()[1]
        pdf_name = "HUM_Uge_{}.pdf".format(week_nr)
        content = self.__download_pdf(pdf_name)
        print(content)
        replaced = re.sub("[\n\xa0\r]", "", content)
        item_names = list(re.match(self.__gen_regex(config.WEEKDAYS), replaced, flags=0).groups())
        for (weekday, item) in zip(config.WEEKDAYS, item_names):
            pool.append(MenuItem("Hovedret", item, weekday, self.name))

