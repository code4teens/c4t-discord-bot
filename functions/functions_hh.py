import constants as c
import utilities as u

def print_keys():
  for index, key in enumerate(u.keys()):
    print(f'{index}: {key}: {u.get_value(key)}')

def get_role_members(bot, role_id):
  guild = bot.get_guild(c.guild_id)

  for role in guild.roles:
    if role.id == role_id:
      return role.members

def student_chunks(bot, n):
  members = get_role_members(bot, c.r_students_id)

  for i in range(0, len(members), n):
    yield members[i:i + n]

def channel_check(bot, message):
  dev_terminal_channel = bot.get_channel(c.c_dev_terminal_id)
  stu_ttb_channel = bot.get_channel(c.c_stu_ttb_id)

  if c.r_devs_id in [role.id for role in message.author.roles] \
  and message.channel.id != c.c_dev_terminal_id \
  and message.channel.id != c.c_stu_ttb_id:
    raise u.ChannelException(f'Kindly utilise me at {dev_terminal_channel.mention} or {stu_ttb_channel.mention}.')

  if c.r_students_id in [role.id for role in message.author.roles] \
  and message.channel.id != c.r_stu_ttb_id:
    raise u.ChannelException(f'Kindly utilise me at {stu_ttb_channel.mention}.')

def command_check(message):
  if c.r_devs_id not in [role.id for role in message.author.roles] \
  and (command := message.content.split()[0]) in c.dev_commands:
    raise u.CommandException(f'You are not authorised to use `{command}`!')

async def assign_command(bot, message):
  guild = bot.get_guild(c.guild_id)
  chunks = student_chunks(bot, 5)
  roles = [guild.get_role(village_id) for village_id in c.r_village_ids]
  
  for members in chunks:
    for index, member in enumerate(members):
      await member.add_roles(roles[index])

  await message.add_reaction(c.tick_emoji)

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
    link = message.content[8:]
    bot_id = link[51:69]
    key = f'{bot_id}-add-bot'

    if key not in u.keys():
      channel = bot.get_channel(c.dev_log_id)
      log_message = await channel.send(link)
      u.put(log_message.id, key)

      await message.reply('The Devs will add your bot into the server soon.')
        
    else:
      await message.reply('You already submitted a request for this bot.')

  else:
    await message.reply('`$addbot [bot-invite-link]`')

async def adopt_command(message):
  match = u.re_search(c.adopt_regex, message.content)

  if match:
    member = message.mentions[0]

    if member.bot:
      author_role = [role for role in message.author.roles if role.id in c.r_village_ids]
      bot_role = [role for role in member.roles if role.id in c.r_village_ids]

      if len(author_role) == 1 and len(bot_role) == 0:
        key = f'{message.author.id}-adopt'

        if key not in u.keys():
          u.put_value(member.id, key)
          reason = f'{message.author} adopted {member}.'

          await member.add_roles(author_role[0], reason = reason)
          await message.reply(f'{member.mention} has been adopted into {author_role[0].mention}.')

        else:
          await message.reply(f'You have already adopted a bot into {author_role[0].mention}.')

      else:
        await message.reply(f'You are not authorised to adopt {member.mention}.')

  else:
    await message.reply('`$adopt [@member]`')

async def release_command(message):
  match = u.re_search(c.release_regex, message.content)

  if match:
    member = message.mentions[0]

    if member.bot:
      author_role = [role for role in message.author.roles if role.id in c.r_village_ids]
      bot_role = [role for role in member.roles if role.id in c.r_village_ids]
      key = f'{message.author.id}-adopt'
    
      if key in u.keys() and len(bot_role) == 1:
        reason = f'{message.author} released {member}.'

        await member.remove_roles(bot_role[0], reason = reason)
        await message.reply(f'{member.mention} has been released from {bot_role[0].mention}.')

      else:
        await message.reply(f'You are not authorised to release {member.mention}.')

  else:
    await message.reply('`$release [@bot]`')

async def agree_coc_check(bot, payload):
  guild = bot.get_guild(payload.guild_id)
  channel = bot.get_channel(payload.channel_id)
  member = guild.get_member(payload.user_id)
  emoji = str(payload.emoji)

  if guild.id == c.guild_id and channel.id == c.c_imp_coc_id and len(member.roles) == 1 and emoji == c.ok_emoji:
    u.put(0, f'{member.id}-stats-level')
    u.put(0, f'{member.id}-stats-xp')
    u.put(0, f'{member.id}-stats-last')

    role = guild.get_role(c.r_students_id)
    reason = f'{member} agreed to Code of Conduct.'
    welcome_channel = bot.get_channel(c.c_imp_introduction_id)
    alerts_channel = bot.get_channel(c.c_imp_alerts_id)

    await member.add_roles(role, reason = reason)
    await welcome_channel.send(f'Welcome {member.mention}! Kindly check out {alerts_channel.mention}')

async def bot_join_check(bot, member):
  if member.bot:
    key = f'{member.id}-add-bot'

    try:
      message_id = int(u.get_value(key))
    
    except Exception as e:
      print(f'ERROR: bot_join_check({member.name}: {member.id}): {e}')

    else:
      log_channel = bot.get_channel(c.c_dev_log_id)
      message = await log_channel.fetch_message(message_id)
      
      await message.add_reaction(c.tick_emoji)

    finally:
      role = member.guild.get_role(c.r_student_bots_id)
      welcome_channel = bot.get_channel(c.c_imp_introduction_id)

      await member.add_roles(role)
      await welcome_channel.send(f'Welcome {member.mention}!')

async def give_students_xp(message):
  if c.r_students_id in [role.id for role in message.author.roles]:
    lvl_key = f'{message.author.id}-stats-level'
    xp_key = f'{message.author.id}-stats-xp'
    last_key = f'{message.author.id}-stats-last'
    level = u.get_value(lvl_key)
    xp = u.get_value(xp_key)
    last = u.get_value(last_key)
    now = u.get_epoch()

    if now - last > 3:
      xp += 10
      next_level_xp = 5 * level ** 2 + 50 * level + 100

      if xp >= next_level_xp:
        level += 1
        xp -= next_level_xp
        
        await message.reply(f'You have been promoted to Level {level}!')

      u.put(level, lvl_key)
      u.put(xp, xp_key)
      u.put(now, last_key)

async def joke_command(message):
  try:
    data = u.requests_get('https://official-joke-api.appspot.com/random_joke').json()

  except Exception as e:
    print(f'ERROR: $joke: {e}')

    await message.reply('Something weng wrong..')

  else:
    await message.reply(f'{data["setup"]}\n\n{data["punchline"]}')

async def ip_command(message):
  try:
    data = u.requests_get('https://api.ipify.org/?format=json').json()

  except Exception as e:
    print(f'ERROR: $ip: {e}')

    await message.reply('Something weng wrong..')

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