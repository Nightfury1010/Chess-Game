import socketio

sio = socketio.Client()

username = input("Enter your username: ")
room = input("Enter room name to join: ")

@sio.event
def connect():
    print("Connected to server!")
    sio.emit('join', {'username': username, 'room': room})

@sio.event
def status(data):
    print(data['message'])

@sio.event
def opponent_move(data):
    move = data['move']
    print(f"Opponent's move: {move}")

@sio.event
def disconnect():
    print("Disconnected from server.")

def send_move(move):
    sio.emit('move', {'room': room, 'move': move})

sio.connect('http://localhost:5000')

while True:
    move = input("Enter your move (or 'quit' to leave): ")
    if move.lower() == 'quit':
        sio.emit('leave', {'username': username, 'room': room})
        sio.disconnect()
        break
    send_move(move)
