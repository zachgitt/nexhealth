from flask import Flask, render_template, request
from helpers import get_unique_provider_names, get_unique_operatory_names, \
    get_provider_availability, get_operatory_availability, next_seven_days
from validate import validate_selection, validate_name, validate_length

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
    length = request.form.get('length')

    # validate inputs
    validate_selection(selection)
    validate_length(length)

    # display list of names
    names = []
    if selection == 'providers':
        names = get_unique_provider_names()
    else:
        names = get_unique_operatory_names()

    return render_template('list.html', selection=selection.capitalize(), names=names,
                           length=int(length))


@app.route('/availability')
def availability():
    # parse input
    selection = request.args.get('selection').lower()
    name = request.args.get('name')
    length = request.args.get('length')

    # validate input
    validate_selection(selection)
    validate_length(length)
    validate_name(name)

    # get availability
    days = next_seven_days()
    availability = [[]]
    if selection == 'providers':
        availability = get_provider_availability(name, days, int(length))
    else:
        availability = get_operatory_availability(name, days, int(length))

    return render_template('availability.html', name=name, days=days,
                           availability=availability)


@app.route('/confirmation')
def confirmation():
    # parse input
    name = request.args.get('name')
    day = request.args.get('day')
    time = request.args.get('time')

    # TODO: validate inputs

    return render_template('confirmation.html', name=name, day=day, time=time)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
