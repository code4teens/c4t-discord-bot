import constants as c
import utilities as u

async def check_to_send(discord, bot, send_pdf_time_str):
  while True:
    now_date_str, now_time_str = u.get_now()

    if now_time_str == send_pdf_time_str:
      for x in range(1, 10):
        key = f'day{x}'
        
        if u.get_value(key) == now_date_str:
          path = f'resources/{key}.txt'
          channel = bot.get_channel(c.c_dev_terminal_id)

          await channel.send(file = discord.File(path))

    await u.asyncio_sleep(60)

async def send_projects(discord, bot, day1_str):
  day1 = u.get_date_time_from_str(day1_str, '%Y-%m-%d %H:%M')
  send_pdf_time_str = u.get_str_from_date_time(day1, '%H:%M')

  for x in range(0, 9):
    date = day1 + u.get_delta_day(x)
    date_str = u.get_str_from_date_time(date, '%Y-%m-%d')
    u.put(date_str, f'day{x + 1}')
  
  loop = u.asyncio_get_event_loop()
  loop.call_later(0, await check_to_send(discord, bot, send_pdf_time_str))

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