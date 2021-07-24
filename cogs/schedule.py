from datetime import datetime, timedelta
import random
import sqlite3

from discord.ext import commands, tasks
import discord
import pytz

import utils as utl


class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timezone = pytz.timezone('Asia/Kuala_Lumpur')
        self.trigger_loop.start()

    async def assign_peers(self, guild, day):
        with sqlite3.connect(f'db/{guild.id}.sqlite') as con:
            cur = con.cursor()
            cur.execute('SELECT COUNT(*) FROM evals')
            disc_id, = cur.fetchone()

        role_students = discord.utils.get(guild.roles, name='Students')
        students = role_students.members
        random.shuffle(students)

        for i, _ in enumerate(students):
            tester = students[i]
            coder = students[0] if i == len(students) - 1 else students[i + 1]

            with sqlite3.connect(f'db/{guild.id}.sqlite') as con:
                cur = con.cursor()
                cur.execute(
                    'SELECT chn_id FROM students WHERE id = ?', (coder.id,)
                )
                chn_eval_id, = cur.fetchone()
                cur.execute(
                    'SELECT tester_id from evals '
                    'WHERE coder_id = ? AND day = ?',
                    (coder.id, day - 1)
                )
                rec = cur.fetchone()

            chn_eval = discord.utils.get(guild.text_channels, id=chn_eval_id)

            if rec is not None:
                # deny previous tester permission to view coder channel
                prev_tester_id, = rec
                prev_tester = discord.utils.get(
                    guild.members,
                    id=prev_tester_id
                )
                await chn_eval.set_permissions(prev_tester, overwrite=None)

            if day != 9:
                # grant new tester permission to view coder channel
                await chn_eval.set_permissions(tester, view_channel=True)

                # send message to coder channel informing discussion pairs
                disc_id += 1
                disc_id_str = str(disc_id).zfill(4)
                await chn_eval.send(
                    f'Hi {coder.mention}, your tester for today is '
                    f'{tester.mention}, the two of you may use this channel '
                    'to discuss. Your unique discussion ID for 4-6 pm later '
                    f'is `{disc_id_str}`.'
                )

                now = datetime.now(self.timezone)

                # update database
                with sqlite3.connect(f'db/{guild.id}.sqlite') as con:
                    cur = con.cursor()
                    cur.execute(
                        'INSERT INTO evals '
                        '(id, day, date, coder_id, tester_id) '
                        'VALUES '
                        '(?, ?, ?, ?, ?)',
                        (disc_id, day, now, coder.id, tester.id)
                    )
                    con.commit()

    async def assign_groups(self, guild):
        def get_student(id):
            return discord.utils.get(guild.members, id=id)

        def get_village_role(i):
            return discord.utils.get(guild.roles, name=f'Village {i}')

        with sqlite3.connect(f'db/{guild.id}.sqlite') as con:
            cur = con.cursor()
            cur.execute(
                "SELECT id FROM students WHERE nickname NOT LIKE '(MIA)%' "
                'ORDER BY lvl DESC, xp DESC'
            )
            recs = cur.fetchall()

        ids = [id for rec in recs for id in rec]
        students = [student for student in map(get_student, ids)]
        roles_villages = [
            x for x in map(get_village_role, range(1, 11)) if x is not None
        ]
        n = len(roles_villages)
        chunks = (students[i:i + n] for i in range(0, len(students), n))

        for chunk in chunks:
            for i, student in enumerate(chunk):
                await student.add_roles(roles_villages[i])

    @tasks.loop(seconds=1)
    async def trigger_loop(self):
        now = datetime.now(self.timezone)

        if now.minute == 0:
            print(f'{utl.green}{now}: Checking schedule...{utl.reset}')
            self.check_schedule.start()
            self.trigger_loop.cancel()

    @tasks.loop(seconds=3600)
    async def check_schedule(self):
        with sqlite3.connect('db/main.sqlite') as con:
            cur = con.cursor()
            cur.execute('SELECT value FROM main WHERE key = "active_guild_id"')
            rec = cur.fetchone()

        if rec is None:
            return

        guild_id, = [*map(int, rec)]

        with sqlite3.connect(f'db/{guild_id}.sqlite') as con:
            cur = con.cursor()
            cur.execute('SELECT value FROM main WHERE key = "start_date"')
            date_str, = cur.fetchone()

        date = datetime.strptime(date_str[:10], '%Y-%m-%d')
        date = date.astimezone(self.timezone)
        date = date.replace(hour=0)
        now = datetime.now(self.timezone)

        if now >= date and now < date + timedelta(days=9):
            delta = now - date
            day = delta.days + 1

            guild = self.bot.get_guild(guild_id)
            chn_server_log = discord.utils.get(
                guild.text_channels,
                name='server-log'
            )
            chn_alerts = discord.utils.get(guild.text_channels, name='alerts')
            chn_townhall = discord.utils.get(
                guild.voice_channels,
                name='townhall'
            )
            chn_chit_chat = discord.utils.get(
                guild.text_channels,
                name='chit-chat'
            )
            role_students = discord.utils.get(guild.roles, name='Students')

            # everyday @ 7:00 am
            if now.hour == 7:
                await chn_server_log.send(
                    f'This is a scheduled test message for Day {day}.'
                )
            # day 1 @ 8:00 am
            elif now.hour == 8:
                if day == 1:
                    await chn_chit_chat.send(
                        f'Good Morning {role_students.mention}, this is a '
                        'reminder for our Townhall at 9:00 am. See you at '
                        f'{chn_townhall.mention}!'
                    )
            # days 2 - 8 @ 9:00 am
            elif now.hour == 9:
                # on days 2 - 8
                if day != 1 and day != 9:
                    await chn_alerts.send(
                        f'Good Morning {role_students.mention}, this is your '
                        f'Day-0{day} assignment. All the best!\n'
                        '\n'
                        f'{utl.projects[day - 1]}'
                    )
                # on day 9
                elif day == 9:
                    await chn_chit_chat.send(
                        f'Good Morning {role_students.mention}, all the best '
                        'on your final day!'
                    )

                # also on day 4
                if day == 4:
                    await self.assign_groups(guild)
                    await chn_alerts.send(
                        'You are also put into groups for your Day-09 group '
                        'assignment. Good luck!\n'
                        '\n'
                        f'{utl.projects[-1]}'
                    )
            # day 1 @ 10:00 am
            elif now.hour == 10:
                if day == 1:
                    await chn_alerts.send(
                        f'Hi {role_students.mention}, this is your Day-0{day} '
                        'assignment. All the best!\n'
                        '\n'
                        f'{utl.projects[day - 1]}'
                    )
            # everyday @ 11:00 pm
            elif now.hour == 11:
                await self.assign_peers(guild, day)
            # days 1 - 8 @ 4:00 pm
            elif now.hour == 16:
                if day != 9:
                    form = utl.forms[day - 1]
                    await chn_alerts.send(
                        f'Good Evening {role_students.mention}, this is a '
                        'reminder to discuss your projects with your pairs. '
                        'You are required to submit below form before 6:00 '
                        'pm.\n'
                        '\n'
                        f'{form}'
                    )
            # days 1, 2, 4 & 9 @ 5:00 pm
            elif now.hour == 17:
                if day == 1 or day == 2 or day == 4 or day == 9:
                    await chn_chit_chat.send(
                        f'Hi {role_students.mention}, this is a reminder for '
                        'our Townhall at 6:00 pm. See you at '
                        f'{chn_townhall.mention}!'
                    )

    @trigger_loop.before_loop
    async def before_trigger_loop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Schedule(bot))
