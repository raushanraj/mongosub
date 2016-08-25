from mongosub import get_app,get_socket_app
socketio=get_socket_app()
app=get_app()

if __name__ == '__main__':
    socketio.run(app,debug=True)