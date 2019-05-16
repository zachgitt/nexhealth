import requests

def http_request_appointments():
	headers = {
		'Accept': 'application/vnd.Nexhealth+json; version=1',
		'Referer': 'https://www.nexhealth.com/app/calendar',
		'Origin': 'https://www.nexhealth.com',
		'If-None-Match': 's',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
		'Authorization': '4lBgtK8dXq7m63Mg-on3tQ'
	}
	params = (
		('cancelled', 'false'),
		('end', '2019-05-19T00:00:00.000Z'),
		('location_id', '75'),
		('nex_only', 'false'),
		('provider_ids[]', ['415815', '417237', '416056', '417240', '417241', '415814', '415827', '415858', '417239']),
		('start', '2019-05-12T00:00:00.000Z'),
		('subdomain', 'test'),
	)
	response = requests.get('https://nexhealth.info/appointments', headers=headers, params=params)
	return response.json()

def http_request_providers():
	headers = {
		'Accept': 'application/vnd.Nexhealth+json; version=1',
		'Referer': 'https://www.nexhealth.com/app/online_booking/customization',
		'Origin': 'https://www.nexhealth.com',
		'If-None-Match': 's',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
		'Authorization': '4lBgtK8dXq7m63Mg-on3tQ',
	}
	params = (
		('location_id', '75'),
		('page', '1'),
		('per_page', '10'),
		('subdomain', 'test'),
	)
	response = requests.get('https://nexhealth.info/providers', headers=headers, params=params)
	return response.json()

def get_unique_provider_names():
	response = http_request_providers() 
	unique_names = set()
	for provider in response['data']:
		name = provider['first_name'] + ' ' + provider['last_name']
		unique_names.add(name)

	return sorted(unique_names)

def get_unique_operatory_names():
	response = http_request_providers()
	unique_names = set()
	for provider in response['data']:
		for working_hour in provider['working_hours']:
			name = working_hour['operatory']['name']
			unique_names.add(name)

	return sorted(unique_names) 

def get_provider_id(name):
	return 1

def get_operatory_id(name):
	return 2

def get_provider_availability(id):
	return [10,20,30]

def get_operatory_availability(id):
	return [15,25,35,45]

def next_seven_days():
	return [1,2,3,4,5,6,7]
