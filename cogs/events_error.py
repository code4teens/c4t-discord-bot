from datetime import datetime
import traceback

from discord.ext import commands
import discord
import pytz

import utils as utl


class ErrorEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timezone = pytz.timezone('Asia/Kuala_Lumpur')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        now = datetime.now(self.timezone)
        date = now.strftime("%Y-%m-%d")
        cmd = (
            f'{ctx.prefix}{ctx.command.name}'
            if ctx.command is not None else None
        )

        # reply with error message
        if isinstance(exc, commands.MissingRole):
            await ctx.reply(f'You are not authorised to use `{cmd}`!')
        elif isinstance(exc, commands.NoPrivateMessage):
            await ctx.reply(f'You may not use `{cmd}` in a private message!')
        elif isinstance(exc, commands.CommandNotFound):
            await ctx.reply('I do not recognise that command!')
        else:
            # send log to '#error-log'
            if ctx.guild is not None:
                chn_error_log = discord.utils.get(
                    ctx.guild.text_channels,
                    name='error-log'
                )
                await chn_error_log.send(
                    '```py\n'
                    f'# {now}\n'
                    '\n'
                    f'{ctx.message.content}\n'
                    f'{ctx.author.display_name}: {ctx.author.id}\n'
                    f'{repr(exc)}```^\n'
                    f'{ctx.message.jump_url}'
                )

            # write log to log/cmd-{date}.log
            with open(f'log/cmd-{date}.log', 'a') as f:
                guild = ctx.guild if ctx.guild is not None else None
                guild_name = guild.name if guild is not None else None
                guild_id = guild.id if guild is not None else None
                f.write(
                    f'{now},\n'
                    f'guild_name: {guild_name},\n'
                    f'guild_id: {guild_id},\n'
                    f'user_nick: {ctx.author.display_name},\n'
                    f'user_id: {ctx.author.id},\n'
                    f'msg: {ctx.message.content},\n'
                    f'msg_url: {ctx.message.jump_url}\n'
                    f'exc: {repr(exc)}\n'
                    '\n'
                )

            print(f'{utl.red}{now}: {repr(exc)}{utl.reset}')

        await ctx.message.add_reaction('🔴')

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        now = datetime.now(self.timezone)
        date = now.strftime("%Y-%m-%d")
        guild = None

        # write log to log/evt-{date}.log
        with open(f'log/evt-{date}.log', 'a') as f:
            if event == 'on_guild_join':
                guild = args[0]
                f.write(
                    f'{now},\n'
                    f'event: {event},\n'
                    f'guild_name: {guild.name},\n'
                    f'guild_id: {guild.id},\n'
                    '\n'
                )
            elif event == 'on_member_join' or event == 'on_member_remove':
                member = args[0]
                guild = member.guild
                f.write(
                    f'{now},\n'
                    f'event: {event},\n'
                    f'guild_name: {member.guild.name},\n'
                    f'guild_id: {member.guild.id},\n'
                    f'user_nick: {member.display_name},\n'
                    f'user_id: {member.id}\n'
                    '\n'
                )
            elif event == 'on_message':
                message = args[0]
                guild = message.guild if message.guild is not None else None
                guild_name = guild.name if guild is not None else None
                guild_id = guild.id if guild is not None else None
                f.write(
                    f'{now},\n'
                    f'event: {event},\n'
                    f'guild_name: {guild_name},\n'
                    f'guild_id: {guild_id},\n'
                    f'user_nick: {message.author.display_name},\n'
                    f'user_id: {message.author.id}\n'
                    f'msg: {message.content}\n'
                    f'msg_url: {message.jump_url}\n'
                    '\n'
                )
            elif event == 'on_raw_reaction_add':
                payload = args[0]
                guild_id = payload.guild_id \
                    if payload.guild_id is not None else None
                user = payload.member if payload.member is not None else None
                user_nick = user.display_name if user is not None else None
                user_id = user.id if user is not None else None
                f.write(
                    f'{now},\n'
                    f'event: {event},\n'
                    f'guild_name: {None},\n'
                    f'guild_id: {guild_id},\n'
                    f'user_nick: {user_nick},\n'
                    f'user_id: {user_id}\n'
                    f'emoji: {payload.emoji}\n'
                    f'msg_id: {payload.message_id}\n'
                    '\n'
                )
            else:
                f.write(
                    f'{now}\n'
                    f'event: {event}\n'
                    f'args: {args}\n'
                    '\n'
                )

        # send log to #error-log
        if guild is not None:
            chn_error_log = discord.utils.get(
                guild.text_channels,
                name='error-log'
            )
            await chn_error_log.send(
                f'```py\n'
                f'# {now}\n'
                f'\n{traceback.format_exc()}```'
            )

        print(f'{utl.red}{now}\n{traceback.format_exc()}{utl.reset}')


def setup(bot):
    bot.add_cog(ErrorEvents(bot))
