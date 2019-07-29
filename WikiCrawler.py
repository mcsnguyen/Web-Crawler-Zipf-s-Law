from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.robotparser
import requests
import queue
import time
import csv
import re
import os


class WikiCrawler:
    def __init__(self, crawl_id, url, page_limit):
        self.crawl_id = crawl_id
        self.url = url
        self.page_limit = page_limit
        self.page_crawled = 0

        self.plain_text = ''
        self.soup_formatted_text = ''

        self.url_frontier = queue.Queue(maxsize=0)
        self.discovered_url_set = set()
        self.content_dictionary = {}

        self.outlink_report = {}
        self.num_of_outlinks = 0
        self.document_number = 0

        self.parsed_url = '{0.scheme}://{0.netloc}/'.format(urlparse(self.url))
        self.domain = '{0.netloc}/'. format(urlparse(self.url))
        robot_url = self.parsed_url + 'robots.txt'

        self.robots_rules = urllib.robotparser.RobotFileParser(robot_url)

    def crawl(self):
        while self.page_crawled < self.page_limit:
            self.get_links()
            self.get_contents()
            self.expand_frontier()

        self.store_output(self.content_dictionary, 'crawled_content.csv')

    def check_robots_txt(self, check_url):
        self.robots_rules.read()
        return self.robots_rules.can_fetch('*', check_url)

    def get_links(self):
        try:
            self.plain_text = requests.get(self.url, timeout=5).text
            self.soup_formatted_text = BeautifulSoup(self.plain_text, 'html.parser')

            for link in self.soup_formatted_text.findAll('a'):
                found_link = link.get('href')
                found_link = str(found_link)
                check_link = urlparse(found_link)
                ignore_these = "\(|\)|%|Wikipedia:|php|jpg|JPG|jpeg|JPEG|svg$"

                if re.search('^/', found_link) and not re.search(ignore_these, found_link):
                        remove_fwdslash = list(found_link)
                        remove_fwdslash[0] = ""
                        remove_fwdslash = ''.join(remove_fwdslash)
                        found_link = self.parsed_url + remove_fwdslash

                if found_link is not None and re.search(self.domain, found_link) and not re.search(ignore_these, found_link):
                    if self.check_robots_txt(found_link):
                        self.check_unique(found_link)
                    self.num_of_outlinks += 1

            self.outlink_report[self.url] = self.num_of_outlinks
            self.store_output(self.outlink_report, "report.csv")
        except requests.Timeout as e:
            print('Timeout:' + str(e))

    def check_unique(self, found_link):
        if found_link not in self.discovered_url_set:
            self.url_frontier.put(found_link)
            self.discovered_url_set.add(found_link)

    def get_html(self):
        html = self.soup_formatted_text
        filename = "doc" + str(self.document_number) + '.html'
        self.store_output(html, filename)

    def get_contents(self):
        crawled_content = ""
        # content_div = self.soup_formatted_text.find(attrs={'class': None})
        # text_div = content_div.find_all('p')
        text_div = self.soup_formatted_text.findAll('p')

        if text_div is not None:
            for paragraphs in text_div:
                crawled_content += paragraphs.text + ' '

            crawled_content = " ".join(crawled_content.split())
            formatted_content = re.sub(r",|\[\d+\]", "", crawled_content)

            self.content_dictionary[self.url] = formatted_content
            self.get_html()
            self.document_number += 1

    def store_output(self, content, filename):
        folder_path = './repository/crawl' + str(self.crawl_id) + '/'
        if not os.path.isdir(folder_path):
            try:
                os.makedirs(folder_path)
            except OSError:
                print('Directory creation for %s failed...' % folder_path)

        file_path = os.path.join(folder_path, filename)
        if re.search(r'.csv$', filename):
            self.csv_output(content, file_path)
        else:
            self.html_output(content, file_path)

    @staticmethod
    def csv_output(content, file_path):
        if not os.path.isfile(file_path):
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                output = csv.writer(csvfile, delimiter=',')
                for key, value in content.items():
                    output.writerow([key, value])
        else:
            with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
                output = csv.writer(csvfile, delimiter=',')
                for key, value in content.items():
                    output.writerow([key, value])

    @staticmethod
    def html_output(content, file_path):
        with open(file_path, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(str(content.prettify()))

    def expand_frontier(self):
        #time.sleep(10)

        self.clear_parameters()
        self.page_crawled += 1

        next_url = self.url_frontier.get()
        self.url = next_url

    def clear_parameters(self):
        self.num_of_outlinks = 0
        self.outlink_report = {}


if __name__ == "__main__":
    test = WikiCrawler(6, 'https://starcraft.fandom.com/wiki/Dominion_Special_Forces', 20)
    test.crawl()
