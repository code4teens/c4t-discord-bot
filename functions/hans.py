import utilities as u

async def joke_command(message):
  try:
    data = u.requests_get('https://official-joke-api.appspot.com/random_joke').json()

  except Exception as e:
    print(f'ERROR: $joke: {e}')

    await message.reply('Something went wrong..')

  else:
    await message.reply(f'{data["setup"]}\n\n{data["punchline"]}')

async def ip_command(message):
  try:
    data = u.requests_get('https://api.ipify.org/?format=json').json()

  except Exception as e:
    print(f'ERROR: $ip: {e}')

    await message.reply('Something went wrong..')

  else:
    await message.reply(data['ip'])

async def iplocation_command(message):
  try:
    data1 = u.requests_get('https://api.ipify.org/?format=json').json()
    ip = data1['ip']
    data2 = u.requests_get(f'https://ipinfo.io/{ip}/geo').json()

  except Exception as e:
    print(f'ERROR: $iplocation: {e}')

    await message.reply('Something went wrong..')

  else:
    await message.reply(f'{data2["city"]}, {data2["region"]}, {data2["country"]}')

async def iplocation_2_command(message):
  try:
    data1 = u.requests_get('https://api.ipify.org/?format=json').json()
    ip = data1['ip']
    data2 = u.requests_get(f'https://ipinfo.io/{ip}/geo').json()
    data3 = u.requests_get(f'https://api.ip2country.info/ip?{ip}').json()

  except Exception as e:
    print(f'ERROR: $iplocation_2: {e}')

    await message.reply('Something went wrong..')

  else:
    await message.reply(f'{data2["city"]}, {data2["region"]}, {data2["country"]}')
    await message.add_reaction(data3['countryEmoji'])