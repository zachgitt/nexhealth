from flask import Flask, render_template, request, abort
from helpers import get_unique_provider_names, get_unique_operatory_names, get_provider_id, get_operatory_id, get_provider_availability, get_operatory_availability, next_seven_days

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip) 

@app.route('/')
@app.route('/select')
def select():
	return render_template('select.html')

@app.route('/list', methods=['POST'])
def list():

	# parse input
	selection = request.form.get('selection')
	length = int(request.form.get('length'))

	# validate inputs
	if selection not in ['providers', 'operatories']:
		abort(400, 'Please select providers or operatories to search!')
	if (length % 5 != 0) or (length < 5) or (60 < length):
		abort(400, 'Uh oh, the schedule length must be between 5 and 60 and a 5 minute interval.')

	# display list of names
	names = []
	if selection == 'providers':
		names = get_unique_provider_names()
	else:
		names = get_unique_operatory_names()

	return render_template('list.html', selection=selection.capitalize(), names=names, length=length)

@app.route('/availability')
def availability():
	
	# parse input
	selection = request.args.get('selection').lower()
	name = request.args.get('name')
	length = request.args.get('length')

	# validate input
	if selection not in ['providers', 'operatories']:
		abort(400, 'Please select providers or operatories to search!')

	# get availability
	days = next_seven_days()
	availability = [[]]
	if selection == 'providers':
		availability = get_provider_availability(name, days)
	else:
		availability = get_operatory_availability(name, days)
	
	availability = [[1,11,111], [22], [3,33], [], [5,55], [6,66], [7,77]]

	return render_template('availability.html', name=name, days=days, availability=availability)


@app.route('/confirmation')
def confirmation():

	# parse input
	name = request.args.get('name')
	day = request.args.get('day')
	time = request.args.get('time')

	return render_template('confirmation.html', name=name, day=day, time=time) 

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
