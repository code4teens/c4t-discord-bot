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
    text = helper.joke_command()

    await message.reply(text)

  if message.content == '~ip':
    text = helper.ip_command()

    await message.reply(text)

  if message.content == '~iplocation':
    d = helper.iplocation_command()

    if isinstance(d, dict):
      await message.reply(d['text'])
      await message.add_reaction(d['emoji'])

    else:
      await message.reply(d)

keep_alive()
client.run(os.getenv('TOKEN'))