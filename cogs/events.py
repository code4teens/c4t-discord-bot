import random

from discord.ext import commands
from discord.utils import get
import discord

from utils import API_URL, COC_MSG_ID, green, now, red, s, reset
import requests
import utils


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.greetings = [
            'Greetings', 'Hey', 'Hi', 'Howdy', 'Welcome', 'Wassup', 'Yo'
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        # IMPORTANT: bot can only be in 1 server
        utils.guild_id = self.bot.guilds[0].id
        print(f'{green}{now()}: {self.bot.user.name} is online!{reset}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            # update database
            bot_url = f'{API_URL}/bots/{member.id}'
            put_data = {
                'name': member.name,
                'discriminator': member.discriminator,
                'display_name': member.display_name
            }
            bot_r = s.put(bot_url, json=put_data, timeout=5)

            if bot_r.status_code == requests.codes.not_found:
                return
            elif bot_r.status_code != requests.codes.ok:
                bot_r.raise_for_status()  # TODO: log error

            bot_data = bot_r.json()
            msg_id = bot_data['msg_id']
            user_id = bot_data['user']['id']
            cohort_id = bot_data['cohort']['id']

            # get user data
            user_url = f'{API_URL}/users/{user_id}'
            user_r = s.get(user_url, timeout=5)

            if user_r.status_code != requests.codes.ok:
                user_r.raise_for_status()  # TODO: log error

            user_data = user_r.json()
            channels = user_data['channels']
            chn_eval_id = next(
                channel['id'] for channel in channels
                if channel['cohort']['id'] == cohort_id
            )

            # assign bot '@Student Bots' role
            role_student_bots = get(member.guild.roles, name='Student Bots')

            await member.add_roles(role_student_bots)

            # grant bot permission to view user channel
            chn_eval = get(member.guild.text_channels, id=chn_eval_id)

            await chn_eval.set_permissions(member, read_messages=True)

            # send message to user channel informing bot entrance
            user = get(member.guild.members, id=user_id)
            message = (
                f'Hi {user.mention}, you may interact with your bot '
                f'{member.mention} here!'
            )

            await chn_eval.send(message)

            # mark bot-invite message in '#server-log' as successful
            chn_server_log = get(member.guild.text_channels, name='server-log')
            msg = await chn_server_log.fetch_message(msg_id)

            await msg.add_reaction('🟢')
        else:
            # send welcome DM
            chn_coc = get(member.guild.text_channels, name='code-of-conduct')
            msg = chn_coc.get_partial_message(COC_MSG_ID)
            message = (
                f'Welcome to {member.guild}, {member.name}!\n'
                '\n'
                'If you are a student, please see below link:\n'
                f'{msg.jump_url}\n'
                '\n'
                'If you are not a student, please wait for the admins to '
                'grant you your corresponding role.'
            )

            if member.dm_channel is not None:
                await member.dm_channel.send(message)
            else:
                try:
                    dm = await member.create_dm()

                    await dm.send(message)
                except discord.Forbidden as e:
                    pass

        # send log to '#server-log'
        chn_server_log = get(member.guild.text_channels, name='server-log')

        await chn_server_log.send(
            '```diff\n'
            f'# {now()}\n'
            '\n'
            f'+ {member}: {member.id} joined the server.```'
        )

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name == after.display_name:
            return

        # update database
        if after.bot:
            url = f'{API_URL}/bots/{after.id}'
        else:
            url = f'{API_URL}/users/{after.id}'

        data = {'display_name': after.display_name}
        r = s.put(url, json=data, timeout=5)

        if r.status_code == requests.codes.not_found:
            return
        elif r.status_code != requests.codes.ok:
            r.raise_for_status()  # TODO: log error

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name == after.name \
                and before.discriminator == after.discriminator:
            return

        # update database
        if after.bot:
            url = f'{API_URL}/bots/{after.id}'
        else:
            url = f'{API_URL}/users/{after.id}'

        data = {
            'name': after.name,
            'discriminator': after.discriminator,
        }
        r = s.put(url, json=data, timeout=5)

        if r.status_code == requests.codes.not_found:
            return
        elif r.status_code != requests.codes.ok:
            r.raise_for_status()  # TODO: log error

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            url = f'{API_URL}/bots/{member.id}'
            r = s.delete(url, timeout=5)

            if r.status_code == requests.codes.not_found:
                return
            elif r.status_code != requests.codes.ok:
                r.raise_for_status()  # TODO: log error

        # send log to '#server-log'
        chn_server_log = get(member.guild.text_channels, name='server-log')

        await chn_server_log.send(
            '```diff\n'
            f'# {now()}\n'
            '\n'
            f'- {member}: {member.id} left the server.```'
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id is None or payload.user_id == self.bot.user.id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        user = get(guild.members, id=payload.user_id)

        if payload.message_id == COC_MSG_ID \
                and payload.event_type == 'REACTION_ADD' \
                and str(payload.emoji) == '🆗' \
                and len(user.roles) == 1:
            # update database
            user_post_url = f'{API_URL}/users'
            user_data = {
                'id': user.id,
                'name': user.name,
                'discriminator': user.discriminator,
                'display_name': user.display_name
            }
            user_r_post = s.post(user_post_url, json=user_data, timeout=5)

            # user previously created
            if user_r_post.status_code == requests.codes.conflict:
                # update database
                user_put_url = f'{API_URL}/users/{user.id}'
                del user_data['id']
                user_r_put = s.put(user_put_url, json=user_data, timeout=5)

                if user_r_put.status_code != requests.codes.ok:
                    user_r_put.raise_for_status()  # TODO: log error

                user_put_data = user_r_put.json()
                channels = user_put_data['channels']

                # grant user permission to view their channel(s)
                for channel in channels:
                    chn_eval = get(user.guild.text_channels, id=channel['id'])

                    await chn_eval.set_permissions(user, read_messages=True)

            # first-time user creation
            elif user_r_post.status_code != requests.codes.ok:
                user_r_post.raise_for_status()  # TODO: log error

            # assign '@Students' role
            role_students = get(guild.roles, name='Students')

            await user.add_roles(role_students)

            # send welcome message to '#chit-chat'
            greet = random.choice(self.greetings)
            chn_alerts = get(guild.text_channels, name='alerts')
            chn_padlet = get(guild.text_channels, name='padlet')
            message = (
                f'{greet} {user.mention}! Kindly check out '
                f'{chn_alerts.mention} & {chn_padlet.mention}.'
            )
            chn_chit_chat = get(guild.text_channels, name='chit-chat')

            await chn_chit_chat.send(message)

            # update database
            enrolment_url = f'{API_URL}/enrolments'
            enrolment_data = {
                'user_id': user.id,
                'cohort_id': utils.active_cohort['id']
            }
            enrolment_r = s.post(
                enrolment_url, json=enrolment_data, timeout=5
            )

            if enrolment_r.status_code == requests.codes.conflict:
                return
            elif enrolment_r.status_code != requests.codes.created:
                enrolment_r.raise_for_status()  # TODO: log error

            # create user channel
            role_dev_bot = get(guild.roles, name='Pyrate Bot')
            role_bocals = get(guild.roles, name='BOCALs')
            role_observers = get(guild.roles, name='Observers')
            overwrites = {
                role_dev_bot: discord.PermissionOverwrite(
                    read_messages=True
                ),
                role_bocals: discord.PermissionOverwrite(
                    read_messages=True
                ),
                role_observers: discord.PermissionOverwrite(
                    read_messages=True
                ),
                user: discord.PermissionOverwrite(read_messages=True),
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=False
                )
            }
            topic = 'Test your bot here!'
            ctg_bot = get(guild.categories, name='bot')
            chn_eval = await ctg_bot.create_text_channel(
                user.name,
                overwrites=overwrites,
                topic=topic
            )

            # update database
            channel_url = f'{API_URL}/channels'
            channel_data = {
                'id': chn_eval.id,
                'name': chn_eval.name,
                'user_id': user.id,
                'cohort_id': utils.active_cohort['id']
            }
            channel_r = s.post(channel_url, json=channel_data, timeout=5)

            if channel_r.status_code != requests.codes.created:
                channel_r.raise_for_status()  # TODO: log error

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.name == after.name:
            return

        # update database
        url = f'{API_URL}/channels/{after.id}'
        data = {'name': after.name}
        r = s.put(url, json=data, timeout=5)

        if r.status_code == requests.codes.not_found:
            return
        elif r.status_code != requests.codes.ok:
            r.raise_for_status()  # TODO: log error

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await ctx.message.add_reaction('🟢')

        if ctx.command.name == 'say':
            try:
                await ctx.message.delete()
            except discord.Forbidden as e:
                pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        _now = now()
        guild = self.bot.get_guild(utils.guild_id)
        cmd = f'{ctx.prefix}{ctx.command.name}' \
            if ctx.command is not None else None

        # reply with error message
        if isinstance(e, commands.MissingRole):
            await ctx.reply(f'You are not authorised to use `{cmd}`!')
        elif isinstance(e, commands.NoPrivateMessage):
            await ctx.reply(f'You may not use `{cmd}` in a private message!')
        elif isinstance(e, commands.CommandNotFound):
            await ctx.reply('I do not recognise that command!')
        else:
            # send log to '#error-log'
            user = ctx.author
            message = (
                '```diff\n'
                f'# {_now}\n'
                '\n'
                f'+ {ctx.message.content}\n'
                f'+ {user.id}: {user.name}#{user.discriminator}: '
                f'{user.display_name}\n'
                f'- {repr(e)}```^\n'
                f'{ctx.message.jump_url}'
            )
            chn_error_log = discord.utils.get(
                guild.text_channels,
                name='error-log'
            )

            await chn_error_log.send(message)

            print(f'{red}{_now}: {repr(e)}{reset}')

        await ctx.message.add_reaction('🔴')


def setup(bot):
    bot.add_cog(Events(bot))
