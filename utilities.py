from bs4 import BeautifulSoup
from flask import Flask
from replit import db
from threading import Thread
import asyncio
import datetime
import pytz
import random
import re
import requests
import time

class CommandException(Exception):
  pass

class ChannelException(Exception):
  pass

def beautiful_soup(content, parser):
  return BeautifulSoup(content, parser)

app = Flask('')

@app.route('/')
def home():
  return 'Code4Teens Bot is online!'

def run():
  app.run(host = '0.0.0.0', port = 8080)

def keys():
  return db.keys()

def get_value(key):
  return db[key]

def del_value(key):
  del db[key]

def put(value, key):
  db[key] = value

def keep_alive():
  t = Thread(target = run)
  t.start()

def asyncio_get_event_loop():
  return asyncio.get_event_loop()

async def asyncio_sleep(s):
  await asyncio.sleep(s)

def get_now():
  akl_tz = pytz.timezone('Asia/Kuala_Lumpur')
  now = datetime.datetime.now(akl_tz)
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

def re_search(regex, string):
  return re.search(regex, string)

def requests_get(URL):
  r = requests.get(URL)

  if r.status_code == 200:
    return r

  else: 
    raise Exception(r.status_code)

def get_epoch():
  return int(time.time())