import constants as c
import utilities as u

def get_role_members(bot, role_id):
  guild = bot.get_guild(c.guild_id)

  for role in guild.roles:
    if role.id == role_id:
      return role.members

def get_student_chunks(bot, n):
  members = u.random_shuffle(get_role_members(bot, c.r_students_id))

  for i in range(0, len(members), n):
    yield members[i:i + n]

def assign_peers(bot):
  students = get_role_members(bot, c.r_students_id)
  members = u.random_shuffle(students)
  i = 0
  #strs = [f'{role.mention}, below are the evaluation groups for today:']
  strs = [(
    f'{role.mention}, below are your evaluation pairs for today:\n\n'
    '`CODE: EVALUATOR   <   >   EVALUATEE`'
  )]

  key = 'code'
  code = int(u.get_value(key)) + 1

  while i < len(members):
    code_str = str(code).zfill(4)

    if i == len(members) - 1:
      strs.append(f'{code_str} : {members[i].name}   <   >   {members[0].name}')
      break

    strs.append(f'{code_str} : {members[i].name}   <   >   {members[i + 1].name}')

    i += 1
    code += 1

  u.put(code, key)

  return '\n'.join(strs)

async def assign_villages(bot):
  guild = bot.get_guild(c.guild_id)
  roles = [guild.get_role(village_id) for village_id in c.r_village_ids]
  chunks = get_student_chunks(bot, 5)

  for members in chunks:
    for index, member in enumerate(members):
      await member.add_roles(roles[index])

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

def channel_check(bot, message):
  dev_terminal_channel = bot.get_channel(c.c_dev_terminal_id)
  stu_ttb_channel = bot.get_channel(c.c_stu_ttb_id)
  roles = message.author.roles

  if c.r_devs_id in [role.id for role in roles] \
  and message.channel.id != c.c_dev_terminal_id \
  and message.channel.id != c.c_stu_ttb_id:
    raise u.ChannelException(f'Kindly utilise me at {dev_terminal_channel.mention} or {stu_ttb_channel.mention}.')

  elif c.r_students_id in [role.id for role in roles] \
  and message.channel.id != c.c_stu_ttb_id:
    raise u.ChannelException(f'Kindly utilise me at {stu_ttb_channel.mention}.')

def command_check(message):
  if c.r_devs_id not in [role.id for role in message.author.roles] \
  and (command := message.content.split()[0]) in c.dev_commands:
    raise u.CommandException(f'You are not authorised to use `{command}`!')

async def check_schedule(discord, bot):
  while True:
    now_date_str, now_time_str = u.get_now()

    if now_date_str in c.schedule.keys():
      tasks = c.schedule[now_date_str]

      for task in tasks:
        time = task['time']
        type = task['type']
        payload = task['payload']
        message = task['message']

        if time == now_time_str:
          channel = bot.get_channel(c.c_imp_alerts_id)

          if type == u.Alert.MESSAGE:
            await channel.send(message)

          elif type == u.Alert.FILE:
            await channel.send(message, file = discord.File(payload))

          elif type == u.Alert.FUNCTION:
            await channel.send(payload(bot))

          elif type == u.Alert.COROUTINE:
            await payload(bot)

    await u.asyncio_sleep(60)

async def on_member_join(bot, member):
  if member.bot:
    key = f'{member.id}-add-bot'

    try:
      message_id = int(u.get_value(key))

    except Exception as e:
      print(f'ERROR: on_member_join({member.name}, {member.id}): {e}')

    else:
      log_channel = bot.get_channel(c.c_dev_log_id)
      message = await log_channel.fetch_message(message_id)

      await message.add_reaction(c.tick_emoji)

    finally:
      role = member.guild.get_role(c.r_student_bots_id)
      welcome_channel = bot.get_channel(c.c_imp_introduction_id)
      prefix = u.get_random_prefix()

      await member.add_roles(role)
      await welcome_channel.send(f'Welcome {member.mention}! Your command prefix is `{prefix}`.')

async def on_member_remove(member):
  if member.bot:
    key = f'{member.id}-add-bot'
    #remove adopt key-value pair

    try:
      u.del_value(key)

    except Exception as e:
      print(f'ERROR: on_member_remove({member.name}, {member.id}): {e}')

  else:
    lvl_key = f'{member.id}-stats-level'
    xp_key = f'{member.id}-stats-xp'
    last_key = f'{member.id}-stats-last'
    adopt_key = f'{member.id}-adopt'

    try:
      u.del_value(lvl_key)
      u.del_value(xp_key)
      u.del_value(last_key)
      u.del_value(adopt_key)

    except Exception as e:
      print(f'ERROR: on_member_remove({member.name}, {member.id}): {e}')

async def on_ok_coc(bot, payload):
  guild = bot.get_guild(payload.guild_id)
  member = guild.get_member(payload.user_id)
  event_type = payload.event_type
  emoji = str(payload.emoji)

  if payload.message_id == c.m_coc_id and len(member.roles) == 1 and event_type == 'REACTION_ADD' and emoji == c.ok_emoji:
    u.put(0, f'{member.id}-stats-level')
    u.put(0, f'{member.id}-stats-xp')
    u.put(0, f'{member.id}-stats-last')

    role = guild.get_role(c.r_students_id)
    reason = f'{member} agreed to Code of Conduct.'
    welcome_channel = bot.get_channel(c.c_imp_introduction_id)
    alerts_channel = bot.get_channel(c.c_imp_alerts_id)

    await member.add_roles(role, reason = reason)
    await welcome_channel.send(f'Welcome {member.mention}! Kindly check out {alerts_channel.mention}.')