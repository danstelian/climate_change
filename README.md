# Readme for climate_change
- climate_change/climate_change_romania.py

## Module doc
	Working with public data sets - csv files

	Analyse 16 years worth of climate related data from 23 weather stations in Romania
	(from 2000 to 2016)

	Use download_doc.py to get the annual climate reports from data.gov.ro

	Three functions:
	1. Lowest temperature by year and place - measure()
	2. Coldest day in 2016 - coldest_day()
	3. All the measurements (23) for a given date - measure_by_date()

## Install virtualenv
	sudo apt-get install virtualenv

## Set up dev environment
	virtualenv -p python3.6 venv
- create new isolated environment with python3 as the interpreter

## Activate it
	source venv/bin/activate

## Install third party libraries
	pip install -r requirements.txt
- requests, beautifulsoup4 and lxml modules

## Run script
	python climate_change.py

## Deactivate virtual env
	deactivate
