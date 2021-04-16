import constants as c
import utilities as u

async def check_to_send(discord, bot, send_pdf_time_str):
  while True:
    now_date_str, now_time_str = u.get_now()

    if now_time_str == send_pdf_time_str:
      for x in range(1, 10):
        key = f'day{x}'
        
        if u.get_value(key) == now_date_str:
          path = f'resources/{key}.pdf'
          channel = bot.get_channel(c.c_imp_alerts_id)

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