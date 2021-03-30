import discord
import os
import helper
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
  print(f'{client.user.name} Bot is online!')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content == '~help':
    text = (
      'Available commands:\n'
      '>>> `~help` - Shows available commands.\n'
      '`~greet` - Greets user.\n'
      '`~joke` - d08 ex00\n'
      '`~ip` - d08 ex01\n'
      '`~iplocation` - d08 ex02&03'
    )

    await message.reply(text)

  if message.content == '~greet':
    text = f'Hello {message.author.name}!'

    await message.reply(text)

  if message.content == '~joke':
    try:
      data = helper.handle_request_from('https://official-joke-api.appspot.com/random_joke')

    except Exception as error:
      print(f'~joke: {error}')

      await message.reply('Something weng wrong..')

    else:
      text = f'{data["setup"]}\n\n{data["punchline"]}'
      
      await message.reply(text)

  if message.content == '~ip':
    try:
      data = helper.handle_request_from('https://api.ipify.org/?format=json')

    except Exception as error:
      print(f'~ip: {error}')

      await message.reply('Something weng wrong..')

    else:
      text = data["ip"]

      await message.reply(text)

  if message.content == '~iplocation':
    try:
      data1 = helper.handle_request_from('https://api.ipify.org/?format=json')
      ip = data1["ip"]
      data2 = helper.handle_request_from(f'https://ipinfo.io/{ip}/geo')
      data3 = helper.handle_request_from(f'https://api.ip2country.info/ip?{ip}')

    except Exception as error:
      print(f'~iplocation: {error}')

      await message.reply('Something weng wrong..')

    else:
      text = f'{data2["city"]}, {data2["region"]}, {data2["country"]}'
      emoji = data3["countryEmoji"]

      await message.add_reaction(emoji)
      await message.reply(text)

keep_alive()
client.run(os.getenv('TOKEN'))