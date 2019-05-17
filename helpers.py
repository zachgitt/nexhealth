import requests
from datetime import datetime, timedelta


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
        ('provider_ids[]',
         ['415815', '417237', '416056', '417240', '417241', '415814', '415827', '415858',
          '417239']),
        ('start', '2019-05-12T00:00:00.000Z'),
        ('subdomain', 'test'),
    )
    response = requests.get('https://nexhealth.info/appointments', headers=headers,
                            params=params)
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
    response = requests.get('https://nexhealth.info/providers', headers=headers,
                            params=params)
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

def parse_hour(timestamp):
	return timestamp:split('T')[1][:2]	

def get_provider_availability(name, weekday_month_days):

	# save next 7 weekdays
	weekdays = []
	for weekday_month_day in weekday_month_days:
		weekdays.append(weekday_month_day.split(' ')[0]
	
	# initialize availability to (0,0)
	weekdays_availability = {}
	for weekday in weekdays:
		weekdays_availability[weekday] = (0,0)

	# update availability to working hours
    response = http_request_providers()
	for provider in response['data']:
		# only save this providers working hours
		if provider == id:
			for working_hour in provider['working_hours']:
				weekdays_availability[working_hour['day']] = (parse_hour(working_hour['begin_time']), parse_hour(working_hour['end_time']))

	# subtract appointments from availability
	response = http_request_appointments()
	for appointment in response['data']:
		if appointment['provider_name'] == name:
			pass		

    return [10, 20, 30]


def get_operatory_availability(name, weekday_month_days):
    return [15, 25, 35, 45]


# NOTE: python enum 0=Monday
def weekday_int_to_string(integer):
    day = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    return day.get(integer)


def month_int_to_string(integer):
    month = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    return month.get(integer)


def next_seven_days():
    days = []
    for i in range(7):
        date = datetime.today() + timedelta(days=i)
        day = date.day
        month = month_int_to_string(date.month)
        weekday = weekday_int_to_string(date.weekday())
        days.append(weekday + ' ' + month + ' ' + str(day))

    return days
