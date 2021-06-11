import random
import re
import time

import asyncio

import constants as c
import utilities as u

def get_chunks(users, n):
  for i in range(0, len(users), n):
    yield users[i:i + n]

def get_user(bot, usr_id):
  gld = bot.get_guild(c.gld_id)

  return gld.get_member(usr_id)

def get_role(bot, rol_id):
  gld = bot.get_guild(c.gld_id)

  for role in gld.roles:
    if role.id == rol_id:
      return role

def get_category(bot, cat_id):
  gld = bot.get_guild(c.gld_id)

  for category in gld.categories:
    if category.id == cat_id:
      return category

def get_channel(bot, chn_id):
  return bot.get_channel(chn_id)

async def give_students_xp(bot, message):
  author = message.author
  rol_students = get_role(bot, c.rol_students_id)

  if rol_students in author.roles:
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
  rol_students = get_role(bot, c.rol_students_id)
  students = rol_students.members
  random.shuffle(students)
  strs = [(
    f'{rol_students.mention}, below are your evaluation pairs for today:\n\n'
    '`CODE: TESTER   <   >   CODER`'
  )]
  key = 'code'
  code = int(u.get_value(key))

  if len(students) > 1:
    for i in range(len(students)):
      if i == len(students) - 1:
        evaluatee = students[0]

      else:
        evaluatee = students[i + 1]

      chn_eval_key = f'{evaluatee.id}-channel-id'

      try:
        chn_eval_id = u.get_value(chn_eval_key)

      except Exception as e:
        print(f'ERROR: assign_peers(): {e}')

      else:
        chn_eval = get_channel(bot, chn_eval_id)

        await chn_eval.set_permissions(students[i], view_channel = True)

        evaluator_key = f'{evaluatee.id}-evaluator'

        try:
          prev_evaluator_id = int(u.get_value(evaluator_key))

        except Exception as e:
          print(f'ERROR: assign_peers(): {e}')

        else:
          prev_evaluator = get_user(bot, prev_evaluator_id)

          await chn_eval.set_permissions(prev_evaluator, overwrite = None)

        u.put(students[i].id, evaluator_key)
        code_str = str(code).zfill(4)
        strs.append(f'{code_str} : {students[i].name}   <   >   {evaluatee.name}')
        code += 1

  elif len(students) == 1:
    chn_eval_key = f'{students[0].id}-channel-id'
    evaluator_key = f'{students[0].id}-evaluator'

    try:
      chn_eval_id = u.get_value(chn_eval_key)
      prev_evaluator_id = int(u.get_value(evaluator_key))
      u.del_value(evaluator_key)

    except Exception as e:
      print(f'ERROR: assign_peers(): {e}')

    else:
      chn_eval = get_channel(bot, chn_eval_id)
      prev_evaluator = get_user(bot, prev_evaluator_id)

      await chn_eval.set_permissions(prev_evaluator, overwrite = None)

    code_str = str(code).zfill(4)
    strs.append(f'{code_str} : {students[0].name}   <   >   {students[0].name}')
    code += 1

  u.put(code, key)

  chn_alerts = get_channel(bot, c.chn_alerts_id)
  await chn_alerts.send('\n'.join(strs))

async def assign_villages(bot):
  rol_villages = [get_role(bot, rol_village_id) for rol_village_id in c.rol_village_ids]
  rol_students = get_role(bot, c.rol_students_id)
  students = rol_students.members
  random.shuffle(students)
  chunks = get_chunks(students, 5)

  for chunk in chunks:
    for i, student in enumerate(chunk):
      await student.add_roles(rol_villages[i])

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
          chn_alerts = get_channel(bot, c.chn_alerts_id)
          chn_terminal = get_channel(bot, c.chn_terminal_id)

          if type == u.Alert.MESSAGE:
            await chn_alerts.send(message)

          elif type == u.Alert.FILE:
            await chn_alerts.send(message, file = discord.File(payload))

          elif type == u.Alert.COROUTINE:
            await payload(bot)

          elif type == u.Alert.TEST_FILE:
            await chn_terminal.send(message, file = discord.File(payload))

    await asyncio.sleep(60)

