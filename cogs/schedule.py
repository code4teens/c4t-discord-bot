from datetime import datetime, timedelta
import random
import sqlite3

from discord.ext import commands, tasks
import discord

import utils as utl


class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trigger_loop.start()

    async def assign_peers(self, guild, day):
        with sqlite3.connect(f'db/{guild.id}.sqlite') as con:
            cur = con.cursor()
            cur.execute('SELECT value FROM main WHERE key = "eval_code"')
            code, = [*map(int, cur.fetchone())]

        role_students = discord.utils.get(guild.roles, name='Students')
        students = role_students.members
        random.shuffle(students)

        for i, _ in enumerate(students):
            if len(students) == 1:
                break

            evaluator = students[i]

            if i == len(students) - 1:
                evaluatee = students[0]
            else:
                evaluatee = students[i + 1]

            with sqlite3.connect(f'db/{guild.id}.sqlite') as con:
                cur = con.cursor()
                cur.execute(
                    'SELECT chn_id, evaluator_id FROM students WHERE id = ?',
                    (evaluatee.id,)
                )
                chn_eval_id, prev_evaluator_id = cur.fetchone()

                if day != 9:
                    cur.execute(
                        'UPDATE students SET evaluator_id = ? WHERE id = ?',
                        (evaluator.id, evaluatee.id)
                    )
                    con.commit()

            chn_eval = discord.utils.get(guild.text_channels, id=chn_eval_id)

            if prev_evaluator_id is not None:
                # deny previous evaluator permission to view channel
                prev_evaluator = discord.utils.get(
                    guild.members,
                    id=prev_evaluator_id
                )
                await chn_eval.set_permissions(prev_evaluator, overwrite=None)

            if day != 9:
                # grant evaluator permission to view channel
                await chn_eval.set_permissions(
                    evaluator,
                    view_channel=True
                )

                # send message to channel informing discussion pairs
                code_str = str(code).zfill(4)
                await chn_eval.send(
                    f'Hi {evaluatee.mention}, your code tester for today is '
                    f'{evaluator.mention}, you may use this channel to '
                    'discuss the project. Your unique submission code for 4-6 '
                    f'pm later is `{code_str}`.'
                )

                # update database
                with sqlite3.connect(f'db/{guild.id}.sqlite') as con:
                    cur = con.cursor()
                    cur.execute(
                        'INSERT INTO evals '
                        '(day, date, eval_code, coder_id, tester_id) '
                        'VALUES '
                        '(?, ?, ?, ?, ?)',
                        (day, datetime.now(), code, evaluatee.id, evaluator.id)
                    )
                    con.commit()

                code += 1

        with sqlite3.connect(f'db/{guild.id}.sqlite') as con:
            cur = con.cursor()
            cur.execute(
                'UPDATE main SET value = ? WHERE key = ?',
                (code, 'eval_code')
            )
            con.commit()

    async def assign_groups(self, guild):
        def get_village_role(i):
            return discord.utils.get(guild.roles, name=f'Village {i}')

        role_students = discord.utils.get(guild.roles, name='Students')
        students = role_students.members
        random.shuffle(students)
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
        now = datetime.now()

        if now.minute == 0:  # trigger loop when min is 0
            print(f'{utl.green}{now}: Checking schedule...{utl.reset}')
            self.check_schedule.start()
            self.trigger_loop.cancel()

    @tasks.loop(seconds=3600)  # run hourly (every 3600 s)
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
        now = datetime.now()

        if now >= date and now < date + timedelta(days=9):
            delta = now - date
            day = delta.days + 1

            guild = self.bot.get_guild(guild_id)
            role_students = discord.utils.get(guild.roles, name='Students')
            chn_alerts = discord.utils.get(guild.text_channels, name='alerts')
            chn_townhall = discord.utils.get(
                guild.voice_channels,
                name='townhall'
            )

            # day 1 @ 8:00 am
            if now.hour == 8:
                if day == 1:
                    await chn_alerts.send(
                        f'Good Morning {role_students.mention}, this is a '
                        'reminder for our Townhall at 9:00 am. See you at '
                        f'{chn_townhall.mention}!'
                    )
            # day 2, 3, 4, 5, 6, 7, 8 & 9 @ 9:00 am
            elif now.hour == 9:
                if day != 1 and day != 9:  # on days 2 - 8
                    await chn_alerts.send(
                        f'Good Morning {role_students.mention}, this is your '
                        f'Day-0{day} assignment. All the best!\n'
                        '\n'
                        f'{utl.projects[day - 1]}'
                    )
                elif day == 9:  # on day 9
                    await chn_alerts.send(
                        f'Good Morning {role_students.mention}, all the best '
                        'on your final day!'
                    )

                if day == 4:  # also on day 4
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
                        f'Good Morning {role_students.mention}, this is your '
                        f'Day-0{day} assignment. All the best!\n'
                        '\n'
                        f'{utl.projects[day - 1]}'
                    )
            # everyday @ 11:00 pm
            elif now.hour == 11:
                await self.assign_peers(guild, day)
            # days 1, 2, 3, 4, 5, 6, 7 & 8 @ 4:00 pm
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
                    await chn_alerts.send(
                        f'Good Evening {role_students.mention}, this is a '
                        'reminder for our Townhall at 6:00 pm. See you at '
                        f'{chn_townhall.mention}!'
                    )

    @trigger_loop.before_loop
    async def before_loop_trigger(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Schedule(bot))
