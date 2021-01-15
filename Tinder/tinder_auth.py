import json, requests

from Tinder.globals import get_headers, URL
from Tinder.Exceptions import TinderAuthError

headers = get_headers.copy()
headers['content-type'] = "application/json"

def login_tinder(fb_token,fb_id):
    return get_tinder_auth_token(fb_token,fb_id)
    
def get_tinder_auth_token(fb_auth_token, fb_user_id):
    url = URL + '/v2/auth/login/facebook'
    req = requests.post(url,
        headers=headers,
        data=json.dumps(
            {'token': fb_auth_token, 'facebook_id': fb_user_id})
        )
    try:
        tinder_auth_token = req.json()["data"]["api_token"]
        return tinder_auth_token
    except Exception as e:
        raise TinderAuthError("Something went wrong. Sorry, but we could not authorize you.", req)
