from flask import Flask
from flask.ext.socketio import SocketIO
from flask import Blueprint
import jinja2
from redispublisher import *
#blue prints
adminapp = Blueprint('adminapp', __name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('mongosub/templates/'),
])
#app.register_blueprint(adminapp,url_prefix='/auth')
socketio = SocketIO(app)

def publish_to_socket(channel):
    pubsub = r.pubsub()
    pubsub.subscribe([channel])
    while True:
        for item in pubsub.listen():
            socketio.emit('my response',{'data':item['data']})
def run():
    for key in ALL_FIELDS:
        pool.map(publish_to_socket, ALL_FIELDS)

socketio.start_background_task(target=run)

def get_app():
    return app

def get_socket_app():
    return socketio

#background task

from . import views
#import redispublisher


