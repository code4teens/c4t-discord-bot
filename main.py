import discord
import constants as c
import utilities as u
from functions import core
#from functions import functions_bb as bb
from functions import functions_bc as bc
from functions import functions_hh as hh
from functions import functions_pp as pp

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = discord.Client(intents = intents)

@bot.event
async def on_ready():
  print(f'{bot.user.name} Bot is online!')
  u.print_keys()
  loop = u.asyncio_get_event_loop()
  loop.call_later(0, await core.check_schedule(discord, bot))

  #await bb.send_projects(discord, bot, '2021-04-17 08:42')

@bot.event
async def on_member_join(member):
  await core.on_member_join(bot, member)

@bot.event
async def on_member_remove(member):
  await core.on_member_remove(bot, member)

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  await core.give_students_xp(bot, message)
  
  if message.content.startswith('$'):
    try:
      core.channel_check(bot, message)
      core.command_check(bot, message)

    except u.ChannelException as e:
      await message.reply(e)

    except u.CommandException as e:
      await message.reply(e)
      
    else:
      if message.content == '$devhelp':
        await message.reply(c.dev_help_text)

      elif message.content.startswith('$attach'):
        await hh.attach_command(message)

      elif message.content.startswith('$devecho'):
        await hh.devecho_command(message)
      
      elif message.content == '$help':
        await message.reply(c.help_text)

      elif message.content.startswith('$addbot'):
        await hh.add_bot_command(bot, message)

      elif message.content.startswith('$adopt'):
        await hh.adopt_command(message)

      elif message.content.startswith('$release'):
        await hh.release_command(message)

      elif message.content == '$joke':
        await hh.joke_command(message)

      elif message.content == '$modules':
        await message.reply(c.modules_text)

      elif message.content.startswith('$hello'):
        await message.reply('Hello')

      elif message.content == '$greet':
        await message.reply(f'Hello {message.author.name}!')

      elif message.content.startswith('$echo'):
        await message.channel.send(message.content[5:])
      
      elif message.content.startswith('$say'):
        await message.delete()
        await message.channel.send(message.content[4:])

      elif message.content in c.rps:
        await pp.rps(message)

      elif message.content == '$emoji':
        await message.reply(u.random_choice(c.emojis))

      elif message.content == '$embed_emoji':
        await bc.embed_emoji_command(discord, message)

      elif message.content == '$gif':
        await bc.gif_command(discord, message)

      elif message.content == '$intro':
        await message.channel.send(file = discord.File('resources/logo.png'))
        await message.channel.send(f'Hello coders, I am {message.author.mention}! Nice to meet you! 😆')
      
      elif message.content == '$img':
        await bc.img_command(discord, message)
        #await bc.img_command_2(discord, message)

      elif message.content.startswith('$react'):
        await bc.react_command(discord, message)

      elif message.content.startswith('$new'):
        await bc.add_encourage_command(message)

      elif message.content.startswith('$list'):
        await bc.list_encourage_command(message)
      
      elif message.content.startswith('$delete'):
        await bc.del_encourage_command(message)
      
      elif message.content.startswith('$del_list'):
        await bc.del_list_command(message)

      elif message.content == '$currency':
        await bc.exchange_rate_command(message)

      elif message.content == '$job':
        await bc.scrape_job(message)

      elif message.content.startswith('$movie'):
        await bc.movie_command(message)
        
      elif message.content == '$ip':
        await hh.ip_command(message)

      elif message.content == '$iplocation':
        await hh.iplocation_command(message)

      else:
        await message.reply('I do not recognise that command.')

@bot.event
async def on_raw_reaction_add(payload):
  await core.on_ok_coc(bot, payload)

u.keep_alive()
bot.run(c.token)