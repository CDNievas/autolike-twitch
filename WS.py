import socketio

import Tinder

sio = socketio.Client()
TinderClient = None

def setTinderClient(client):
    global TinderClient
    TinderClient = client

def connect(IP,PORT):
    sio.connect("http://localhost:5000")
    print('Sucessfully connected to WS Server')

@sio.on("handshake")
def handshake(data):
    sio.emit("handshake","tinder")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.on('message')
def message(data):
    username = data["user"]

    try:
        likes = TinderClient.get_likes()
        matchs = TinderClient.get_matchs()
        msg = "@{}, el bot dio {} likes y tiene {} matchs".format(username, likes,matchs)

    except Exception as e:
        print(e)
        msg = "Hubo un error al extraer los datos de Tinder"

    finally:
        sio.emit('response', msg)

    

