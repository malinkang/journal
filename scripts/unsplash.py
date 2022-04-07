#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from scipy import rand
BASE_URL = 'https://api.unsplash.com/'
ACCESS_KEY = "b0cbd23d5d1b188ffbf313d0c78071280f3d506d0279a1d31302ad87548b1beb"
def random():
    params = {"client_id": ACCESS_KEY, "orientation": "landscape"}
    r = requests.get(BASE_URL+'photos/random', params=params)
    cover = r.json().get("urls").get("small")
    return cover

def topics():
    params = {"client_id": ACCESS_KEY}
    r = requests.get(BASE_URL+'/topics', params=params)
    print(r.text)


print(random())