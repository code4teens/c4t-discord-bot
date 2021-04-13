import random
import constants as c


def rps(msg, text):
  if msg == '$rock':
    if text == 'I choose rock!':
      resp = (random.choice(c.tielist))
    elif text == 'I choose scissors!':
      resp = (random.choice(c.winlist))
    elif text == 'I choose paper!':
      resp = (random.choice(c.loselist))
  elif msg == '$paper':
    if text == 'I choose rock!':
      resp = (random.choice(c.winlist))
    elif text == 'I choose scissors!':
      resp = (random.choice(c.loselist))
    elif text == 'I choose paper!':
      resp = (random.choice(c.tielist))
  elif msg == '$scissors':
    if text == 'I choose rock!':
      resp = (random.choice(c.loselist))
    elif text == 'I choose scissors!':
      resp = (random.choice(c.tielist))
    elif text == 'I choose paper!':
      resp = (random.choice(c.winlist))
  return resp