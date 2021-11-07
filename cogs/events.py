from discord.ext import commands
from discord.utils import get
import discord

from utils import API_URL, green, now, red, s, reset
import requests
import utils


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # IMPORTANT: bot can only be in 1 server
        utils.guild_id = self.bot.guilds[0].id
        print(f'{green}{now()}: {self.bot.user.name} is online!{reset}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            # update bot table
            bot_url = f'{API_URL}/bots/{member.id}'
            put_bot_data = {
                'name': member.name,
                'discriminator': member.discriminator,
                'display_name': member.display_name
            }
            bot_r = s.put(bot_url, json=put_bot_data, timeout=5)

            if bot_r.status_code == requests.codes.not_found:
                return
            elif bot_r.status_code != requests.codes.ok:
                bot_r.raise_for_status()

            # assign '@Student Bots' role
            role_student_bots = get(member.guild.roles, name='Student Bots')

            await member.add_roles(role_student_bots)

            bot_data = bot_r.json()
            cohort_id = bot_data['cohort']['id']

            # discord.py Botcamp
            if cohort_id in utils.dpy:
                user_id = bot_data['user']['id']

                # get user data
                user_url = f'{API_URL}/users/{user_id}'
                user_r = s.get(user_url, timeout=5)

                if user_r.status_code != requests.codes.ok:
                    user_r.raise_for_status()

                user_data = user_r.json()
                channels = user_data['channels']
                chn_eval_id = next(
                    channel['id'] for channel in channels
                    if channel['cohort']['id'] == cohort_id
                )

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
                msg_id = bot_data['msg_id']
                chn_server_log = get(
                    member.guild.text_channels, name='server-log'
                )
                msg = await chn_server_log.fetch_message(msg_id)

                await msg.add_reaction('🟢')
        else:
            # update user table
            user_url = f'{API_URL}/users/{member.id}'
            put_user_data = {
                'name': member.name,
                'discriminator': member.discriminator,
                'display_name': member.display_name
            }
            user_r = s.put(user_url, json=put_user_data, timeout=5)

            if user_r.status_code == requests.codes.not_found:
                return
            elif user_r.status_code != requests.codes.ok:
                user_r.raise_for_status()

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
            r.raise_for_status()

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
            r.raise_for_status()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            url = f'{API_URL}/bots/{member.id}'
            r = s.delete(url, timeout=5)

            if r.status_code == requests.codes.not_found:
                return
            elif r.status_code != requests.codes.ok:
                r.raise_for_status()

        # send log to '#server-log'
        chn_server_log = get(member.guild.text_channels, name='server-log')

        await chn_server_log.send(
            '```diff\n'
            f'# {now()}\n'
            '\n'
            f'- {member}: {member.id} left the server.```'
        )

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.name == after.name:
            return

        # update channel table
        url = f'{API_URL}/channels/{after.id}'
        data = {'name': after.name}
        r = s.put(url, json=data, timeout=5)

        if r.status_code == requests.codes.not_found:
            return
        elif r.status_code != requests.codes.ok:
            r.raise_for_status()

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        # update channel table
        url = f'{API_URL}/channels/{channel.id}'
        r = s.delete(url, timeout=5)

        if r.status_code == requests.codes.not_found:
            return
        elif r.status_code != requests.codes.ok:
            r.raise_for_status()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await ctx.message.add_reaction('🟢')

        if ctx.command.name == 'say':
            try:
                await ctx.message.delete()
            except discord.Forbidden as exc:
                pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        _now = now()
        guild = self.bot.get_guild(utils.guild_id)
        cmd = f'{ctx.prefix}{ctx.command.name}' \
            if ctx.command is not None else None

        # reply with error message
        if isinstance(exc, commands.MissingRole):
            await ctx.reply(f'You are not authorised to use `{cmd}`!')
        elif isinstance(exc, commands.NoPrivateMessage):
            await ctx.reply(f'You may not use `{cmd}` in a private message!')
        elif isinstance(exc, commands.CommandNotFound):
            await ctx.reply('I do not recognise that command!')
        elif isinstance(exc, commands.CommandInvokeError):
            print(f'{red}{_now}: {repr(exc)}{reset}')
            await ctx.reply('Something went wrong...')
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
                f'- {repr(exc)}```^\n'
                f'{ctx.message.jump_url}'
            )
            chn_error_log = discord.utils.get(
                guild.text_channels,
                name='error-log'
            )

            await chn_error_log.send(message)

            print(f'{red}{_now}: {repr(exc)}{reset}')

        await ctx.message.add_reaction('🔴')


def setup(bot):
    bot.add_cog(Events(bot))