def channel_check(bot, message):
  roles = message.author.roles
  rol_devs = get_role(bot, c.rol_devs_id)
  rol_bocals = get_role(bot, c.rol_bocals_id)
  rol_students = get_role(bot, c.rol_students_id)
  chn_terminal = get_channel(bot, c.chn_terminal_id)
  chn_clockwork = get_channel(bot, c.chn_clockwork_id)

  if rol_devs in roles and message.channel != chn_terminal and message.channel != chn_clockwork:
    raise u.ChannelException(f'Kindly utilise me at {chn_terminal.mention} or {chn_clockwork.mention}.')

  elif rol_bocals in roles and message.channel != chn_terminal and message.channel != chn_clockwork:
    raise u.ChannelException(f'Kindly utilise me at {chn_terminal.mention} or {chn_clockwork.mention}.')

  elif rol_students in roles and message.channel != chn_clockwork:
    raise u.ChannelException(f'Kindly utilise me at {chn_clockwork.mention}.')

def command_check(bot, message):
  command = message.content.split()[0]
  roles = message.author.roles
  rol_devs = get_role(bot, c.rol_devs_id)

  if rol_devs not in roles and command in c.dev_commands:
    raise u.CommandException(f'You are not authorised to use `{command}`!')

async def devattach_command(message):
  match = re.search(c.rgx_devattach, message.content)

  if match:
    chn = message.channel_mentions[0]
    message_data = message.content.split(' ', 2)
    description = message_data[2]

    if message.attachments:
      file = await message.attachments[0].to_file()

      try:
        await chn.send(description, file = file)

      except Exception as e:
        print(f'ERROR: $devattach: {e}')

        await message.reply(f'I do not have write permissions in {chn.mention}.')

    else:
      await message.reply('You forgot to include the attachment.')

  else:
    await message.reply('`$devattach [#channel] [description]`')

async def devecho_command(message):
  match = re.search(c.rgx_devecho, message.content)
      
  if match:
    chn = message.channel_mentions[0]
    message_data = message.content.split(' ', 2)
    text = message_data[2]

    try:
      await chn.send(text)

    except Exception as e:
      print(f'ERROR: $devecho: {e}')

      await message.reply(f'I do not have write permissions in {chn.mention}.')
        
  else:
    await message.reply('`$devecho [#channel] [message]`')

async def add_bot_command(bot, message):
  match = re.search(c.rgx_addbot, message.content)

  if match:
    link = message.content.split()[1]
    bot_id = match.group(1)
    message_key = f'{bot_id}-add-bot-message-id'
    owner_key = f'{bot_id}-owner-id'
    prm_int = int(match.group(2))

    if prm_int == c.prm_add_student_bot_int:
      if message_key not in u.keys():
        rol_devs = get_role(bot, c.rol_devs_id)
        chn_log = get_channel(bot, c.chn_log_id)
        log_message = await chn_log.send(f'{rol_devs.mention} Kindly add this bot as soon as possible.\n{link}')
        u.put(log_message.id, message_key)
        u.put(message.author.id, owner_key)

        await message.reply(f'The {rol_devs.mention} will add your bot into the server soon.')
          
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
      chn_eval_key = f'{owner_id}-channel-id'
      chn_eval_id = int(u.get_value(chn_eval_key))

    except Exception as e:
      print(f'ERROR: on_member_join({member.name}, {member.id}): {e}')

    else:
      chn_log = get_channel(bot, c.chn_log_id)
      message = await chn_log.fetch_message(message_id)

      await message.add_reaction(c.emoji_tick)

      rol_student_bots = get_role(bot, c.rol_student_bots_id)

      await member.add_roles(rol_student_bots)

      chn_chit_chat = get_channel(bot, c.chn_chit_chat_id)
      owner = get_user(bot, owner_id)

      await chn_chit_chat.send(f'Welcome {owner.mention}\'s bot, {member.mention}!')

      chn_eval = get_channel(bot, chn_eval_id)

      await chn_eval.set_permissions(member, view_channel = True)

async def on_member_remove(member):
  if member.bot:
    message_key = f'{member.id}-add-bot-message-id'
    owner_key = f'{member.id}-owner-id'

    try:
      u.del_value(message_key)
      u.del_value(owner_key)

    except Exception as e:
      print(f'ERROR: on_member_remove({member.name}, {member.id}): {e}')

  else:
    chn_eval_key = f'{member.id}-channel-id'
    evaluator_key = f'{member.id}-evaluator'
    lvl_key = f'{member.id}-stats-level'
    xp_key = f'{member.id}-stats-xp'
    last_key = f'{member.id}-stats-last'

    try:
      u.del_value(chn_eval_key)
      u.del_value(evaluator_key)
      u.del_value(lvl_key)
      u.del_value(xp_key)
      u.del_value(last_key)

    except Exception as e:
      print(f'ERROR: on_member_remove({member.name}, {member.id}): {e}')

