from functions import functions_bb as bb
from functions import functions_bc as bc
from functions import functions_hh as hh
from functions import functions_pp as pp
import discord
import constants as c
import utilities as u

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = discord.Client(intents = intents)

@bot.event
async def on_ready():
  print(f'{bot.user.name} Bot is online!')
  #hh.print_keys()

  await bb.send_projects(discord, bot, '2021-04-17 14:03')

@bot.event
async def on_member_join(member):
  await hh.bot_join_check(bot, member)

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  await hh.give_students_xp(message)
  
  if message.content.startswith('$'):
    try:
      hh.channel_check(bot, message)
      hh.command_check(message)

    except u.ChannelException as e:
      await message.reply(e)

    except u.CommandException as e:
      await message.reply(e)
      
    else:
      if message.content == '$devhelp':
        await message.reply(c.dev_help_text)

      elif message.content == '$assign':
        await hh.assign_command(bot, message)

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
        await message.channel.send(message.content[5:])

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
  await hh.agree_coc_check(bot, payload)

u.keep_alive()
bot.run(c.token)