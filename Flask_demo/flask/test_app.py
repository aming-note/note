from flask import Flask,render_template
from flask_socketio import SocketIO,emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("test.html")

@socketio.on('msg')
def give_response(data):
    value = data.get('param')
    print(value)
    emit('res', 'nihao')

if __name__ == '__main__':
    socketio.run(app)