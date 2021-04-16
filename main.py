from functions import functions_bb as bb
from functions import functions_bc as bc
from functions import functions_hh as hh
from functions import functions_pp as pp
import discord
import constants as c
import utilities as u

import scrape
import io
import aiohttp

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = discord.Client(intents = intents)

@bot.event
async def on_ready():
  print(f'{bot.user.name} Bot is online!')
  #hh.print_keys()

  await bb.send_projects(discord, bot, '2021-04-16 14:45')

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
        await hh.attach_command(bot, message)

      elif message.content.startswith('$devecho'):
        await hh.devecho_command(bot, message)
      
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

      #Praghetti Code
      elif message.content.startswith('$hello'):
        await message.reply('Hello')

      elif message.content == '$greet':
        await message.reply(f'Hello {message.author.name}!')

      #basic echo function
      elif message.content.startswith('$echo'):
        await message.channel.send(message.content[5:])
      
      #echo + delete
      elif message.content.startswith('$say'):
        await message.channel.send(message.content[5:])
        await message.delete()

      elif message.content in c.rps:
        await pp.rps(message)

      elif message.content.startswith('$emoji'):
        emoji = bc.emoji_command()

        await message.reply(emoji)

      elif message.content.startswith('$embed_emoji'):
        text = bc.embed_emoji_command()

        await message.reply(embed = text)

      elif message.content.startswith('$gif'):
        text = bc.gif_command()

        await message.reply(embed = text)

      #send img
      elif message.content.startswith('$intro'):
        await message.channel.send(file = discord.File('logo.png'))
        await message.channel.send('Hello coders! I am {} Nice to meet you! 😆'.format(message.author.mention))
      
      #send image from url
      elif message.content.startswith('$img'):
        async with aiohttp.ClientSession() as session:
          async with session.get('https://i.pinimg.com/originals/3c/90/c6/3c90c6359c4f0b887f4fea7e67a1f982.jpg') as resp:
            if resp.status != 200:
              return await message.channel.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await message.channel.send(file=discord.File(data, 'photo.jpg'))

      elif message.content.startswith('$react'):
        msg = message.content[7:]
        if any(word in msg.lower() for word in bc.available_react):
          emoji = bc.react_command(message.content[7:])

          await message.add_reaction(emoji)
        
        else:
          text = bc.react_error()

          await message.reply(embed = text)

      elif message.content.startswith('$new'):
        text = bc.add_encourage_command(message.content[5:])

        await message.reply(text)

      elif message.content.startswith('$list'):
        text = bc.list_encourage_command()

        await message.reply(text)
      
      elif message.content.startswith('$delete'):
        text = bc.del_encourage_command(message.content[8:])

        await message.reply(text)
      
      elif message.content.startswith('$del_list'):
        text = bc.del_list_command(message.content[10:])
          
        await message.reply(text)

      elif message.content.startswith('$currency'):
        text = bc.exchange_rate_command()

        await message.reply(text)

      elif message.content.startswith('$job'):
        result = scrape.scrape_job()

        await message.reply(result)

      elif message.content.startswith('$movie'):
        text = bc.movie_command(message.content[7:])

        await message.reply(text)
        
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
