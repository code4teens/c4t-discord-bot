import discord
import constants as c
import functions_bc as bc
import functions_hans as fh
import functions_pp as pp
import utilities as u
import scrape
import io
import aiohttp
#import dailydocs
import threading
import random
from fpdf import FPDF 
from io import BytesIO
import time
import datetime
import get_time
from replit import db
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = discord.Client(intents = intents)

#sends the pdf TEST
async def send_task(day):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, "Hi all, here is today's task!")
    bstring = pdf.output(dest='S').encode('latin-1')
    channel = bot.get_channel(c.imp_alerts)
    await channel.send(file=discord.File(BytesIO(bstring), filename='sample.pdf'))

def set_start_day(day,month,year):
    for x in range(1,10):
        NextDay_Date = datetime.datetime(year,month,day) + datetime.timedelta(days=x)
        db['day' + str(x)] = str(NextDay_Date)[0:10]

async def check_to_send():
    if get_time.current_time() == send_task_time:
        await send_task(get_time.check_day())

def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(begin())
    loop.close()

async def begin():
    while True:
        await check_to_send()
        time.sleep(50)

send_task_time = '15:57'

set_start_day(13,4,2021)
dailydocs_thread = threading.Thread(target=between_callback)
dailydocs_thread.start()

@bot.event
async def on_ready():
  print(f'{bot.user.name} Bot is online!')

@bot.event
async def on_member_join(member):
  await fh.bot_join_check(bot, member)

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  await fh.give_students_xp(message)
  
  if message.content.startswith('$'):
    try:
      fh.dev_command_check(message)
      fh.channel_command_check(bot, message)

    except u.DevException as e:
      await message.reply(e)

    except u.ChannelException as e:
      await message.reply(e)
      
    else:
      if message.content == '$devhelp':
        await message.reply(c.dev_help_text)

      elif message.content.startswith('$attach'):
        await fh.attach_command(bot, message)

      elif message.content.startswith('$devecho'):
        await fh.devecho_command(bot, message)
      
      elif message.content == '$help':
        await message.reply(c.help_text)

      elif message.content.startswith('$addbot'):
        await fh.add_bot_command(bot, message)

      elif message.content == '$greet':
        await message.reply(f'Hello {message.author.name}!')

      elif message.content == '$joke':
        await fh.joke_command(message)

      elif message.content == '$ip':
        await fh.ip_command(message)

      elif message.content == '$iplocation':
        await fh.iplocation_command(message)

      elif message.content.startswith('$currency'):
        text = bc.exchange_rate_command()

        await message.reply(text)

      elif message.content.startswith('$movie'):
        text = bc.movie_command(message.content[7:])

        await message.reply(text)

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

      elif message.content.startswith('$emoji'):
        emoji = bc.emoji_command()

        await message.reply(emoji)

      elif message.content.startswith('$embed_emoji'):
        text = bc.embed_emoji_command()

        await message.reply(embed = text)

      elif message.content.startswith('$gif'):
        text = bc.gif_command()

        await message.reply(embed = text)

      elif message.content.startswith('$react'):
        msg = message.content[7:]
        if any(word in msg.lower() for word in bc.available_react):
          emoji = bc.react_command(message.content[7:])

          await message.add_reaction(emoji)
        
        else:
          text = bc.react_error()

          await message.reply(embed = text)
      
      elif message.content.startswith('$hello'):
        text = 'Hello!'
        
        await message.reply(text)
      
      #Praghetti Code

      elif message.content in c.rpslist:
        text = (random.choice(c.rpsans))
        await message.channel.send(text)
        await message.channel.send(pp.rps(message.content, text))

      #basic echo function
      elif message.content.startswith('$echo'):
        text = (message.content[5:].format(message))

        await message.channel.send(text)
      
      #echo + delete
      elif message.content.startswith('$say'):
        await message.channel.send(message.content[5:].format(message))
        await message.delete()
      
      #send img
      elif message.content.startswith('$intro'):
        await message.channel.send(file=discord.File('logo.png'))
        await message.channel.send('Hello coders! I am {} Nice to meet you! 😆'.format(message.author.mention))
      
      #send image from url
      
      elif message.content.startswith('$img'):
        async with aiohttp.ClientSession() as session:
          async with session.get('https://i.pinimg.com/originals/3c/90/c6/3c90c6359c4f0b887f4fea7e67a1f982.jpg') as resp:
            if resp.status != 200:
              return await message.channel.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await message.channel.send(file=discord.File(data, 'photo.jpg'))
      

      elif message.content.startswith('$job'):
        result = scrape.scrape_job()
        await message.reply(result)
        
      else:
          await message.reply('I do not recognise that command.')

@bot.event
async def on_raw_reaction_add(payload):
  await fh.agree_coc_check(bot, payload)

u.keep_alive()
bot.run(c.token)
dailydocs_thread.join()