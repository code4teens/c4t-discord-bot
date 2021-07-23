import re
import sqlite3

from discord.ext import commands
from discord.ext.commands.errors import CommandError
import discord


class Student(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class MultipleBotApplication(CommandError):
        """
        Exception raised when multiple bot applications are made.
        """
        pass

    class WrongBotPermissions(CommandError):
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

        if match:
            bot_id = int(match.group(1))
            perm = int(match.group(2))

            if perm == 257088:
                with sqlite3.connect(f'db/{ctx.guild.id}.sqlite') as con:
                    cur = con.cursor()
                    cur.execute(
                        'SELECT bot_id FROM students WHERE id = ?',
                        (ctx.author.id,)
                    )
                    rec, = cur.fetchone()

                if rec is None:
                    await ctx.reply(
                        'Your bot will be added into the server soon.'
                    )

                    # prompt '@Pyrates' to add student bot
                    chn_server_log = discord.utils.get(
                        ctx.guild.text_channels,
                        name='server-log'
                    )
                    role_devs = discord.utils.get(
                        ctx.guild.roles,
                        name='Pyrates'
                    )
                    msg = await chn_server_log.send(
                        f'{role_devs.mention} Kindly add this bot as soon as '
                        'possible.\n'
                        f'{link}'
                    )

                    # update database
                    with sqlite3.connect(f'db/{ctx.guild.id}.sqlite') as con:
                        cur = con.cursor()
                        cur.execute(
                            'UPDATE students SET bot_id = ?, bot_msg_id = ? '
                            'WHERE id = ?',
                            (bot_id, msg.id, ctx.author.id)
                        )
                else:
                    raise self.MultipleBotApplication
            else:
                raise self.WrongBotPermissions
        else:
            raise commands.BadArgument

    @commands.command()
    @commands.has_role('Students')
    async def stats(self, ctx):
        """
        Shows user stats
        """
        with sqlite3.connect(f'db/{ctx.guild.id}.sqlite') as con:
            cur = con.cursor()
            cur.execute(
                'SELECT lvl, xp FROM students WHERE id = ?',
                (ctx.author.id,)
            )
            lvl, xp = cur.fetchone()

        text = f'You are Level {lvl} with {xp} XP.'
        await ctx.reply(text)

    @addbot.error
    async def addbot_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument) \
                or isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$addbot <link>```')
        elif isinstance(exc, self.MultipleBotApplication):
            await ctx.reply('You already submitted a request for a bot.')
        elif isinstance(exc, self.WrongBotPermissions):
            await ctx.reply(
                'You are granting your bot the wrong permissions. Kindly '
                'reconfigure and run the command again.'
            )


def setup(bot):
    bot.add_cog(Student(bot))
