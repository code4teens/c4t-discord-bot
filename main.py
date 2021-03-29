import discord
import os
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
  print(f'{client.user.name} Bot is online!')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('~help'):
    text = (
      'Available commands:\n'
      '>>> `~help` - Shows available commands.\n'
      '`~greet` - Greets user.'
    )
    await message.reply(text)

  if message.content.startswith('~greet'):
    text = f'Hello {message.author.name}!'
    await message.reply(text)

keep_alive()
client.run(os.getenv('TOKEN'))