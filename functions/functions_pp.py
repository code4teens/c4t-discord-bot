import constants as c
import utilities as u

async def rps(message):
  ans = u.random_choice(c.rps_ans)

  if message.content == '$rock':
    if ans == 'I choose rock!':
      resp = u.random_choice(c.rps_tie)

    elif ans == 'I choose paper!':
      resp = u.random_choice(c.rps_lose)

    elif ans == 'I choose scissors!':
      resp = u.random_choice(c.rps_win)

  elif message.content == '$paper':
    if ans == 'I choose rock!':
      resp = u.random_choice(c.rps_win)

    elif ans == 'I choose paper!':
      resp = u.random_choice(c.rps_tie)

    elif ans == 'I choose scissors!':
      resp = u.random_choice(c.rps_lose)

  elif message.content == '$scissors':
    if ans == 'I choose rock!':
      resp = u.random_choice(c.rps_lose)

    elif ans == 'I choose paper!':
      resp = u.random_choice(c.rps_win)

    elif ans == 'I choose scissors!':
      resp = u.random_choice(c.rps_tie)
      
  await message.channel.send(ans)
  await message.channel.send(resp)