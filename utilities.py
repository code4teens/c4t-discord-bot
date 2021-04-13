import re
import requests
import time
from flask import Flask
from replit import db
from threading import Thread

app = Flask('')

def re_search(regex, string):
  return re.search(regex, string)

def get_JSON(URL):
  r = requests.get(URL)

  if r.status_code == 200:
    return r.json()

  else: 
    raise Exception(r.status_code)

def get_epoch():
  return int(time.time())

def keys():
  return db.keys()

def get_value(key):
  return db[key]

def del_value(key):
  try:
    del db[key]

  except Exception as e:
    print(f'ERROR: $del_value({key}): {e}')

def put(value, key):
  db[key] = value

@app.route('/')
def main():
  return 'Bot is still online!'

def run():
  app.run(host = '0.0.0.0', port = 8080)

def keep_alive():
  t = Thread(target = run)
  t.start()

class DevException(Exception):
  pass

class ChannelException(Exception):
  pass