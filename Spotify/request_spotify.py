import json
import os
import base64
from requests import post,get

import dotenv

#client_id = os.getenv('CLIENT_ID')
#client_secret = os.getenv('CLIENT_SECRET')



class SpotifyRequest:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self):
        auth_string = self.client_id + ":" + self.client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
        url = "https://accounts.spotify.com/api/token"
        headers = {"Authorization": "Basic " + auth_base64,
                   "Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        print(token,json_result)
        return token