async def on_ok_coc(discord, bot, payload):
  member = get_user(bot, payload.user_id)
  emoji = str(payload.emoji)

  if member.id not in c.usr_non_student_ids and payload.message_id == c.msg_coc and len(member.roles) == 1 and payload.event_type == 'REACTION_ADD' and emoji == c.emoji_ok:
    u.put(0, f'{member.id}-stats-level')
    u.put(0, f'{member.id}-stats-xp')
    u.put(0, f'{member.id}-stats-last')

    rol_students = get_role(bot, c.rol_students_id)

    await member.add_roles(rol_students)

    chn_chit_chat = get_channel(bot, c.chn_chit_chat_id)
    chn_alerts = get_channel(bot, c.chn_alerts_id)

    await chn_chit_chat.send(f'Welcome {member.mention}! Kindly check out {chn_alerts.mention}.')

    gld = bot.get_guild(c.gld_id)
    rol_dev_bot = get_role(bot, c.rol_dev_bot_id)
    rol_bocals = get_role(bot, c.rol_bocals_id)
    rol_observer = get_role(bot, c.rol_observer_id)
    overwrites = {
      gld.default_role: discord.PermissionOverwrite(view_channel=False),
      rol_dev_bot: discord.PermissionOverwrite(view_channel = True),
      rol_bocals: discord.PermissionOverwrite(view_channel = True),
      rol_observer: discord.PermissionOverwrite(view_channel = True),
      member: discord.PermissionOverwrite(view_channel = True)
    }
    cat_bot = get_category(bot, c.cat_bot_id)
    chn_eval = await cat_bot.create_text_channel(member.name, overwrites = overwrites, topic = f'Use this channel for your evaluations!')
    chn_eval_key = f'{member.id}-channel-id'
    u.put(chn_eval.id, chn_eval_key)

async def override_assign_peers(bot):
  ids = [] # update when necessary
  random.shuffle(ids)
  students = [get_user(bot, id) for id in ids]

  strs = ['`CODE: TESTER   <   >   CODER`']
  
  key = 'code'
  code = int(u.get_value(key))
  
  for i in range(len(students)):
    if i == len(students) - 1:
      evaluatee = students[0]

    else:
      evaluatee = students[i + 1]

    chn_eval_key = f'{evaluatee.id}-channel-id'

    try:
      chn_eval_id = u.get_value(chn_eval_key)

    except Exception as e:
      print(f'ERROR: override_assign_peers(): {e}')

    else:
      chn_eval = get_channel(bot, chn_eval_id)

      await chn_eval.set_permissions(students[i], view_channel = True)

      evaluator_key = f'{evaluatee.id}-evaluator'

      try:
        prev_evaluator_id = int(u.get_value(evaluator_key))

      except Exception as e:
        print(f'ERROR: override_assign_peers(): {e}')

      else:
        prev_evaluator = get_user(bot, prev_evaluator_id)

        await chn_eval.set_permissions(prev_evaluator, overwrite = None)

      u.put(students[i].id, evaluator_key)
      code_str = str(code).zfill(4)
      strs.append(f'{code_str} : {students[i].name}   <   >   {evaluatee.name}')
      code += 1

  u.put(code, key)

  chn_alerts = get_channel(bot, c.chn_alerts_id)
  await chn_alerts.send('\n'.join(strs))

async def override_on_ok_coc(discord, bot):
  gld = bot.get_guild(c.gld_id)
  rol_dev_bot = get_role(bot, c.rol_dev_bot_id)
  rol_bocals = get_role(bot, c.rol_bocals_id)
  rol_observer = get_role(bot, c.rol_observer_id)
  cat_bot = get_category(bot, c.cat_bot_id)

  ids = [] # update when necessary
  for id in ids:
    member = get_user(bot, id)
    u.put(0, f'{member.id}-stats-level')
    u.put(0, f'{member.id}-stats-xp')
    u.put(0, f'{member.id}-stats-last')

    overwrites = {
      gld.default_role: discord.PermissionOverwrite(view_channel = False),
      rol_dev_bot: discord.PermissionOverwrite(view_channel = True),
      rol_bocals: discord.PermissionOverwrite(view_channel = True),
      rol_observer: discord.PermissionOverwrite(view_channel = True),
      member: discord.PermissionOverwrite(view_channel = True)
    }
    chn_eval = await cat_bot.create_text_channel(member.name, overwrites = overwrites, topic = f'Use this channel for your evaluations!')
    chn_eval_key = f'{member.id}-channel-id'
    u.put(chn_eval.id, chn_eval_key)