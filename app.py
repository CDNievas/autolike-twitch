import sys, os, time
from dotenv import load_dotenv
from pathlib import Path
from random import randint

import WS
from Tinder.Exceptions import TinderAuthError, FBAuthError
from Tinder.Client import TinderClient

from Tinder.Exceptions import MyError

load_dotenv()

TOKENS_PATH = os.path.dirname(os.path.abspath(__file__)) + "/.tokens"

IP_WS = os.environ.get("IP_WS")
PORT_WS = os.environ.get("PORT_WS")

client = None

def startTinderClient():
    global client
    if(os.path.exists(TOKENS_PATH)):
        load_dotenv(dotenv_path=TOKENS_PATH)
        client = TinderClient()
        TINDER_TOKEN = os.environ.get("TINDER_TOKEN")
        client.set_tinder_token(TINDER_TOKEN)

    else:
        try:
            FB_USER = os.environ.get("FB_USER")
            FB_PWD = os.environ.get("FB_PWD")
            client = TinderClient(FB_USER, FB_PWD)
        except (FBAuthError, TinderAuthError) as e:
            print(e.error.headers,e.error.json())
    print("Conectado a Tinder correctamente")

def startWS(client):
    WS.connect(IP_WS,PORT_WS)
    WS.setTinderClient(client)

def startAutoLike():
    global client

    print("Empezando a dar likes automaticos")
    while True:
        recs = client.get_recs()
        print("Encontrados {} recomendados".format(len(recs)))
        for rec in recs:
            try:
                client.likeRec(rec["_id"])
            except TinderLikeError as e:
                print(e.error.headers, e.error.json())
            time.sleep(randint(1,5))

        nxtTime = randint(2400,5400)
        print("Proxima iteración de likes en {} minutos".format(nxtTime/60))
        time.sleep(nxtTime)

startTinderClient()
startWS(client)
startAutoLike()
