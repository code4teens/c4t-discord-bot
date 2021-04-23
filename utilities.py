import asyncio
import datetime
import pytz
import random
import re
import requests
import string
from bs4 import BeautifulSoup
from enum import Enum
from flask import Flask
from replit import db
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return 'Code4Teens Bot is online!'

def run():
  app.run(host = '0.0.0.0', port = 8080)

def keep_alive():
  t = Thread(target = run)
  t.start()

class Alert(Enum):
  MESSAGE = 1
  FILE = 2
  FUNCTION = 3
  COROUTINE = 4

class CommandException(Exception):
  pass

class ChannelException(Exception):
  pass

def keys():
  return db.keys()

def get_value(key):
  return db[key]

def del_value(key):
  del db[key]

def put(value, key):
  db[key] = value

def print_keys():
  for index, key in enumerate(keys()):
    print(f'{index + 1}: {key}: {get_value(key)}')

def asyncio_get_event_loop():
  return asyncio.get_event_loop()

async def asyncio_sleep(s):
  await asyncio.sleep(s)

def get_now_str():
  a_kl_tz = pytz.timezone('Asia/Kuala_Lumpur')
  now = datetime.datetime.now(a_kl_tz)
  date_str = now.strftime('%Y-%m-%d')
  time_str = now.strftime('%H:%M')

  return date_str, time_str

def get_date_time_from_str(date_time_str, format):
  return datetime.datetime.strptime(date_time_str, format)

def get_str_from_date_time(date_time, format):
  return date_time.strftime(format)

def get_delta_day(d):
  return datetime.timedelta(days = d)

def random_choice(obj):
  return random.choice(obj)

def random_shuffle(obj):
  random.shuffle(obj)

  return obj

def re_search(regex, string):
  return re.search(regex, string)

def requests_get(URL):
  r = requests.get(URL)

  if r.status_code == 200:
    return r

  else: 
    raise Exception(r.status_code)

def beautiful_soup(content, parser):
  return BeautifulSoup(content, parser)

def get_random_prefix():
  lower_alpha = string.ascii_lowercase
  symbols = [
    '~',
    '!',
    '%',
    '&',
    '?'
  ]
  key = 'prefixes'
  taken_prefixes = get_value(key)

  while True:
    prefix_1 = random.choice(lower_alpha)
    prefix_2 = random.choice(symbols)
    prefix = prefix_1 + prefix_2

    if prefix not in taken_prefixes:
      taken_prefixes.append(prefix)
      put(taken_prefixes, key)

      return prefix