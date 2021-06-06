import random
import re
import time

import asyncio

import constants as c
import utilities as u

def get_chunks(members, n):
  for i in range(0, len(members), n):
    yield members[i:i + n]

def get_member(bot, member_id):
  guild = bot.get_guild(c.guild_id)

  return guild.get_member(member_id)

def get_role(bot, role_id):
  guild = bot.get_guild(c.guild_id)

  for role in guild.roles:
    if role.id == role_id:
      return role

def get_category(bot, category_id):
  guild = bot.get_guild(c.guild_id)

  for category in guild.categories:
    if category.id == category_id:
      return category

def get_channel(bot, channel_id):
  return bot.get_channel(channel_id)

async def give_students_xp(bot, message):
  author = message.author
  r_students = get_role(bot, c.r_students_id)

  if r_students in author.roles:
    lvl_key = f'{author.id}-stats-level'
    xp_key = f'{author.id}-stats-xp'
    last_key = f'{author.id}-stats-last'
    level = u.get_value(lvl_key)
    xp = u.get_value(xp_key)
    last = u.get_value(last_key)
    now = int(time.time())

    if now - last > 3:
      xp += 10
      xp_next_level = 5 * level ** 2 + 50 * level + 100

      if xp >= xp_next_level:
        level += 1
        xp -= xp_next_level
        
        await message.reply(f'You have been promoted to Level {level}!')

      u.put(level, lvl_key)
      u.put(xp, xp_key)
      u.put(now, last_key)

async def assign_peers(bot):
  r_students = get_role(bot, c.r_students_id)
  students = r_students.members
  random.shuffle(students)
  key = 'code'
  code = int(u.get_value(key))
  strs = [(
    f'{r_students.mention}, below are your evaluation pairs for today:\n\n'
    '`CODE: EVALUATOR   <   >   EVALUATEE`'
  )]

  if len(students) > 1:
    for i in range(len(students)):
      if i == len(students) - 1:
        evaluatee = students[0]

      else:
        evaluatee = students[i + 1]
      
      channel_key = f'{evaluatee.id}-channel-id'
      channel = get_channel(bot, channel_key)
      evaluator_key = f'{evaluatee.id}-evaluator'

      try:
        prev_evaluator_id = int(u.get_value(evaluator_key))

      except Exception as e:
        print(f'ERROR: assign_peers(): {e}')

      else:
        prev_evaluator = get_member(bot, prev_evaluator_id)

        await channel.set_permissions(prev_evaluator, overwrite = None)
      
      finally:
        u.put(students[i].id, evaluator_key)
        code_str = str(code).zfill(4)
        strs.append(f'{code_str} : {students[i].name}   <   >   {evaluatee.name}')
        code += 1

        await channel.set_permissions(students[i], view_channel = True)

  elif len(students) == 1:
    channel_key = f'{students[0].id}-channel-id'
    channel = get_channel(bot, channel_key)
    evaluator_key = f'{students[0].id}-evaluator'

    try:
      prev_evaluator_id = int(u.get_value(evaluator_key))
      u.del_value(evaluator_key)

    except Exception as e:
      print(f'ERROR: assign_peers(): {e}')

    else:
      prev_evaluator = get_member(bot, prev_evaluator_id)

      await channel.set_permissions(prev_evaluator, overwrite=None)
    
    finally:
      code_str = str(code).zfill(4)
      strs.append(f'{code_str} : {students[0].name}   <   >   {students[0].name}')
      code += 1

  u.put(code, key)

  c_imp_alerts = get_channel(bot, c.c_imp_alerts_id)
  await c_imp_alerts.send('\n'.join(strs))

async def assign_villages(bot):
  r_villages = [get_role(bot, r_village_id) for r_village_id in c.r_village_ids]
  r_students = get_role(bot, c.r_students_id)
  students = r_students.members
  random.shuffle(students)
  chunks = get_chunks(students, 5)

  for chunk in chunks:
    for i, student in enumerate(chunk):
      await student.add_roles(r_villages[i])

async def check_schedule(discord, bot):
  while True:
    now_date_str, now_time_str = u.get_now_str()

    if now_date_str in c.schedule.keys():
      tasks = c.schedule[now_date_str]

      for task in tasks:
        time = task['time']
        type = task['type']
        payload = task['payload']
        message = task['message']

        if time == now_time_str:
          c_imp_alerts = get_channel(bot, c.c_imp_alerts_id)

          if type == u.Alert.MESSAGE:
            await c_imp_alerts.send(message)

          elif type == u.Alert.FILE:
            await c_imp_alerts.send(message, file = discord.File(payload))

          elif type == u.Alert.COROUTINE:
            await payload(bot)

    await asyncio.sleep(60)

def channel_check(bot, message):
  roles = message.author.roles
  r_devs = get_role(bot, c.r_devs_id)
  r_students = get_role(bot, c.r_students_id)
  c_dev_terminal = get_channel(bot, c.c_dev_terminal_id)
  c_bot_clockwork = get_channel(bot, c.c_bot_clockwork_id)

  if r_devs in roles and message.channel != c_dev_terminal and message.channel != c_bot_clockwork:
    raise u.ChannelException(f'Kindly utilise me at {c_dev_terminal.mention} or {c_bot_clockwork.mention}.')

  elif r_students in roles and message.channel != c_bot_clockwork:
    raise u.ChannelException(f'Kindly utilise me at {c_bot_clockwork.mention}.')

