import constants as c
import utilities as u

async def attach_command(message):
  match = u.re_search(c.attach_regex, message.content)

  if match:
    channel = message.channel_mentions[0]
    message_data = message.content.split(' ', 2)
    description = message_data[2]

    if message.attachments:
      file = await message.attachments[0].to_file()

      try:
        await channel.send(description, file = file)

      except Exception as e:
        print(f'ERROR: $attach: {e}')

        await message.reply(f'I do not have write permissions in {channel.mention}.')

    else:
      await message.reply('You forgot to include the attachment.')

  else:
    await message.reply('`$attach [#channel] [description]`')

async def devecho_command(message):
  match = u.re_search(c.devecho_regex, message.content)
      
  if match:
    channel = message.channel_mentions[0]
    message_data = message.content.split(' ', 2)
    text = message_data[2]

    try:
      await channel.send(text)

    except Exception as e:
      print(f'ERROR: $devecho: {e}')

      await message.reply(f'I do not have write permissions in {channel.mention}.')
        
  else:
    await message.reply('`$devecho [#channel] [message]`')

async def add_bot_command(bot, message):
  match = u.re_search(c.addbot_regex, message.content)

  if match:
    link = message.content.split()[1]
    bot_id = match.group(1)
    key = f'{bot_id}-add-bot'
    permission = int(match.group(2))

    if permission == c.p_student_bots:
      if key not in u.keys():
        channel = bot.get_channel(c.c_dev_log_id)
        log_message = await channel.send(link)
        u.put(log_message.id, key)

        await message.reply('The Devs will add your bot into the server soon.')
          
      else:
        await message.reply('You already submitted a request for this bot.')

    else:
      await message.reply('You are granting your bot the wrong permissions. Kindly reconfigure and resend invitation link.')

  else:
    await message.reply('`$addbot [bot-invite-link]`')

async def adopt_command(message):
  match = u.re_search(c.adopt_regex, message.content)

  if match:
    member = message.mentions[0]
    key = f'{message.author.id}-adopt'

    if key not in u.keys():

      if member.bot and member.id != c.u_dev_bot_id:
        author_role = [role for role in message.author.roles if role.id in c.r_village_ids]
        bot_role = [role for role in member.roles if role.id in c.r_village_ids]

        if len(author_role) == 1 and len(bot_role) == 0:
          u.put(member.id, key)
          reason = f'{message.author} adopted {member}.'

          await member.add_roles(author_role[0], reason = reason)
          await message.reply(f'You adopted {member.mention}.')

        else:
          await message.reply(f'You are not authorised to adopt {member.mention}.')

      else:
        await message.reply(f'You cannot adopt {member.mention}.')

    else:
      await message.reply(f'You have already adopted a bot.')

  else:
    await message.reply('`$adopt [@member]`')

async def release_command(message):
  match = u.re_search(c.release_regex, message.content)

  if match:
    member = message.mentions[0]
    key = f'{message.author.id}-adopt'

    if key in u.keys():
      bot_id = u.get_value(key)

      if member.id == bot_id:
        bot_role = [role for role in member.roles if role.id in c.r_village_ids]
      
        if len(bot_role) == 1:
          u.del_value(key)
          reason = f'{message.author} released {member}.'

          await member.remove_roles(bot_role[0], reason = reason)
          await message.reply(f'You released {member.mention} for adoption.')

        else:
          await message.reply('Something went wrong..')

      else:
        await message.reply('Unable to fulfill request.')

    else:
      await message.reply('You have yet to adopt a bot.')

  else:
    await message.reply('`$release [@bot]`')

async def joke_command(message):
  try:
    data = u.requests_get('https://official-joke-api.appspot.com/random_joke').json()

  except Exception as e:
    print(f'ERROR: $joke: {e}')

    await message.reply('Something went wrong..')

  else:
    await message.reply(f'{data["setup"]}\n\n{data["punchline"]}')

async def ip_command(message):
  try:
    data = u.requests_get('https://api.ipify.org/?format=json').json()

  except Exception as e:
    print(f'ERROR: $ip: {e}')

    await message.reply('Something went wrong..')

  else:
    await message.reply(data['ip'])

async def iplocation_command(message):
  try:
    data1 = u.get_JSON('https://api.ipify.org/?format=json')
    ip = data1['ip']
    data2 = u.get_JSON(f'https://ipinfo.io/{ip}/geo')
    data3 = u.get_JSON(f'https://api.ip2country.info/ip?{ip}')

  except Exception as e:
    print(f'ERROR: $iplocation: {e}')

    await message.reply('Something went wrong..')

  else:
    await message.reply(f'{data2["city"]}, {data2["region"]}, {data2["country"]}')
    await message.add_reaction(data3['countryEmoji'])