from datetime import datetime, timedelta
import random

from discord.ext import commands, tasks
from discord.utils import get
import discord

from utils import API_URL, get_active_cohort, green, now, reset, s, tz
import requests
import utils


class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trigger_loop.start()

    async def assign_peers(self, guild, cohort_data, day, date):
        # get & shuffle students
        role_students = get(guild.roles, name='Students')
        students = role_students.members
        random.shuffle(students)

        for i, _ in enumerate(students):
            # assign evaluator & evaluatee
            evaluator = students[i]
            evaluatee = students[i + 1] \
                if i != len(students) - 1 else students[0]

            # get evaluatee data
            user_url = f'{API_URL}/users/{evaluatee.id}'
            user_r = s.get(user_url, timeout=10)
            user_data = user_r.json()
            chn_eval_id = next(
                channel['id'] for channel in user_data['channels']
                if channel['cohort']['id'] == cohort_data['id']
            )
            chn_eval = get(guild.text_channels, id=chn_eval_id)

            # # deny other students permission to view evaluatee channel
            # for user in chn_eval.members:
            #     if user in students and user.id != evaluatee.id:
            #         await chn_eval.set_permissions(user, overwrite=None)

            if day != cohort_data['duration']:
                # update eval table
                eval_url = f'{API_URL}/evals'
                post_eval_data = {
                    'evaluator_id': evaluator.id,
                    'evaluatee_id': evaluatee.id,
                    'cohort_id': utils.active_cohort['id'],
                    'date': date
                }
                eval_r = s.post(eval_url, json=post_eval_data, timeout=10)

                if eval_r.status_code != requests.codes.created:
                    eval_r.raise_for_status()

                # grant new tester permission to view evaluatee channel
                await chn_eval.set_permissions(evaluator, view_channel=True)

                # send message to evaluatee channel informing evaluation pairs
                eval_data = eval_r.json()
                eval_id = str(eval_data['id']).zfill(4)
                message = (
                    f'Hi {evaluatee.mention}, your reviewer for today is '
                    f'{evaluator.mention}, the two of you may use this '
                    'channel to communicate.'
                )

                await chn_eval.send(message)

    async def assign_groups(self, guild, cohort_data):
        async def create_village_channels(cohort_data, role_village, i):
            role_dev_bot = get(guild.roles, name='Pyrate Bot')
            role_bocals = get(guild.roles, name='BOCALs')
            role_observers = get(guild.roles, name='Observers')
            overwrites = {
                role_dev_bot: discord.PermissionOverwrite(read_messages=True),
                role_bocals: discord.PermissionOverwrite(read_messages=True),
                role_observers:
                    discord.PermissionOverwrite(read_messages=True),
                role_village: discord.PermissionOverwrite(read_messages=True),
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=False
                )
            }
            topic = 'Test your village bot here!'
            ctg_cohort = get(guild.categories, name=cohort_data['nickname'])

            await ctg_cohort.create_text_channel(
                f'village {i + 1}',
                overwrites=overwrites,
                topic=topic
            )

            await ctg_cohort.create_voice_channel(
                f'village {i + 1} voice',
                overwrites=overwrites
            )

        def get_village_role(i):
            return get(guild.roles, name=f'Village {i + 1}')

        role_students = get(guild.roles, name='Students')
        students = role_students.members
        random.shuffle(students)
        n = len(students) // 5  # max no. of students per village

        if len(students) % 5 > 2:
            n += 1

        for i in range(n):
            role_village = await guild.create_role(name=f'Village {i + 1}')
            await create_village_channels(cohort_data, role_village, i)

        roles_villages = [x for x in map(get_village_role, range(n))]
        chunks = (students[i:i + n] for i in range(0, len(students), n))

        for chunk in chunks:
            for i, student in enumerate(chunk):
                await student.add_roles(roles_villages[i])

    @tasks.loop(seconds=1)
    async def trigger_loop(self):
        if now().minute == 0:
            print(f'{green}{now()}: Checking schedule...{reset}')
            self.check_schedule.start()
            self.trigger_loop.cancel()

    @tasks.loop(seconds=3600)
    async def check_schedule(self):
        utils.active_cohort = get_active_cohort()
        cohort_data = utils.active_cohort
        start_date = datetime.strptime(cohort_data['start_date'], '%Y-%m-%d')\
            .astimezone(tz)\
            .replace(hour=0)
        _now = now()

        if _now >= start_date \
                and _now < start_date + \
                timedelta(days=cohort_data['duration']):
            delta = _now - start_date
            day = delta.days + 1

            guild = self.bot.get_guild(utils.guild_id)
            chn_server_log = get(guild.text_channels, name='server-log')
            chn_alerts = get(guild.text_channels, name='alerts')
            chn_townhall = get(guild.voice_channels, name='townhall')
            role_students = get(guild.roles, name='Students')

            # C4T discord.py Botcamp
            if cohort_data['id'] in utils.c4t_dpy:
                # everyday @ 7:00 am
                if _now.hour == 7:
                    await chn_server_log.send(
                        'This is a scheduled test message for '
                        f'{cohort_data["name"]} Day {day}.'
                    )
                # everyday @ 8:00 am
                elif _now.hour == 8:
                    if day == 1:
                        await chn_alerts.send(
                            f'Good Morning {role_students.mention}, this is a '
                            'reminder for our Townhall at 9:00 am. See you at '
                            f'{chn_townhall.mention}!'
                        )
                    elif day == 4:
                        # await self.assign_groups(guild, cohort_data)
                        await chn_alerts.send(
                            f'Good Morning {role_students.mention}, you are '
                            'put into groups for your Day-09 project. All the '
                            'best!'
                        )
                    elif day == 9:
                        await chn_alerts.send(
                            f'Good Morning {role_students.mention}, all the '
                            'best on your final day!'
                        )
                    else:
                        await chn_alerts.send(
                            f'Good Morning {role_students.mention}, all the '
                            'best for today!\n'
                        )
                # everyday @ 10:00 am
                elif _now.hour == 10:
                    await self.assign_peers(
                        guild, cohort_data, day, str(_now.date())
                    )
                # days 1 - 8 @ 4:00 pm
                elif _now.hour == 16:
                    if day != 9:
                        await chn_alerts.send(
                            f'Good Evening {role_students.mention}, this is a '
                            'reminder to discuss your projects with your '
                            'assigned peers before 6:00 pm.'
                        )
                # days 1, 2, 4 & 9 @ 5:00 pm
                elif _now.hour == 17:
                    if day == 1 or day == 2 or day == 4 or day == 9:
                        await chn_alerts.send(
                            f'Hi {role_students.mention}, this is a reminder '
                            'for our Townhall at 6:00 pm. See you at '
                            f'{chn_townhall.mention}!'
                        )
            # C4W discord.py Botcamp
            elif cohort_data['id'] in utils.c4w_dpy:
                # everyday @ 7:00 am
                if _now.hour == 7:
                    await chn_server_log.send(
                        'This is a scheduled test message for '
                        f'{cohort_data["name"]} Day {day}.'
                    )
                # # everyday @ 8:00 am
                # elif _now.hour == 8:
                #     if day == 4:
                #         await self.assign_groups(guild, cohort_data)
                # everyday @ 10:00 am
                elif _now.hour == 10:
                    await self.assign_peers(
                        guild, cohort_data, day, str(_now.date())
                    )

    @trigger_loop.before_loop
    async def before_trigger_loop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Schedule(bot))
