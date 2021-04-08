import utilities as u

def set_stats(id):
  key = f'{id}-stats'
  u.put(0, f'{key}-level')
  u.put(0, f'{key}-xp')
  u.put(0, f'{key}-last')

def give_xp(message):
  key = f'{message.author.id}-stats'
  lvl_key = f'{key}-level'
  xp_key = f'{key}-xp'
  last_key = f'{key}-last'
  user_did_level_up = False

  try:
    level = u.get_value(lvl_key)
    xp = u.get_value(xp_key)
    last = u.get_value(last_key)

  except Exception as e:
    print(f'ERROR: give_xp({message.author.id}): {e}')

  else:
    now = u.get_epoch()

    if now - last > 3:
      xp += 10
      xp_to_next_level = 5 * level ** 2 + 50 * level + 100

      if xp >= xp_to_next_level:
        level += 1
        xp -= xp_to_next_level
        user_did_level_up = True

      u.put(level, lvl_key)
      u.put(xp, xp_key)
      u.put(now, last_key)

      if user_did_level_up:
        return f'{message.author.mention} has been promoted to Level {level}!'

def joke_command():
  try:
    data = u.get_JSON('https://official-joke-api.appspot.com/random_joke')

  except Exception as e:
    print(f'ERROR: ~joke: {e}')

    return 'Something weng wrong..'

  else:
    return f'{data["setup"]}\n\n{data["punchline"]}'

def ip_command():
  try:
    data = u.get_JSON('https://api.ipify.org/?format=json')

  except Exception as e:
    print(f'ERROR: ~ip: {e}')

    return 'Something weng wrong..'

  else:
    return data['ip']

def iplocation_command():
  d = dict()

  try:
    data1 = u.get_JSON('https://api.ipify.org/?format=json')
    ip = data1['ip']
    data2 = u.get_JSON(f'https://ipinfo.io/{ip}/geo')
    data3 = u.get_JSON(f'https://api.ip2country.info/ip?{ip}')

  except Exception as e:
    print(f'ERROR: ~iplocation: {e}')
    d['error'] = 'Something went wrong..'

    return d

  else:
    d['text'] = f'{data2["city"]}, {data2["region"]}, {data2["country"]}'
    d['emoji'] = data3['countryEmoji']

    return d