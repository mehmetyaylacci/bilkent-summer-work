# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
import csv
from bs4 import BeautifulSoup as bs
from urllib import request
import time
import logging

"""
Author: Mehmet Yaylacı
Year: 2019
Contributors: 
- Alp Sayin (alpsayin.com)
"""

"""
    *As recommended this project will only create two csv files on .txt format
    *Other libraries could also be used, but I've chosen to use scrapy on this project,
please don't recommend me to use other libs (like urllib.requests, selenium or others).
Scrapy is the coolest way to scrape these kinds of data :)
    *I didn't want to create a scrapy project so we will use
a primitive way of using spiders.
    *Try not to crush Bilkent's servers. Adding waiting time for our spiders will
hopefully solve this issue.
    *The information is fetched from: http://mfstaj.cs.bilkent.edu.tr
"""

########

# some global variables to create two csv files on .txt format
first_outfile = "data/first.csv"
second_outfile = "data/second.csv"
second_infile = first_outfile

"""
    First of the spiders. Just goes through the first sets of pages and extracts links 
with some other information.
"""

class first_spider(scrapy.Spider):
    name = 'first_spider'

    def start_requests(self):
        # setting custom settings, this will hopefully solve a possible ddos.
        custom_settings = {
            'DOWNLOAD_DELAY': 0.1,
            'ITEM_PIPELINES': {
                'freedom.pipelines.IndexPipeline': 300
            }
        }

        global first_outfile

        csvfile = open(first_outfile, 'w', newline='', encoding="utf-8") # could be 'a' if append
        self.writer = csv.writer(csvfile)

        # these are the headers of csv
        self.writer.writerow(["company", "id", "city", "dep", "sec"])

        allowed_domains = ['mfstaj.cs.bilkent.edu.tr']
        # url = "http://mfstaj.cs.bilkent.edu.tr/visitor/?filter=AllCompanies&page=company"

        with request.urlopen('http://mfstaj.cs.bilkent.edu.tr/visitor/?page=company&start=0') as response:
            html = response.read()
            page = bs(html)
            # page.prettify()
            company_table = page.find('table', {'id':'companies'})
            first_col = company_table.find('td', {'style':'font-size:0.9em;'})
            page_indicator = first_col.find("span", {"style": "font-size:1.2em;"}).getText()
            last_page_num = int(page_indicator.split('/')[1].replace(' ',''))
            logging.debug('last_page_num={}'.format(last_page_num))
            input('haha')

        for page_num in range(last_page_num):
            url = "http://mfstaj.cs.bilkent.edu.tr/visitor/?page=company&start={}&filter=AllCompanies".format(page_num)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = bs(response.text, 'html.parser')
        soup.prettify()

        stuff = []

        size = len(soup.find_all("td", class_="companyName"))

        former_id = 0  # this checks duplicates. thanks bilkent for the mistakes :(

        for x in range(size):
                company = soup.find_all("td", class_="companyName")[x]
                companyTop = soup.find_all("tr", class_="company")[x]
                listOfAtt = companyTop.find_all("td")

                newID = company.find("a")["href"][-4:].strip()

                # getting rid of duplicates will help us on the next spider.
                if newID != former_id:
                        self.writer.writerow([company.get_text().strip(), newID,
                                                    listOfAtt[1].get_text().strip(), listOfAtt[2].get_text().strip(),
                                                        listOfAtt[3].get_text().strip()])

                        former_id = company.find("a")["href"][-4:].strip()

########

"""
    Second spider. This time we will click on the links and get the company 
pages one by one. Pls don't ddos Bilkent. Bilkent's internet seems it can crush
anytime so pls don't pressure the servers :(
"""

class second_spider(scrapy.Spider):
    name = 'second_spider'

    def start_requests(self):
        # setting custom settings, this will hopefully solve a possible ddos.
        custom_settings = {
            'DOWNLOAD_DELAY': 0.1,
            'ITEM_PIPELINES': {
                'freedom.pipelines.IndexPipeline': 300
            }
        }

        global second_infile, second_outfile

        csvfile = open(second_infile, 'r', newline='', encoding="utf-8")
        reader = csv.DictReader(csvfile)
        id = []
        allowed_domains = ['mfstaj.cs.bilkent.edu.tr']

        csvfile = open(second_outfile, 'w', newline='', encoding="utf-8")
        self.writer = csv.writer(csvfile)
        self.writer.writerow(["address", "info", "sector", "name", "country", "city", "phone",
                                "fax", "site"])

        for line in reader:
            id.append(line["id"])

        for x in id:
            url = "http://mfstaj.cs.bilkent.edu.tr/visitor/?page=company&content=detail&CompanyID=" + str(x)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = bs(response.text, 'html.parser')
        stuff = []
        for x in soup.find_all("textarea", class_="inputText"):
            stuff.append(x.getText().strip())

        for x in soup.find_all("input", class_="inputText"):
            stuff.append(x["value"].strip())

        self.writer.writerow(stuff)

########

"""
    Scrapy doesn't let me run two processes subsequently,
so call them one at a time.
"""

def first_process():
    process = CrawlerProcess()
    process.crawl(first_spider)
    process.start()


def second_process():
    process2 = CrawlerProcess()
    process2.crawl(second_spider)
    process2.start()


def setup_logger():
    FORMAT = '%(asctime)-15s %(name)s - %(levelname)s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    logging.debug('DEBUG messages are printed')
    logging.info('INFO messages are printed')
    logging.warning('WARNING messages are printed')
    logging.error('ERROR messages are printed')
    logging.critical('CRITICAL messages are printed')


def main():
    setup_logger()

    logging.info('starting first_process')
    first_process()
    logging.info('first_process finished')
    # time.sleep(1)
    # logging.info('starting second_process')
    # second_process()
    # logging.info('second_process finished')


if __name__ == '__main__':
    main()
