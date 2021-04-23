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
    data1 = u.get_JSON('https://api.ipify.org/?format=json')
    ip = data1['ip']
    data2 = u.get_JSON(f'https://ipinfo.io/{ip}/geo')
    data3 = u.get_JSON(f'https://api.ip2country.info/ip?{ip}')

  except Exception as e:
    print(f'ERROR: $iplocation: {e}')

    await message.reply('Something went wrong..')

  else:
    await message.reply(f'{data2["city"]}, {data2["region"]}, {data2["country"]}')
    await message.add_reaction(data3['countryEmoji'])