import requests
from bs4 import BeautifulSoup
from replit import db
import random
import discord

def movie_command(word):
    if word == '':
      return ('Please enter a movie name.')

    r = requests.get("https://www.imdb.com/find?q={}&s=tt&ttype=ft&ref_=fn_ft".format(word))
    soup = BeautifulSoup(r.content, "html.parser")
    result = soup.find("td",attrs={"class":"result_text"})
    movie_link = result.a.get('href')
    movie_name = result.a.text

    r = requests.get("https://www.imdb.com" + movie_link)
    soup = BeautifulSoup(r.content, "html.parser")
    parent = soup.find("div",attrs={"class":"credit_summary_item"})
    director = parent.a.text
    msg = "Movie Name: {} \nDirector: {}".format(movie_name, director)
    return msg

def update_encoragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def add_encourage_command(msg):
  encouraging_message = msg
  update_encoragements(encouraging_message)
  return 'New encouraging message added.'

def list_encourage_command():
  encouragements = []
  if "encouragements" in db.keys():
    encouragements = db["encouragements"].value
    return encouragements

def del_encourage_command(msg):
  encouragements = []
  if "encouragements" in db.keys():
    index = int(msg)
    delete_encouragement(index)
    encouragements = db["encouragements"]
    return 'Encouraging message deleted.'

def del_list_command(msg):
  encouragements = []
  if "encouragements" in db.keys():
    index = int(msg)
    delete_encouragement(index)
    encouragements = db["encouragements"].value
    result = "Encouraging message deleted.\nUpdating the list:\n{}".format(encouragements)
    return (result)

emoji_list = [
  ":teddy_bear:",
  ":heart_eyes:",
  ":clap:",
  ":pleading_face:",
  ":smiling_face_with_3_hearts:",
  ":woman_facepalming:",
  ":laughing:",
  ":smirk:",
  ":eyes:",
  ":woozy_face:",
  ":exploding_head:",
  ":neutral_face:",
  ":partying_face:",
  ":money_mouth:",
  ":ghost:",
]

def emoji_command():
  random_emoji = random.choice(emoji_list)
  return (random_emoji)


def embed_emoji_command():
  random_emoji = random.choice(emoji_list)

  embedVar = discord.Embed(title="Emoji Function ON", description="Randomly picking one emoji for you: ", 
  color=0x4b0082)

  embedVar.add_field(name=random_emoji + "\n\n", value="Do you like this emoji?", inline=False)

  return (embedVar)

gif_list = [
  'https://media1.tenor.com/images/861409ba9b00e46a67f4f7be00cee2f7/tenor.gif?itemid=16992959',
  'https://media1.tenor.com/images/a7ae94274d1bc120b1a59382ef5ac66b/tenor.gif?itemid=13418523',
  'https://media1.tenor.com/images/24ac13447f9409d41c1aecb923aedf81/tenor.gif?itemid=5026057',
  'https://media1.tenor.com/images/f6f02f22f3da8a85d8f600a947144b6d/tenor.gif?itemid=17202817',
  'https://media1.tenor.com/images/0796f5445e9730634315351c86d00e99/tenor.gif?itemid=15323902',
  'https://media1.tenor.com/images/ed628307910258f8d23796b7029faa19/tenor.gif?itemid=12251780',
  'https://media1.tenor.com/images/1c7bc370dc6ac84cc79660eba1f4f2c7/tenor.gif?itemid=15443300',
  'https://media1.tenor.com/images/119dd3797490c22e49cf42e5357fb719/tenor.gif?itemid=4869672',
  'https://media1.tenor.com/images/5a85818cb17039f20e3c31ba87005b72/tenor.gif?itemid=17640265',
  'https://media1.tenor.com/images/d3dac1b007907d196e3235d7fe251efe/tenor.gif?itemid=16999811',
  'https://media1.tenor.com/images/58de9f3c43b92e5f4cacc57714fd9fa5/tenor.gif?itemid=16216173'
]

def gif_command():
  random_gif = random.choice(gif_list)

  embedVar = discord.Embed(title="GIFs Function ON", description="Randomly picking one GIF for you: ", 
  color=0xee82ee)
  
  embedVar.set_image(url = random_gif)

  return (embedVar)

available_react = ["happy", "sad", "love", "wow", "lol", "teddy"]

def react_command(word):
  if word.lower() == "happy":
    return ("😄")

  elif word.lower() == "sad":
    return ("☹️")

  elif word.lower() == "love":
    return ("🥰")

  elif word.lower() == "wow":
    return ("🤩")
    
  elif word.lower() == "lol":
    return ("🤣")

  elif word.lower() == "teddy":
    return ("🧸")
      
  else:
    return ("⛔")

def react_error():
  embedVar = discord.Embed(title="**Command Error**",description="Try: `%react [Available Options]`\n" , color=0xff0000)
    
  embedVar.add_field(name="Available Options: ",
   value="1. happy\n"
        "2. sad\n"
        "3. love\n"
        "4. wow\n"
        "5. lol\n"
        "6. teddy\n", inline=False)
    
  return (embedVar)

def exchange_rate_command():
  url = 'https://mtradeasia.com/main/daily-exchange-rates/'
  r = requests.get(url)
  soup = BeautifulSoup(r.content, "html.parser")
  #get currency name
  parent = soup.find("td",attrs={"style":"line-height: 1;"})
  child = parent.find("small", attrs={"class":"spansmall"})
  currency = child.br.next_sibling
  update_currency = " ".join(currency.split())

  #get currency rate
  webuy = soup.find("td", attrs={"class":"text-center"}).text
  rate = " ".join(webuy.split())
  msg = "Currency: {}\nExchange Rate (MYR): {}".format(update_currency, rate)
  return msg