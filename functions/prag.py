import random

import constants as c

async def rps(message):
  ans = random.choice(c.rps_ans)

  if message.content == '$rock':
    if ans == 'I choose rock!':
      resp = random.choice(c.rps_tie)

    elif ans == 'I choose paper!':
      resp = random.choice(c.rps_lose)

    elif ans == 'I choose scissors!':
      resp = random.choice(c.rps_win)

  elif message.content == '$paper':
    if ans == 'I choose rock!':
      resp = random.choice(c.rps_win)

    elif ans == 'I choose paper!':
      resp = random.choice(c.rps_tie)

    elif ans == 'I choose scissors!':
      resp = random.choice(c.rps_lose)

  elif message.content == '$scissors':
    if ans == 'I choose rock!':
      resp = random.choice(c.rps_lose)

    elif ans == 'I choose paper!':
      resp = random.choice(c.rps_win)

    elif ans == 'I choose scissors!':
      resp = random.choice(c.rps_tie)
      
  await message.channel.send(ans)
  await message.channel.send(resp)