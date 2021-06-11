import random

import aiohttp
import io
from bs4 import BeautifulSoup

import constants as c
import utilities as u

async def embed_emoji_command(discord, message):
  embedVar = discord.Embed(title = "Emoji Function ON", description = "Sending emoji: ", 
  color = 0x4b0082)
  emoji = random.choice(c.emojis)
  embedVar.add_field(name = f'{emoji}\n\n', value = "--- Successful ---", inline = False)

  await message.reply(embed = embedVar)

async def gif_command(discord, message):
  embedVar = discord.Embed(title = "GIFs Function ON", description = "Sending GIF: ", 
  color = 0xee82ee)
  gif = random.choice(c.gifs)
  embedVar.set_image(url = gif)

  await message.reply(embed = embedVar)

async def img_command(discord, message):
  async with aiohttp.ClientSession() as session:
    async with session.get('https://i.pinimg.com/originals/3c/90/c6/3c90c6359c4f0b887f4fea7e67a1f982.jpg') as resp:

      if resp.status == 200:
        data = io.BytesIO(await resp.read())

        await message.channel.send(file = discord.File(data, 'photo.jpg'))
        
      else:
        await message.channel.send('Could not download file...')

#async def img_command_2(discord, message):
#  url = 'https://i.pinimg.com/originals/3c/90/c6/3c90c6359c4f0b887f4fea7e67a1f982.jpg'
#  content = u.requests_get(url).content
#  open('photo.jpg', 'wb').write(content)

#  await message.channel.send(file = discord.File('photo.jpg'))

async def react_command(discord, message):
  msg = message.content[7:].lower()

  if msg == "happy":
    await message.add_reaction("😄")

  elif msg == "sad":
    await message.add_reaction("☹️")

  elif msg == "love":
    await message.add_reaction("🥰")

  elif msg == "wow":
    await message.add_reaction("🤩")
    
  elif msg == "lol":
    await message.add_reaction("🤣")

  elif msg == "teddy":
    await message.add_reaction("🧸")
      
  else:
    embedVar = discord.Embed(title = "**Command Error**",description = "Try: `$react [Available Options]`\n", color = 0xff0000)
    embedVar.add_field(name = "Available Options: ", value = (
      "1. happy\n"
      "2. sad\n"
      "3. love\n"
      "4. wow\n"
      "5. lol\n"
      "6. teddy\n"
     ), inline = False)
      
    await message.add_reaction("✔️")
    await message.reply(embed = embedVar)

async def add_encourage_command(message):
  encouraging_message = message.content[5:]

  if encouraging_message:
    key = 'encouragements'

    if key in u.keys():
      encouragements = u.get_value(key)
      encouragements.append(encouraging_message)
      u.put(encouragements, key)

    else:
      u.put([encouraging_message], key)

    await message.reply('New encouraging message added.')

  else:
    await message.reply('Please insert a message.')

async def list_encourage_command(message):
  key = 'encouragements'

  if key in u.keys():
    encouragements = u.get_value(key).value

    await message.reply(encouragements)

  else:
    await message.reply('No encouragements list available.')

async def del_encourage_command(message):
  msg = message.content[8:]

  if msg:
    key = 'encouragements'

    if key in u.keys():
      encouragements = u.get_value(key)
      index = int(msg)

      if index < len(encouragements):
        del encouragements[index]

        u.put(encouragements, key)

        await message.reply('Encouraging message deleted.')
        
      else:
        await message.reply('Unable to delete: Message does not exist.')
  
  else:
    await message.reply('Please insert the index of message.')

async def del_list_command(message):
  msg = message.content[10:]

  if msg:
    key = 'encouragements'
    
    if key in u.keys():
      encouragements = u.get_value(key).value
      index = int(msg)

      if index < len(encouragements):
        del encouragements[index]

        u.put(encouragements, key)
        
        await message.reply(f"Encouraging message deleted.\nUpdating the list:\n{encouragements}")

      else:
        await message.reply('Unable to delete: Message does not exist.')

  else:
    await message.reply('Please insert the index of message.')

async def scrape_name(message):
  url = 'https://webscraper.io/test-sites/tables'
  content = u.requests_get(url).content
  soup = BeautifulSoup(content, "html.parser")
  name1 = soup.tbody.tr.td.find_next("td")
  firstname = name1.text
  name2 = name1.find_next("td")
  lastname = name2.text
  name3 = name2.find_next("td")
  username = name3.text

  msg = f"First Name = {firstname} \nLast Name = {lastname} \nUsername = {username}"

  await message.reply(msg)


async def exchange_rate_command(message):
  url = 'https://mtradeasia.com/main/daily-exchange-rates/'
  content = u.requests_get(url).content
  soup = BeautifulSoup(content, "html.parser")

  #get currency name
  parent = soup.find("td", attrs = {"style": "line-height: 1;"})
  child = parent.find("small", attrs = {"class": "spansmall"})
  currency = child.br.next_sibling
  update_currency = " ".join(currency.split())

  #get currency rate
  webuy = soup.find("td", attrs = {"class": "text-center"}).text
  rate = " ".join(webuy.split())
  msg = f"Currency: {update_currency}\nExchange Rate (MYR): {rate}"
  
  await message.reply(msg)

async def scrape_job(discord,message):
  url = u.requests_get('https://my.wobbjobs.com/jobs')
  soup = BeautifulSoup(url.content, 'html.parser')
  #jobs
  for h in soup.find_all('h6'):
    jobs = soup.find_all('h6', class_="mdc-typography--body1")
    joblist = []
    for jobnames in jobs:
      joblist.append(jobnames.text)

  #company
  for p in soup.find_all('p', class_="mdc-typography--body2"):
    cname = soup.find_all('p', class_="mdc-typography--body2")
    cname_list = []
    for cnames in cname:
      cname_list.append(cnames.text)


  result = ["Job: " + x  + " , "+ "Company: " + y  for x, y in zip(joblist, cname_list)]
  output = "\n\n".join(result)

  embed_content= discord.Embed(title="Job List: ", description=output, color=14177041)

  await message.reply(embed=embed_content)

async def movie_command(message):
  word = message.content[7:]

  if word:
    url = f"https://www.imdb.com/find?q={word}&s=tt&ttype=ft&ref_=fn_ft"
    content = u.requests_get(url).content
    soup = BeautifulSoup(content, "html.parser")
    result = soup.find("td" ,attrs = {"class": "result_text"})
    movie_link = result.a.get('href')
    movie_name = result.a.text

    url_2 = f"https://www.imdb.com{movie_link}"
    content_2 = u.requests_get(url_2).content
    soup = BeautifulSoup(content_2, "html.parser")
    element = soup.find("a",attrs={"class":"ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})
    director = element.text
    msg = f"Movie Name: {movie_name} \nDirector: {director}"

    await message.reply(msg)

  else:
    await message.reply('Please enter a movie name.')