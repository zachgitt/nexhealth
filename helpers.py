import requests
import datetime as dt
import pytz


def http_request_appointments():
    today = now_with_timezone()
    next_week = today + dt.timedelta(days=7)
    start = str(today.year) + '-' + str(today.month) + '-' + str(
        today.day) + 'T00:00:00.000Z'
    end = str(today.year) + '-' + str(today.month) + '-' + str(
        next_week.day) + 'T00:00:00.000Z'

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
        ('end', end),
        ('location_id', '75'),
        ('nex_only', 'false'),
        ('provider_ids[]',
         ['415815', '417237', '416056', '417240', '417241', '415814', '415827', '415858',
          '417239']),
        ('start', start),
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
    return int(timestamp.split('T')[1][:2])


def parse_time(timestamp):
    return timestamp.split('T')[1][:5]


def appointment_date(appointment):
    timestamp = appointment['start_time']
    date = timestamp.split('T')[0]
    year, month, day = date.split('-')
    appt = dt.datetime(int(year), int(month), int(day))
    return appt.date()


def within_week(appointment):
    appt = appointment_date(appointment)
    now = now_with_timezone().date()
    next_week = now + dt.timedelta(days=7)

    if now <= appt < next_week:
        return True
    return False


def appointment_index(appointment):
    appt = appointment_date(appointment)
    delta = appt - now_with_timezone().date()
    return delta.days


# method is a bit roundabout due to python timestamp nuances 
def time_plus_duration(time, duration):
    assert (5 <= duration <= 60)
    future = dt.datetime.combine(now_with_timezone(), time) + dt.timedelta(minutes=duration)
    return future.time()


# converts '09:30' to datetime
def str_to_time(str):
    hr, min = str.split(':')
    return dt.time(int(hr), int(min))


# find if time overlaps with an appointment
# this is linear solution, but can be done in O(logn) with binary search
def overlapping_appointment(time, appointments):
    for idx, appointment in enumerate(appointments):
        start = str_to_time(appointment[0])
        end = str_to_time(appointment[1])
        if start <= time < end:
            return idx

    # overlap not found
    return None


def get_working_hours(name, weekdays, selection):

    # save working hours, initialy (0,0)
    working_hours = {weekday: (0, 0) for weekday in weekdays}
    response = http_request_providers()
    for provider in response['data']:

        for working_hour in provider['working_hours']:

            # provider name
            if selection == 'providers':
                found_name = provider['name']
            # operatory name
            else:
                found_name = working_hour['operatory']['name']

            # save hours if it matches with the name we're searching
            if found_name == name:
                working_hours[working_hour['day']] = (
                    parse_hour(working_hour['begin_time']),
                    parse_hour(working_hour['end_time'])
                )

    return working_hours


# returns the appointments per day, in chronological order, for the next week
def get_week_appointments(name, selection):

    week_appointments = [[] for i in range(7)]
    response = http_request_appointments()

    for appointment in response['data']:

        # provider vs. operatory name
        if selection == 'providers':
            found_name = appointment['provider_name']
        else:
            found_name = appointment['operatory_name']

        # name is correct and appointment is upcoming
        if found_name == name and within_week(appointment):
            index = appointment_index(appointment)
            week_appointments[index].append((
                parse_time(appointment['start_time']),
                parse_time(appointment['end_time'])
            ))

    return week_appointments


def get_availability(name, weekdays, length, selection):

    # get working hours and appointments
    working_hours = get_working_hours(name, weekdays, selection)
    week_appointments = get_week_appointments(name, selection)

    # save next 7 days availability at defined interval lengths
    week_availability = []
    for i, weekday in enumerate(weekdays):

        # within working hours
        day_availability = []
        day_appointments = week_appointments[i]
        time = dt.time(working_hours[weekday][0], 0)
        end = dt.time(working_hours[weekday][1], 0)
        while time < end:

            # check time doesn't overlap with appointments
            overlapping_idx = overlapping_appointment(time, day_appointments)
            if overlapping_idx is not None:
                time = str_to_time(day_appointments[overlapping_idx][1])

            # otherwise update time by adding length
            else:
                day_availability.append(str(time.hour) + ':' + str(time.minute).zfill(2))
                time = time_plus_duration(time, length)

        week_availability.append(day_availability)

    return week_availability


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


def parse_weekdays(dates):
    weekdays = [date.split(' ')[0] for date in dates]
    return weekdays


def next_seven_dates():
    dates = []
    for i in range(7):
        date = now_with_timezone() + dt.timedelta(days=i)
        day = date.day
        month = month_int_to_string(date.month)
        weekday = weekday_int_to_string(date.weekday())
        dates.append(weekday + ' ' + month + ' ' + str(day))

    return dates


def now_with_timezone():
    # assume timezone should be NYC
    tz = pytz.timezone('America/New_York')
    return dt.datetime.now(tz)
