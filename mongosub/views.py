from . import app
from . import socketio
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit,send
from flask_socketio import join_room, leave_room

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@socketio.on('field changes')
def subscribe_db_field_changes(data):
    room=data['room']
    join_room(room)
    emit('my response',{'data':'subscribed to field '+str(room)})

@socketio.on('all changes')
def subscribe_all_changes(data):
    room='all_changes'
    join_room(room)
    emit('my response',{'data':'subscribed to all changes in database'})
