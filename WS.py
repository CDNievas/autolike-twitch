import socketio
import os
import Tinder

sio = socketio.Client()
TinderClient = None

def setTinderClient(client):
    global TinderClient
    TinderClient = client

def connect(ip,port):
    sio.connect("http://{}:{}/".format(ip,port))
    print('Conectado correctamente a ChatTwitch Server')

@sio.on("handshake")
def handshake(data):
    sio.emit("handshake","tinder")

@sio.on('message')
def message(data):
    username = data["user"]

    try:
        likes = TinderClient.get_likes()
        matchs = TinderClient.get_matchs()
        msg = "TinderBot: @{}, di {} likes y tengo {} matchs".format(username, likes,matchs)

    except Exception as e:
        print(e)
        msg = "TinderBot: Hubo un error al extraer los datos de Tinder"

    finally:
        sio.emit('response', msg)

    

