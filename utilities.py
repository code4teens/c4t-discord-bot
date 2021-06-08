import datetime
from enum import Enum
from threading import Thread

import pytz
import requests
from flask import Flask
from replit import db

app = Flask('')

@app.route('/')
def home():
  return 'Clockwork Bot is online!'

def run():
  app.run(host = '0.0.0.0', port = 8080)

def keep_alive():
  t = Thread(target = run)
  t.start()

class Alert(Enum):
  MESSAGE = 1
  FILE = 2
  COROUTINE = 3
  TEST_FILE = 5

class CommandException(Exception):
  pass

class ChannelException(Exception):
  pass

def keys():
  return sorted(db.keys())

def get_value(key):
  return db[key]

def del_value(key):
  del db[key]

def put(value, key):
  db[key] = value

def print_keys():
  for index, key in enumerate(keys()):
    print(f'{index + 1}: {key}: {get_value(key)}')

def get_now_str():
  a_kl_tz = pytz.timezone('Asia/Kuala_Lumpur')
  now = datetime.datetime.now(a_kl_tz)
  date_str = now.strftime('%Y-%m-%d')
  time_str = now.strftime('%H:%M')

  return date_str, time_str

def requests_get(URL):
  r = requests.get(URL)

  if r.status_code == 200:
    return r

  else: 
    raise Exception(r.status_code)