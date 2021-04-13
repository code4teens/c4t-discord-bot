import constants as c
import utilities as u

def get_role_members(bot, guild_id, role_id):
  guild = bot.get_guild(guild_id)

  for role in guild.roles:
    if role.id == role_id:
      return role.members

def dev_command_check(message):
  if c.devs not in [role.id for role in message.author.roles] \
  and (command := message.content.split()[0]) in c.dev_command_list:
    raise u.DevException(f'You are not authorised to use `{command}`!')

def channel_command_check(bot, message):
  dev_terminal_channel = bot.get_channel(c.dev_terminal)
  stu_ttb_channel = bot.get_channel(c.stu_ttb)

  if c.devs in [role.id for role in message.author.roles] \
  and message.channel.id != c.dev_terminal \
  and message.channel.id != c.stu_ttb:
    raise u.ChannelException(f'Kindly utilise me at {dev_terminal_channel.mention} or {stu_ttb_channel.mention}.')

  if c.students in [role.id for role in message.author.roles] \
  and message.channel.id != c.stu_ttb:
    raise u.ChannelException(f'Kindly utilise me at {stu_ttb_channel.mention}.')

async def attach_command(bot, message):
  match = u.re_search(c.attach_regex, message.content)

  if match:
    try:
      message_data = message.content.split(' ', 2)
      channel_id = int(message_data[1][2:20])
      description = message_data[2]

    except Exception as e:
      print(f'ERROR: $attach: {e}')

      await message.reply('Something went wrong..')

    else:
      if message.attachments:
        channel = bot.get_channel(channel_id)
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

async def devecho_command(bot, message):
  match = u.re_search(c.devecho_regex, message.content)
      
  if match:
    try:
      message_data = message.content.split(' ', 2)
      channel_id = int(message_data[1][2:20])
      text = message_data[2]
        
    except Exception as e:
      print(f'ERROR: $devecho: {e}')

      await message.reply('Something went wrong..')

    else:
      channel = bot.get_channel(channel_id)

      try:
        await channel.send(text)

      except Exception as e:
        print(f'ERROR: $devecho: {e}')

        await message.reply(f'I do not have write permissions in {channel.mention}.')
        
  else:
    await message.reply('`$devecho [#channel] [message]`')

async def add_bot_command(bot, message):
  match = u.re_search(c.add_bot_regex, message.content)

  if match:
    try:
      message_data = message.content.split(' ', 1)
      bot_id = int(message_data[1][51:69])
      link = message_data[1]

    except Exception as e:
      print(f'ERROR: $addbot: {e}')

      await message.reply('Something went wrong..')

    else:
      channel = bot.get_channel(c.dev_log)
      key = f'{bot_id}-add-bot'

      if key not in u.keys():
        try:
          log_message = await channel.send(link)
          u.put(log_message.id, key)

        except Exception as e:
          print(f'ERROR: $addbot: {e}')

          await message.reply('Something went wrong..')

        else:
          await message.reply('The Devs will add your bot into the server soon.')

      else:
        await message.reply('You already submitted a request for this bot.')

  else:
    await message.reply('`$addbot [bot-invite-link]`')

async def joke_command(message):
  try:
    data = u.get_JSON('https://official-joke-api.appspot.com/random_joke')

  except Exception as e:
    print(f'ERROR: $joke: {e}')

    await message.reply('Something weng wrong..')

  else:
    await message.reply(f'{data["setup"]}\n\n{data["punchline"]}')

async def ip_command(message):
  try:
    data = u.get_JSON('https://api.ipify.org/?format=json')

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

async def bot_join_check(bot, member):
  if member.guild.id == c.guild and member.bot:
    key = f'{member.id}-add-bot'

    try:
      message_id = int(u.get_value(key))
    
    except Exception as e:
      print(f'ERROR: bot_join_check({member.name}: {member.id}): {e}')

    else:
      log_channel = bot.get_channel(c.dev_log)
      message = await log_channel.fetch_message(message_id)
      
      await message.add_reaction(c.tick_emoji)

    finally:
      role = member.guild.get_role(c.student_bots)
      welcome_channel = bot.get_channel(c.stu_chit_chat)

      await member.add_roles(role)
      await welcome_channel.send(f'Welcome {member.mention}!')

async def give_students_xp(message):
  if c.students in [role.id for role in message.author.roles]:
    key = f'{message.author.id}-stats'
    lvl_key = f'{key}-level'
    xp_key = f'{key}-xp'
    last_key = f'{key}-last'

    try:
      level = u.get_value(lvl_key)
      xp = u.get_value(xp_key)
      last = u.get_value(last_key)

    except Exception as e:
      print(f'ERROR: give_students_xp({message.author.name}: {message.author.id}): {e}')

    else:
      now = u.get_epoch()

      if now - last > 3:
        xp += 10
        next_level_xp = 5 * level ** 2 + 50 * level + 100

        if xp >= next_level_xp:
          level += 1
          xp -= next_level_xp
          
          await message.reply(f'You have been promoted to Level {level}! Keep going at it!')

        u.put(level, lvl_key)
        u.put(xp, xp_key)
        u.put(now, last_key)

async def agree_coc_check(bot, payload):
  guild = bot.get_guild(payload.guild_id)
  channel = bot.get_channel(payload.channel_id)
  member = guild.get_member(payload.user_id)
  emoji = str(payload.emoji)

  if guild.id == c.guild and channel.id == c.imp_coc and len(member.roles) == 1 and emoji == c.ok_emoji:
    key = f'{member.id}-stats'
    u.put(0, f'{key}-level')
    u.put(0, f'{key}-xp')
    u.put(0, f'{key}-last')

    role = guild.get_role(c.students)
    reason = f'{member} agreed to Code of Conduct.'
    welcome_channel = bot.get_channel(c.stu_chit_chat)

    await member.add_roles(role, reason = reason)
    await welcome_channel.send(f'Welcome {member.mention}!')