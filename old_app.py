from flask import Flask, render_template, request, abort
app = Flask(__name__)

#from helpers import get_unique_provider_names, get_unique_operatory_names

@app.route('/')
def main():
	return render_template('select.html')

@app.route('/list', methods=['POST'])
def h():

	# parse input
	selection = request.form.get('selection')
	length = int(request.form.get('length'))

	# validate inputs
	if selection not in ['providers', 'operatories']:
		abort(404)
	if (length % 5) != 0 and (5 <= length <= 60):
		abort(404)		

	# display list of names
    names = []	
	#if selection == 'providers':
	#	names = get_unique_provider_names()	
	#else:
	#	names = get_unique_operatory_names() 

	return render_template('list.html', selection=selection)
	#return render_template('list.html', selection=selection.capitalize(), names=names)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
