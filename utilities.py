import requests
from replit import db

def get_JSON(URL):
  r = requests.get(URL)

  if r.status_code == 200:
    return r.json()

  else: 
    raise Exception(r.status_code)

def keys():
  return db.keys()

def get_value(key):
  return db[key]

def put(value, key):
  db[key] = value