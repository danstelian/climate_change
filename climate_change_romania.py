"""
Working with public data sets - csv files

Analyse 16 years worth of climate related data from 23 weather stations in Romania
(from 2000 to 2016)

Use download_doc.py to get the annual climate reports from data.gov.ro

Three functions:
1. Lowest temperature by year and place - measure()
2. Coldest day in 2016 - coldest_day()
3. All the measurements (23) for a given date - measure_by_date()
"""
from collections import defaultdict, Counter
import csv
import os
from datetime import datetime

from operator import itemgetter
from itertools import groupby


# Station id and station name
stations = {
    '15015': 'Ocna Sugatag',
    '15020': 'Botosani',
    '15090': 'Iasi',
    '15108': 'Ceahlau Toaca',
    '15120': 'Cluj-Napoca',
    '15150': 'Bacau',
    '15170': 'Miercurea Ciuc',
    '15200': 'Arad',
    '15230': 'Deva',
    '15260': 'Sibiu',
    '15280': 'Varfu Omu',
    '15292': 'Caransebes',
    '15310': 'Galati',
    '15335': 'Tulcea',
    '15346': 'Ramnicu Valcea',
    '15350': 'Buzau',
    '15360': 'Sulina',
    '15410': 'Drobeta Turnu Severin',
    '15420': 'Bucuresti-Baneasa',
    '15450': 'Craiova',
    '15460': 'Calarasi',
    '15470': 'Rosiorii de Vede',
    '15480': 'Constanta'
}


def get_reports():
    # Make a list of names for all the annual climate report files stored in 'doc' directory
    reports = []

    file_names = os.listdir(os.path.join(os.path.dirname(__file__), 'doc'))

    for file in file_names:
        if 'clim' in file:
            reports.append(file)

    return reports


def measure():
    # Go through all the climate reports and make a list of all the entries
    reports = get_reports()

    measurements = []
    for report in reports:
        measurements += list(csv.DictReader(open('doc/'+report)))

    # Identify the lowest temperature for each year, and also the coldest place
    coldest = defaultdict(Counter)  # not the best use of Counter objects
    for row in measurements:
        year = row['DATCLIM'].split('/')[0]
        place = stations[row['CODST']]

        try:
            temp = float(row['TMIN'])
        except ValueError:
            continue  # ignore all the wrong temperature entries

        # Thanks to Counter, the try - except block below is unnecessary
        if coldest[year][place] > temp:
            coldest[year][place] = temp

        # This would be mandatory for a dictionary type object
        # try:
        #     if coldest[year][place] > temp:
        #         coldest[year][place] = temp
        # except Exception:
        #     coldest[year][place] = temp

    print('Lowest temperature by year and place:')
    for key, value in coldest.items():
        year = key
        place, minim = min(value.items(), key=lambda t: t[1])
        print(f'{year}', end='\t')
        print(f'{minim}\t{place}')


def coldest_day(year):
    # Compute the average temperature for each day (based on all 23 measurements)
    # Compare the results and display the five coldest days of the year
    file_name = 'doc/climrbsn'+str(year)+'.csv'
    if not os.path.isfile(file_name):
        return

    measurements = list(csv.DictReader(open(file_name)))

    by_date = defaultdict(list)

    for day in measurements:
        try:
            temp = float(day['TMED'].strip())  # try converting to float
        except Exception:
            temp = day['TMED'].insert('0', day['TMED'].index('.'))  # some temperatures look like this: -.7 or .4
            temp = float(temp.strip())  # convert into this: -0.7 and 0.4 (and then float)

        by_date[day['DATCLIM']].append(temp)

    print(f'Coldest days in {year}:')

    index = 0
    for k in sorted(by_date, key=lambda t: sum(by_date[t]) / len(by_date[t])):
        index += 1
        if index is 6:
            break

        date = datetime.strptime(k.split()[0], '%Y/%m/%d')  # make datetime object from string
        dat = datetime.date(date).strftime('%d %B')  # format date

        avrg = round(sum(by_date[k]) / len(by_date[k]), 1)
        print(f"{dat} {avrg}")


def convert_temp(temp_str):
    # Convert temperature from string to float
    try:
        temp = float(temp_str.strip())  # try converting to float
    except Exception:
        temp = temp_str.insert('0', temp_str.index('.'))  # some temperatures look like this: -.7 or .4
        temp = float(temp.strip())  # convert into this: -0.7 and 0.4 (and then float)
    return temp


def measure_by_date(date):
    # Extract year from date
    year = date.split('/')[0]

    # Open climate report from specified year
    file_name = 'doc/climrbsn' + str(year) + '.csv'
    if not os.path.isfile(file_name):
        return

    # Make a list of measurements
    measurements = list(csv.DictReader(open(file_name)))

    # Sort the measurements by date (they are sorted by weather station and then by year)
    measurements.sort(key=itemgetter('DATCLIM'))

    # Iterate in groups
    for field, items in groupby(measurements, key=itemgetter('DATCLIM')):
        if field == date:
            print(field)
            for i in sorted(items, key=lambda t: convert_temp(t['TMED'])):
                temp = convert_temp(i['TMED'])
                station = stations[i['CODST']]
                print(f'\t{station}, {temp}')


if __name__ == '__main__':
    measure()
    print('-'*30)
    coldest_day(2016)
    print('-' * 30)
    measure_by_date('2014/03/18')
