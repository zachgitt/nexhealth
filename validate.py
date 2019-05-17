from flask import abort

def validate_selection(selection):
	if selection not in ['providers', 'operatories']:
		abort(400, 'Please select providers or operatories to search!')        

def validate_length(length):
	# check empty
	if length == '':
		abort(400, 'Please provide an appointment length between 5 and 60 minutes.')

	# validate value
	length = int(length)
	if (length % 5 != 0) or (length < 5) or (60 < length):
		abort(400, 'Uh oh, the schedule length must be between 5 and 60 and have a 5 minute interval.')

# TODO: validate name in database
def validate_name(name):
	True
