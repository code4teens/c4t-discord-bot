from datetime import datetime

from discord.ext import commands
import discord

from utils import API_URL, s, tz
import requests


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class MissingAttachment(commands.errors.CommandError):
        """
        Exception raised when required attachment is missing.

        This inherits from :exc:`CommandError`.
        """
        pass

    def to_date(argument):
        date = datetime.strptime(argument, '%Y-%m-%d')

        return date.astimezone(tz)

    @commands.command()
    @commands.has_role('Pyrates')
    async def devecho(self, ctx, channel: discord.TextChannel, message):
        """
        Sends message to a channel

        Args:
            channel: Destination channel
            message: Message body wrapped in double quotes
        """
        await channel.send(message)

    @commands.command()
    @commands.has_role('Pyrates')
    async def devattach(self, ctx, channel: discord.TextChannel, message):
        """
        Sends message with attachment to a channel

        Args:
            channel: Destination channel
            message: Message body wrapped in double quotes
            attachment: Any file supported by Discord
        """
        if len(ctx.message.attachments) > 0:
            file = await ctx.message.attachments[0].to_file()

            await channel.send(message, file=file)
        else:
            raise self.MissingAttachment

    @commands.command()
    @commands.has_role('Pyrates')
    async def givexp(self, ctx, user: discord.Member, xp: int = 10):
        """
        Awards XP to a user

        Args:
            user: User to award XP
            xp(int): Optional argument XP amount
        """
        url = f'{API_URL}/users/{user.id}'
        get_r = s.get(url, timeout=5)

        if get_r.status_code != requests.codes.ok:
            get_r.raise_for_status()

        get_data = get_r.json()
        put_data = {'xp': get_data['xp'] + xp}
        r_put = s.put(url, json=put_data, timeout=5)

        if r_put.status_code != requests.codes.ok:
            r_put.raise_for_status()

    @devecho.error
    async def devecho_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument) \
                or isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$devecho <channel> "<message>"```')

    @devattach.error
    async def devattach_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument) \
                or isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$devattach <channel> "<message>"```')
        elif isinstance(exc, self.MissingAttachment):
            await ctx.reply('You forgot to include the attachment.')

    @givexp.error
    async def givexp_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument) \
                or isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$givexp <student> <xp>```')
        elif isinstance(exc, requests.exceptions.RequestException):
            await ctx.reply('Something went wrong...')


def setup(bot):
    bot.add_cog(Dev(bot))
