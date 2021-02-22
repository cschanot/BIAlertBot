from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import configparser

config_file = "../alerts.ini"

config = configparser.ConfigParser()


app = Flask(__name__)

@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		config.read(config_file)
		return render_template('cameras.html', config=config)


@app.route('/login', methods=['POST'])
def do_admin_login():
	if request.form['password'] == 'password' and request.form['username'] == 'admin':
		session['logged_in'] = True
	else:
		flash('wrong password!')
	return home()

@app.route('/cameras', methods=['POST'])
def do_set_alarms():
	config['camera_alerts'] = {}
	config['camera_alerts']['inside'] = request.form['inside']
	config['camera_alerts']['outside'] = request.form['outside']
	with open(config_file, 'w') as configfile:
		config.write(configfile)
	return home()

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=5555)
