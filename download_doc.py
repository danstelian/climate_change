"""
Get all the download links, store them in a csv file
Download all the annual climate reports from data.gov.ro
from 2016 to 1961
"""
from collections import OrderedDict
from bs4 import BeautifulSoup
import requests
import csv
import os


def get_file_list():
    """
    Web Scraping
    Parse and collect links to annual climate reports (csv files)
    Returns list of links as list of OrderedDict type objects (year, name of file, download link)
    """
    files = []

    url = 'http://data.gov.ro/dataset/date-climatologice-de-la-cele-23-de-statii-esentiale-pentru-anul-2016'

    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')

    links = soup.find('section', id='dataset-resources', class_='resources')

    for link in links.find_all('a', class_='resource-url-analytics'):
        to_get = link['href']
        name = to_get.split('/')[-1]
        year = name.split('.')[0][-4:]

        d = OrderedDict()

        d['file_year'] = year
        d['file_name'] = name
        d['file_link'] = to_get

        files.append(d)

    # First and last link point to the same file
    if files[0]['file_year'] == files[-1]['file_year']:
        files.pop()

    return files


def make_list(files):
    """
    Make csv file from list
    Fieldnames: file_year, file_name and file_link
    """
    with open('doc/file_list.csv', 'w', newline='') as f:
        fieldnames = ['file_year', 'file_name', 'file_link']

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for file in files:
            writer.writerow(file)


def download_files(files, start, stop=None):
    """
    Download desired annual climate reports if missing
    """
    try:
        stop = int(stop) + 1
    except Exception:
        stop = int(start) + 1
    finally:
        start = int(start)

    for i in range(start, stop):

        for item in files:
            if int(item['file_year']) == i:

                if os.path.isfile('doc/'+item['file_name']):
                    continue
                source = requests.get(item['file_link'])
                with open('doc/'+item['file_name'], 'wb') as f:
                    f.write(source.content)


def main():
    # 'doc/file_list.csv' stores all the download links to the annual climate reports
    if not os.path.isfile('doc/file_list.csv'):
        files = get_file_list()
        make_list(files)
    else:
        files = list(csv.DictReader(open('doc/file_list.csv')))

    # Download al the reports from 2000 to 2016
    download_files(files, '2000', '2016')


if __name__ == '__main__':
    main()