def command_check(bot, message):
  command = message.content.split()[0]
  roles = message.author.roles
  r_devs = get_role(bot, c.r_devs_id)

  if r_devs not in roles and command in c.dev_commands:
    raise u.CommandException(f'You are not authorised to use `{command}`!')

async def attach_command(message):
  match = re.search(c.attach_regex, message.content)

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
  match = re.search(c.devecho_regex, message.content)
      
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
  match = re.search(c.addbot_regex, message.content)

  if match:
    link = message.content.split()[1]
    bot_id = match.group(1)
    message_key = f'{bot_id}-add-bot-message-id'
    owner_key = f'{bot_id}-owner-id'
    permission = int(match.group(2))

    if permission == c.p_add_student_bot_int:
      if message_key not in u.keys():
        r_devs = get_role(bot, c.r_devs_id)
        c_dev_log = get_channel(bot, c.c_dev_log_id)
        log_message = await c_dev_log.send(f'{r_devs.mention} {link}')
        u.put(log_message.id, message_key)
        u.put(message.author.id, owner_key)

        await message.reply(f'The {r_devs.mention} will add your bot into the server soon.')
          
      else:
        await message.reply('You already submitted a request for this bot.')

    else:
      await message.reply('You are granting your bot the wrong permissions. Kindly reconfigure and resubmit bot invitation link.')

  else:
    await message.reply('`$addbot [bot-invite-link]`')

async def on_member_join(bot, member):
  if member.bot:
    message_key = f'{member.id}-add-bot-message-id'
    owner_key = f'{member.id}-owner-id'

    try:
      message_id = int(u.get_value(message_key))
      owner_id = int(u.get_value(owner_key))
      channel_key = f'{owner_id}-channel-id'
      channel_id = int(u.get_value(channel_key))

    except Exception as e:
      print(f'ERROR: on_member_join({member.name}, {member.id}): {e}')

    else:
      c_dev_log = get_channel(bot, c.c_dev_log_id)
      message = await c_dev_log.fetch_message(message_id)

      await message.add_reaction(c.tick_emoji)

      channel = get_channel(bot, channel_id)

      await channel.set_permissions(member, view_channel = True)

    finally:
      r_student_bots = get_role(bot, c.r_student_bots_id)
      c_stu_chit_chat = get_channel(bot, c.c_stu_chit_chat_id)
      owner = get_member(bot, owner_id)

      await member.add_roles(r_student_bots)
      await c_stu_chit_chat.send(f'Welcome {owner.mention}\'s bot, {member.mention}!')

async def on_member_remove(bot, member):
  if member.bot:
    message_key = f'{member.id}-add-bot-message-id'
    owner_key = f'{member.id}-owner-id'

    try:
      u.del_value(message_key)
      u.del_value(owner_key)

    except Exception as e:
      print(f'ERROR: on_member_remove({member.name}, {member.id}): {e}')

  else:
    channel_key = f'{member.id}-channel-id'
    lvl_key = f'{member.id}-stats-level'
    xp_key = f'{member.id}-stats-xp'
    last_key = f'{member.id}-stats-last'

    try:
      u.del_value(channel_key)
      u.del_value(lvl_key)
      u.del_value(xp_key)
      u.del_value(last_key)

    except Exception as e:
      print(f'ERROR: on_member_remove({member.name}, {member.id}): {e}')

async def on_ok_coc(discord, bot, payload):
  member = get_member(bot, payload.user_id)
  emoji = str(payload.emoji)

  if member.id not in c.u_non_student_ids and payload.message_id == c.m_coc_id and len(member.roles) == 1 and payload.event_type == 'REACTION_ADD' and emoji == c.ok_emoji:
    u.put(0, f'{member.id}-stats-level')
    u.put(0, f'{member.id}-stats-xp')
    u.put(0, f'{member.id}-stats-last')

    r_students = get_role(bot, c.r_students_id)

    await member.add_roles(r_students)

    c_stu_chit_chat = get_channel(bot, c.c_stu_chit_chat_id)
    c_imp_alerts = get_channel(bot, c.c_imp_alerts_id)

    await c_stu_chit_chat.send(f'Welcome {member.mention}! Kindly check out {c_imp_alerts.mention}.')

    guild = bot.get_guild(c.guild_id)
    r_dev_bot = get_role(bot, c.r_dev_bot_id)
    r_bocals = get_role(bot, c.r_bocals_id)
    overwrites = {
      guild.default_role: discord.PermissionOverwrite(view_channel=False),
      r_dev_bot: discord.PermissionOverwrite(view_channel = True),
      r_bocals: discord.PermissionOverwrite(view_channel = True, manage_channels = False),
      member: discord.PermissionOverwrite(view_channel = True)
    }
    cat_bot = get_category(bot, c.cat_bot_id)
    channel = await cat_bot.create_text_channel(member.name, overwrites = overwrites, topic = f'Use this channel for your evaluations!')
    channel_key = f'{member.id}-channel-id'
    u.put(channel.id, channel_key)