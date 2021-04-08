import discord
import constants as c
import functions_hans as fh
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents = intents)

@bot.event
async def on_ready():
  print(f'{bot.user.name} Bot is online!')

#  members = get_members(c.server, c.developer)
  
#  for member in members:
#    fh.set_stats(member.id)

@bot.event
async def on_member_join(member):
  fh.set_stats(member.id)
  channel = bot.get_channel(c.general)

  await channel.send(f'Welcome {member.author.mention}!')

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if c.developer in [role.id for role in message.author.roles] and message.channel.id == c.discussions:
    text = fh.give_xp(message)

    if text is not None:
      await message.channel.send(text)

  if message.content == '~help':
    text = (
      '```fix\n'
      '~help       - Shows (all?) commands.\n'
      '~greet      - Greets user.\n'
      '~joke       - d08 ex00\n'
      '~ip         - d08 ex01\n'
      '~iplocation - d08 ex02 & 03\n'
      '```'
    )

    await message.reply(text)

  if message.content == '~greet':
    text = f'Hello {message.author.name}!'

    await message.reply(text)

  if message.content == '~joke':
    text = fh.joke_command()

    await message.reply(text)

  if message.content == '~ip':
    text = fh.ip_command()

    await message.reply(text)

  if message.content == '~iplocation':
    d = fh.iplocation_command()

    if isinstance(d, dict):
      await message.reply(d['text'])
      await message.add_reaction(d['emoji'])

    else:
      await message.reply(d['error'])

def get_members(server_ID, role):
  guild = bot.get_guild(server_ID)

  for role_ in guild.roles:
    if role_.id == role:
      return role_.members

keep_alive()
bot.run(c.token)