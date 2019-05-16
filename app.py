from flask import Flask, render_template, request, abort
from helpers import get_unique_provider_names, get_unique_operatory_names

app = Flask(__name__)


@app.route('/')
def main():
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

	return render_template('list.html', selection=selection.capitalize(), names=names)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
