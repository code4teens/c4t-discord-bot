import re

from discord.ext import commands
from discord.utils import get
import requests

from utils import API_URL, BOT_PERM, s
import utils


class Student(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class MultipleBotApplication(commands.errors.CommandError):
        """
        Exception raised when multiple applications for the same bot are made.
        """
        pass

    class WrongBotPermissions(commands.errors.CommandError):
        """
        Exception raised when a bot is granted the wrong permissions.
        """
        pass

    @commands.command()
    @commands.has_role('Students')
    async def addbot(self, ctx, link):
        """
        Adds bot to server

        Args:
            link: Bot-invite link
        """
        regex = (
            r'https://discord.com/api/oauth2/authorize\?client_id=([0-9]{18})'
            r'&permissions=([0-9]+)&scope=bot'
        )
        match = re.fullmatch(regex, link)

        if not match:
            raise commands.BadArgument

        bot_id = int(match.group(1))
        perm = int(match.group(2))

        if perm != BOT_PERM:
            raise self.WrongBotPermissions

        # get bot data
        get_url = f'{API_URL}/bots/{bot_id}'
        get_r = s.get(get_url, timeout=5)

        if get_r.status_code == requests.codes.ok:
            raise self.MultipleBotApplication
        elif get_r.status_code != requests.codes.not_found:
            get_r.raise_for_status()

        # notify user bot will be added to server
        await ctx.reply('Your bot will be added into the server soon.')

        # prompt '@Pyrates' to add student bot
        role_devs = get(ctx.guild.roles, name='Pyrates')
        chn_server_log = get(ctx.guild.text_channels, name='server-log')
        msg = await chn_server_log.send(
            f'{role_devs.mention} Kindly add {ctx.author.mention}\'s bot:\n'
            f'{link}'
        )

        # update database
        post_url = f'{API_URL}/bots'
        data = {
            'id': bot_id,
            'user_id': ctx.author.id,
            'cohort_id': utils.active_cohort['id'],
            'msg_id': msg.id
        }
        post_r = s.post(post_url, json=data, timeout=5)

        if post_r.status_code != requests.codes.created:
            post_r.raise_for_status()

    @addbot.error
    async def addbot_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument) \
                or isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$addbot <link>```')
        elif isinstance(exc, self.MultipleBotApplication):
            await ctx.reply('Bot already added into server.')
        elif isinstance(exc, self.WrongBotPermissions):
            await ctx.reply(
                'You are granting your bot the wrong permissions. Kindly '
                'reconfigure and try again.'
            )


def setup(bot):
    bot.add_cog(Student(bot))
