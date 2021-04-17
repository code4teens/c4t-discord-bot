import constants as c
import utilities as u

import aiohttp
import io

async def embed_emoji_command(discord, message):
  embedVar = discord.Embed(title = "Emoji Function ON", description = "Randomly picking one emoji for you: ", 
  color = 0x4b0082)
  random_emoji = u.random_choice(c.emojis)
  embedVar.add_field(name = f'{random_emoji}\n\n', value = "Do you like this emoji?", inline = False)

  await message.reply(embed = embedVar)

async def gif_command(discord, message):
  embedVar = discord.Embed(title = "GIFs Function ON", description = "Randomly picking one GIF for you: ", 
  color = 0xee82ee)
  random_gif = u.random_choice(c.gifs)
  embedVar.set_image(url = random_gif)

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
    embedVar = discord.Embed(title = "**Command Error**",description = "Try: `%react [Available Options]`\n", color = 0xff0000)
    embedVar.add_field(name = "Available Options: ", value = (
      "1. happy\n"
      "2. sad\n"
      "3. love\n"
      "4. wow\n"
      "5. lol\n"
      "6. teddy\n"
     ), inline = False)
      
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

async def exchange_rate_command(message):
  url = 'https://mtradeasia.com/main/daily-exchange-rates/'
  content = u.requests_get(url).content
  soup = u.beautiful_soup(content, "html.parser")
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

async def scrape_job(message):
  url = 'https://malaysia.indeed.com/jobs?q=python&l='
  text = u.requests_get(url).text
  soup = u.beautiful_soup(text, 'html.parser')
  job_name = soup.find('h2', class_ = 'title').a.text.replace("\n", '')
  comp_name = soup.find('span', class_ = 'company').text.replace("\n", '')
  location = soup.find('span', class_ = 'location accessible-contrast-color-location').text.replace("\n",'')

  idict = {}
  idict['Job name'] = job_name
  idict['Company name'] = comp_name
  idict['Location'] = location

  await message.reply(idict)

async def movie_command(message):
  word = message.content[7:]

  if word:
    url = f"https://www.imdb.com/find?q={word}&s=tt&ttype=ft&ref_=fn_ft"
    content = u.requests_get(url).content
    soup = u.beautiful_soup(content, "html.parser")
    result = soup.find("td" ,attrs = {"class": "result_text"})
    movie_link = result.a.get('href')
    movie_name = result.a.text

    url_2 = f"https://www.imdb.com{movie_link}"
    content_2 = u.requests_get(url_2).content
    soup = u.beautiful_soup(content_2, "html.parser")
    parent = soup.find("div", attrs = {"class": "credit_summary_item"})
    director = parent.a.text
    msg = f"Movie Name: {movie_name} \nDirector: {director}"

    await message.reply(msg)

  else:
    await message.reply('Please enter a movie name.')