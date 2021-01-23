import requests, os, sys, time
from random import randint

from Tinder.tinder_auth import login_tinder
from Tinder.fb_auth import login_fb
from Tinder.globals import get_headers, URL

from Tinder.Exceptions import TinderGetMatchesError, TinderGetRecsError, TinderLikeError, TinderPassError

from WS import sio

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TinderClient:

    headers = get_headers.copy()

    def __init__(self,fb_user=None,fb_pwd=None):
        if fb_user != None and fb_pwd != None:
            
            fb_token, fb_id = login_fb(fb_user,fb_pwd)
            tinder_token = login_tinder(fb_token,fb_id)

            self._saveOnFile(fb_token,fb_id,tinder_token)
            self.headers.update({"X-Auth-Token": tinder_token})

    def _saveOnFile(self,fb_token, fb_id, tinder_token):

        f = open(PATH + "/.tokens","w+")

        f.write("FB_TOKEN={}\r\nFB_ID={}\r\nTINDER_TOKEN={} \r\n".format(fb_token, fb_id, tinder_token))

    def set_tinder_token(self,tinder_token):
        self.headers.update({"X-Auth-Token": tinder_token})

    def get_matchs(self):
        f = open(PATH + "/.matchs","r")
        matchs = int(f.readline())
        f.close()
        return matchs

    def get_likes(self):
        f = open(PATH + "/.likes","r")
        likes = int(f.readline())
        f.close()
        return likes

    def get_recs(self):

        url = URL + "/user/recs"
        req = requests.get(url,
            headers=self.headers
        )
        
        json = req.json()

        if(json["status"] != 200):
            raise TinderGetRecsError("No se pudieron extraer los recomendados", req)
        
        return json["results"]

    def likeRec(self,id):

        url = URL + "/like/" + id
        req = requests.get(url,
            headers=self.headers
        )
        
        json = req.json()
        match = json["status"]

        if(json["status"] != 200):
            raise TinderLikeError("No se pudo dar like", req)
        
        f = open(PATH + "/.likes","r+")
        likes = int(f.readline()) + 1
        f.seek(0)
        f.write(str(likes))
        f.close()

        if(json["match"]):
            f = open(PATH + "/.matchs","r+")
            likes = int(f.readline()) + 1
            f.seek(0)
            f.write(str(likes))
            f.close()

    def passRec(self,id):

        url = URL + "/pass/" + id
        req = requests.get(url,
            headers=self.headers
        )

        json = req.json()

        if(json["status"] != 200):
            raise TinderPassError("No se pudo dar Pass", req)

    def startAutoLike(self):
        print("Empezando a dar likes automaticos")
        sio.emit("info","TinderBot: Empezando a dar likes automáticos")
        while True:
            recs = self.get_recs()
            print("Encontrados {} recomendados".format(len(recs)))
            sio.emit("info","TinderBot: Encontrados {} recomendados".format(len(recs)))
            for rec in recs:
                try:
                    self.likeRec(rec["_id"])
                except TinderLikeError as e:
                    print(e.error.headers, e.error.json())
                time.sleep(randint(1,5))

            nxtTime = randint(2400,5400)
            print("Proxima iteración de likes en {} minutos".format(round(nxtTime/60,0)))
            sio.emit("info","TinderBot: Proxima iteración de likes en {} minutos".format(round(nxtTime/60,0)))
            time.sleep(nxtTime)