#!/usr/bin/python

import sys
from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import quote_plus
from pprint import pprint

def parse_multiple_results(soup):
    rows = soup.find(id='pagecontent').find('table').find_all('tr')
    all_rows = []
    for row in rows:
        cells = row.find_all('td')
        row_data = {}
        for cell_num in xrange(len(cells)):
            cell_data = cells[cell_num]
            cell_text = cell_data.text
            cell_field = fields[cell_num]
            if cell_text.strip() != '':
                row_data[cell_field] = cell_text
            if cell_num == url_field_num:
                url = cell_data.find('a')['href']
                row_data[url_field] = url
                x500 = url.split(x500_split)[1]
                row_data[x500_field] = x500
        all_rows.append(row_data)
    all_rows.pop(0)
    return all_rows

def is_multiple_results(soup):
    try:
        table_present = soup.find(id='pagecontent').find('table')
        h2_present = soup.find(id='pagecontent').find('h2')
        return (table_present and not(h2_present)) == True  
    except AttributeError: # catch None.find()
        return False

def is_single_result(soup):
    try:
        result = soup.find(id='pagecontent').find('h2')
        return result != None
    except AttributeError: # catch None.find()
        return False

def is_no_results(soup):
    try:
        results = soup.find(id='pagecontent').find_all('b')
        for result in results:
            if result.text == 'No matches found.':
                return True
        return False
    except AttributeError: # catch None.find()
        return False

def is_too_many_results(soup):
    try:
        results = soup.find(id='pagecontent').find_all('b')
        for result in results:
            if result.text == 'Too many entries matched your search criteria. Please try again with more specific criteria. ':
                return True
        return False
    except AttributeError: # catch None.find()
        return False

search_url = 'http://www.umn.edu/lookup?SET_INSTITUTION=UMNTC&type=name&CN=%s&campus=t&role=any'
search_name = quote_plus(sys.argv[1])

fields = ['name', 'email', 'work_phone', 'phone', 'dept_or_college']
x500_field = 'x500'
x500_split = '&UID='
url_field = 'url'
url_field_num = 0

html = urlopen(search_url % search_name).read()
soup = BeautifulSoup(html)
if is_multiple_results(soup):
    results = parse_multiple_results(soup)
    pprint(results)
    print '%s results found.' % len(results)
elif is_single_result(soup):
    print 'Single result'
elif is_no_results(soup):
    print 'No results'
elif is_too_many_results(soup):
    print 'Too many results'
else:
    print 'Unknown state'
