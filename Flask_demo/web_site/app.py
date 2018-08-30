from flask import Flask,render_template
from flask_socketio import SocketIO,emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@socketio.on('button')
def message(button):
    emit('msg','http://cpc.people.com.cn/')

if __name__ == '__main__':
    socketio.run(app)
