#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
BASE_URL = 'https://api.unsplash.com/'
# ACCESS_KEY = "b0cbd23d5d1b188ffbf313d0c78071280f3d506d0279a1d31302ad87548b1beb"
ACCESS_KEY = "cXKRBgzoILHbD1OhNZs3f5hiZBFJWSrp3K1NiA2XGeM"
def random():
    params = {"client_id": ACCESS_KEY, "orientation": "landscape"}
    r = requests.get(BASE_URL+'photos/random', params=params)
    cover = r.json().get("urls").get("small")
    return cover

def topics():
    params = {"client_id": ACCESS_KEY}
    r = requests.get(BASE_URL+'/topics', params=params)
    print(r.text)
