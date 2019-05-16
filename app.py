from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main():
	return render_template('select.html')

@app.route('/list', methods=['POST'])
def list():
	return render_template('list.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
