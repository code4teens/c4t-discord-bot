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

def get_channel(bot, channel_id):
  return bot.get_channel(channel_id)

def assign_peers(bot):
  r_students = get_role(bot, c.r_students_id)
  students = r_students.members
  random.shuffle(students)
  key = 'code'
  code = int(u.get_value(key)) + 1
  strs = [(
    f'TEST:\n{r_students.mention}, below are your evaluation pairs for today:\n\n'
    '`CODE: EVALUATOR   <   >   EVALUATEE`'
  )]

  if len(students) > 1:
    for i in range(len(students)):
      code_str = str(code).zfill(4)

      if i == len(students) - 1:
        strs.append(f'{code_str} : {students[i].name}   <   >   {students[0].name}')

        break

      strs.append(f'{code_str} : {students[i].name}   <   >   {students[i + 1].name}')
      code += 1

  elif len(students) == 1:
    code_str = str(code).zfill(4)
    strs.append(f'{code_str} : {students[0].name}   <   >   {students[0].name}')

  u.put(code, key)

  return '\n'.join(strs)

async def assign_villages(bot):
  r_villages = [get_role(bot, r_village_id) for r_village_id in c.r_village_ids]
  r_students = get_role(bot, c.r_students_id)
  students = r_students.members
  random.shuffle(students)
  chunks = get_chunks(students, 5)

  for chunk in chunks:
    for i, student in enumerate(chunk):
      await student.add_roles(r_villages[i])

async def give_students_xp(bot, message):
  author = message.author
  r_students = get_role(bot, c.r_students_id)

  if r_students in author.roles:
    lvl_key = f'{author.id}-stats-level'
    xp_key = f'{author.id}-stats-xp'
    l_key = f'{author.id}-stats-last'
    level = u.get_value(lvl_key)
    xp = u.get_value(xp_key)
    last = u.get_value(l_key)
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
      u.put(now, l_key)

def channel_check(bot, message):
  roles = message.author.roles
  r_devs = get_role(bot, c.r_devs_id)
  r_students = get_role(bot, c.r_students_id)
  c_dev_terminal = get_channel(bot, c.c_dev_terminal_id)
  c_stu_ttb = get_channel(bot, c.c_stu_ttb_id)

  if r_devs in roles and message.channel != c_dev_terminal and message.channel != c_stu_ttb:
    raise u.ChannelException(f'Kindly utilise me at {c_dev_terminal.mention} or {c_stu_ttb.mention}.')

  elif r_students in roles and message.channel != c_stu_ttb:
    raise u.ChannelException(f'Kindly utilise me at {c_stu_ttb.mention}.')

def command_check(bot, message):
  command = message.content.split()[0]
  roles = message.author.roles
  r_devs = get_role(bot, c.r_devs_id)

  if r_devs not in roles and command in c.dev_commands:
    raise u.CommandException(f'You are not authorised to use `{command}`!')

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
          channel = get_channel(bot, c.c_imp_alerts_id)

          if type == u.Alert.MESSAGE:
            await channel.send(message)

          elif type == u.Alert.FILE:
            await channel.send(message, file = discord.File(payload))

          elif type == u.Alert.FUNCTION:
            await channel.send(payload(bot))

          elif type == u.Alert.COROUTINE:
            await payload(bot)
            await channel.send(message)

    await asyncio.sleep(60)

async def on_member_join(bot, member):
  if member.bot:
    key = f'{member.id}-add-bot'

    try:
      message_id = int(u.get_value(key))

    except Exception as e:
      print(f'ERROR: on_member_join({member.name}, {member.id}): {e}')

    else:
      c_dev_log = get_channel(bot, c.c_dev_log_id)
      message = await c_dev_log.fetch_message(message_id)

      await message.add_reaction(c.tick_emoji)

    finally:
      r_student_bots = get_role(bot, c.r_student_bots_id)
      c_imp_introduction = get_channel(bot, c.c_imp_introduction_id)
      prefix = u.get_random_prefix()

      await member.add_roles(r_student_bots)
      await c_imp_introduction.send(f'Welcome {member.mention}! Your command prefix is `{prefix}`.')

async def on_member_remove(bot, member):
  if member.bot:
    a_key = f'{member.id}-add-bot'

    for key in u.keys():
        match = re.search(c.adopt_key_regex, key)

        if match:
          if int(u.get_value(key)) == member.id:
            u.del_value(key)

    try:
      u.del_value(a_key)

    except Exception as e:
      print(f'ERROR: on_member_remove({member.name}, {member.id}): {e}')

  else:
    lvl_key = f'{member.id}-stats-level'
    xp_key = f'{member.id}-stats-xp'
    l_key = f'{member.id}-stats-last'
    a_key = f'{member.id}-adopt'

    try:
      bot_id = u.get_value(a_key)
      u.del_value(lvl_key)
      u.del_value(xp_key)
      u.del_value(l_key)
      u.del_value(a_key)

    except Exception as e:
      print(f'ERROR: on_member_remove({member.name}, {member.id}): {e}')
    
    else:
      adopted_bot = get_member(bot, bot_id)
      r_villages = [get_role(bot, r_village_id) for r_village_id in c.r_village_ids]

      for role in adopted_bot.roles:
        if role in r_villages:
          reason = f'{member.name} left server.'

          await adopted_bot.remove_roles(role, reason = reason)

async def on_ok_coc(bot, payload):
  member = get_member(bot, payload.user_id)
  event_type = payload.event_type
  emoji = str(payload.emoji)

  if payload.message_id == c.m_coc_id and len(member.roles) == 1 and event_type == 'REACTION_ADD' and emoji == c.ok_emoji:
    u.put(0, f'{member.id}-stats-level')
    u.put(0, f'{member.id}-stats-xp')
    u.put(0, f'{member.id}-stats-last')

    r_students = get_role(bot, c.r_students_id)
    reason = f'{member.name} agreed to Code of Conduct.'
    c_imp_introduction = get_channel(bot, c.c_imp_introduction_id)
    c_imp_alerts = get_channel(bot, c.c_imp_alerts_id)

    await member.add_roles(r_students, reason = reason)
    await c_imp_introduction.send(f'Welcome {member.mention}! Kindly check out {c_imp_alerts.mention}.')