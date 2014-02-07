#!/usr/bin/python

import argparse
import sys
from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import quote_plus
from pprint import pprint
from HTMLParser import HTMLParser

class SearchUMN(object):

    class MLStripper(HTMLParser):
        def __init__(self):
            self.reset()
            self.fed = []
        def handle_data(self, d):
            self.fed.append(d)
        def get_data(self):
            return ''.join(self.fed)

    def strip_tags(self, html):
        s = self.MLStripper()
        s.feed(html)
        return s.get_data()

    def replace_br_with_newline(self, html):
        return html.replace('<br>', '\n').replace('</br>', '\n')

    def parse_multiple_results(self, soup):
        rows = soup.find(id='pagecontent').find('table').find_all('tr')
        all_rows = []
        for row in rows:
            cells = row.find_all('td')
            row_data = {}
            for cell_num in xrange(len(cells)):
                cell_data = cells[cell_num]
                cell_text = cell_data.text
                cell_field = self.fields[cell_num]
                if cell_text.strip() != '':
                    row_data[cell_field] = cell_text.replace(u'\xa0', u' ')
                if cell_num == self.url_field_num:
                    url = cell_data.find('a')['href']
                    row_data[self.url_field] = url
                    x500 = url.split(self.x500_split)[1]
                    row_data[self.x500_field] = x500
            all_rows.append(row_data)
        all_rows.pop(0)
        return all_rows

    def parse_single_result(self, soup):
        data = soup.find(id='pagecontent').find('table').find_all('tr')
        parsed = {}
        for kv_pair in data:
            key = kv_pair.find('th').text.strip().lower().replace(' ', '_')
            value_html = str(kv_pair.find('td'))
            value = self.strip_tags(self.replace_br_with_newline(value_html)).strip()
            parsed[key] = value
        return parsed

    def is_multiple_results(self, soup):
        try:
            table_present = soup.find(id='pagecontent').find('table')
            h2_present = soup.find(id='pagecontent').find('h2')
            return (table_present and not(h2_present)) == True
        except AttributeError: # catch None.find()
            return False

    def is_single_result(self, soup):
        try:
            result = soup.find(id='pagecontent').find('h2')
            return result != None
        except AttributeError: # catch None.find()
            return False

    def is_no_results(self, soup):
        try:
            results = soup.find(id='pagecontent').find_all('b')
            for result in results:
                if result.text == 'No matches found.':
                    return True
            return False
        except AttributeError: # catch None.find()
            return False

    def is_too_many_results(self, soup):
        try:
            results = soup.find(id='pagecontent').find_all('b')
            for result in results:
                if result.text == 'Too many entries matched your search criteria. Please try again with more specific criteria. ':
                    return True
            return False
        except AttributeError: # catch None.find()
            return False

    search_url = 'http://www.umn.edu/lookup?SET_INSTITUTION=UMNTC&type=%s&CN=%s&campus=%s&role=%s'
    fields = ['name', 'email', 'work_phone', 'phone', 'dept_or_college']
    x500_field = 'x500'
    x500_split = '&UID='
    url_field = 'url'
    url_field_num = 0

    def load_results(self):
        html = urlopen(self.search_url % (search_type, search_query, campus, role)).read()
        soup = BeautifulSoup(html)
        if self.is_multiple_results(soup):
            return self.parse_multiple_results(soup)
        elif self.is_single_result(soup):
            return self.parse_single_result(soup)
        elif self.is_no_results(soup):
            return None
        elif self.is_too_many_results(soup):
            return None
        else:
            return None

    def __init__(self, search_type='name', campus='t', role='any', query=None):
        self.search_type = search_type
        self.campus = campus
        self.role = role


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search the UMN People Directory using a Python API.')
    parser.add_argument('-t', '--search_type', default='name',
                        help='Search by name or id (Default: name)',
                        choices=['name','id'])
    parser.add_argument('-c', '--campus', default='t',
                        help='Campus to search (Default: Twin Cities campus)',
                        choices=['a','c','d','m','r','t','o'])
    parser.add_argument('-r', '--role', default='any',
                        help='The person\'s role (Default: any)',
                        choices=['any','sta','stu','alu','ret'])
    parser.add_argument('query',
                        help='Name or Internet ID of person to be searched')
    args = parser.parse_args()

    if (args.search_type == 'id'):
        search_type = 'Internet+ID'
    else:
        search_type = args.search_type
    campus = args.campus
    role = args.role
    search_query = quote_plus(args.query)

    searcher = SearchUMN(search_type, campus, role, search_query)
    results = searcher.load_results()

    pprint(results)
