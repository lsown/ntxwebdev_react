import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
#import ntxpi
import random

basedir = os.path.abspath(os.path.dirname(__file__))

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

#app.config['SQLALCHEMY_DATABASE_URI'] =\
#    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#app.config['SQLALfCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)

#aquarium = ntxpi.aquarium()

# runs every x seconds and updates values on WEBUI
aqdict = {
    'temp': random.randrange(0,30),
    'motor1' : 'ON FWD',
    'motor2' : 'ON BACK',
    'AqFlag' : random.randrange(0,2),
    'CleanFlag' : random.randrange(0,2),
    'WasteFlag' : random.randrange(0,2),
    'SpareFlag' : random.randrange(0,2),
    }

def aqState():
	while True:
		socketio.sleep(1)
		aqdict['temp'] = random.randrange(0,30)
		aqdict['CleanFlag'] = random.randrange(0,2)
		#pinstatus = aquarium.pinsIn
		socketio.emit('aqStatemsg', 
			{'data' : aqdict}, 
			namespace='/aqState')

#@app.shell_context_processor
#def make_shell_context():
#    return dict(db=db, User=User, Role=Role)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
	aqdict = {
    'temp': random.randrange(0,30),
    'motor1' : 'ON FWD',
    'motor2' : 'ON BACK',
    'AqFlag' : random.randrange(0,2),
    'CleanFlag' : random.randrange(0,2),
    'WasteFlag' : random.randrange(0,2),
    'SpareFlag' : random.randrange(0,2),
    }
	return render_template('index.html')

@app.route('/settings')
def settings():
	return render_template('settings.html')

@app.route('/analytics')
def analytics():
	return render_template('analytics.html')

@socketio.on('connect', namespace='/aqState')
def aqState_monitor():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(aqState)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
    #uncompleted

if __name__ == '__main__': 
  socketio.run(app, host='0.0.0.0',debug=True, use_reloader=False) 