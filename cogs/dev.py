from datetime import datetime
import sqlite3

from discord.ext import commands
from discord.ext.commands.errors import CommandError
import discord

import utils as utl


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class MissingAttachment(CommandError):
        """
        Exception raised when required attachment is missing.
        """
        pass

    def to_date(argument):
        return datetime.strptime(argument, '%Y-%m-%d')

    @commands.command()
    @commands.has_role('Pyrates')
    async def setup(self, ctx, date: to_date):
        """
        Sets up server

        Args:
            date: Date in 'yyyy-mm-dd'

        Notes:
            1. Sends 'Code of Conduct' to '#code-of-conduct'
            2. Sends 'Survival Guide' to '#alerts'
            3. Sends 'Padlet' reminder to '#padlet'
        """
        if date < datetime.now():
            raise commands.BadArgument

        with sqlite3.connect(f'db/{ctx.guild.id}.sqlite') as con:
            cur = con.cursor()
            cur.execute('SELECT value FROM main WHERE key = "coc_msg_id"')
            rec = cur.fetchone()

        if rec is None:
            # send 'Code of Conduct' to '#code-of-conduct'
            chn_coc = discord.utils.get(
                ctx.guild.text_channels,
                name='code-of-conduct'
            )
            role_students = discord.utils.get(
                ctx.guild.roles,
                name='Students'
            )
            msg = await chn_coc.send(
                'I acknowledge that I have read the Code of Conduct in '
                'details and am agreeable to the rules, regulations, terms '
                'and conditions set by the C4T establishment. I will abide by '
                'the Code of Conduct and I am aware that action will be taken '
                'against me for any form of misconduct.\n'
                '\n'
                f'React OK to be granted {role_students.mention} Role.\n'
                '\n'
                f'{utl.COC}'
            )
            await msg.add_reaction('🆗')
            await ctx.reply(f'{msg.jump_url}')

            # send 'Surival Guide' to '#alerts'
            chn_alerts = discord.utils.get(
                ctx.guild.text_channels,
                name='alerts'
            )
            await chn_alerts.send(
                f'{role_students.mention}, below guide will serve as your '
                'reference during the BotCamp.\n'
                '\n'
                f'{utl.GUIDE}'
            )

            # send 'Padlet' reminder to '#padlet'
            chn_padlet = discord.utils.get(
                ctx.guild.text_channels,
                name='padlet'
            )
            await chn_padlet.send(
                'Create your own Padlet and share them here! Check out '
                'Prag\'s Padlet!\n'
                '\n'
                f'{utl.PRAG_PADLET}'
            )

            # update database
            with sqlite3.connect('db/main.sqlite') as con:
                cur = con.cursor()
                cur.execute(
                    'REPLACE INTO main VALUES (?, ?)',
                    ('active_guild_id', ctx.guild.id)
                )
                con.commit()

            with sqlite3.connect(f'db/{ctx.guild.id}.sqlite') as con:
                cur = con.cursor()
                cur.executemany(
                    'INSERT INTO main VALUES (?, ?)',
                    [
                        ('coc_msg_id', msg.id),
                        ('start_date', date),
                        ('eval_code', 1)
                    ]
                )
                con.commit()
        else:
            chn_coc = discord.utils.get(
                ctx.guild.text_channels,
                name='code-of-conduct'
            )
            msg_id, = [*map(int, rec)]
            msg = chn_coc.get_partial_message(msg_id)
            await ctx.reply(msg.jump_url)

    @commands.command()
    @commands.has_role('Pyrates')
    async def devecho(self, ctx, channel: discord.TextChannel, message):
        """
        Sends message to a specific channel

        Args:
            channel: Destination channel
            message: Message body wrapped in quotes
        """
        await channel.send(message)

    @commands.command()
    @commands.has_role('Pyrates')
    async def devattach(self, ctx, channel: discord.TextChannel, message):
        """
        Sends message with attachment to a specific channel

        Args:
            channel: Destination channel
            message: Message body wrapped in quotes
            attachment: Any file supported by Discord
        """
        if len(ctx.message.attachments) > 0:
            file = await ctx.message.attachments[0].to_file()
            await channel.send(message, file=file)
        else:
            raise self.MissingAttachment

    @commands.command()
    @commands.has_role('Pyrates')
    async def givexp(self, ctx, student: discord.Member, xp: int = 10):
        """
        Gives XP to student

        Args:
            student: Student to award XP
            xp: XP amount
        """
        role_students = discord.utils.get(ctx.guild.roles, name='Students')

        if role_students in student.roles:
            with sqlite3.connect(f'db/{ctx.guild.id}.sqlite') as con:
                cur = con.cursor()
                cur.execute(
                    'SELECT lvl, xp FROM students WHERE id = ?',
                    (student.id,)
                )
                lvl, cur_xp = cur.fetchone()

            cur_xp += xp

            while True:
                xp_next_lvl = 5 * lvl ** 2 + 50 * lvl + 100

                if cur_xp >= xp_next_lvl:
                    lvl += 1
                    cur_xp -= xp_next_lvl
                else:
                    break

            # update database
            with sqlite3.connect(f'db/{ctx.guild.id}.sqlite') as con:
                cur = con.cursor()
                cur.execute(
                    'UPDATE students SET lvl = ?, xp = ? WHERE id = ?',
                    (lvl, cur_xp, student.id)
                )
                con.commit()
        else:
            raise commands.BadArgument

    @commands.command()
    @commands.has_role('Pyrates')
    async def leaderboard(self, ctx, n: int = 5):
        """
        Shows leaderboard

        Args:
            n: Optional argument to only show top n results
        """
        text = (
            '```\n'
            '-----------\n'
            'LEADERBOARD\n'
            '-----------\n'
        )

        with sqlite3.connect(f'db/{ctx.guild.id}.sqlite') as con:
            cur = con.cursor()
            cur.execute(
                'SELECT id, lvl, xp FROM students '
                'ORDER BY lvl DESC, xp DESC '
                'LIMIT ?',
                (n,)
            )
            recs = cur.fetchall()

        for i, rec in enumerate(recs, start=1):
            id, *data = rec
            lvl, xp = [*map(str, data)]
            user = discord.utils.get(ctx.guild.members, id=id)
            text += (
                f'{i}. LEVEL{lvl.rjust(3)}:{xp.rjust(5)} '
                f'XP: {user.display_name}\n'
            )

        text += '```'
        await ctx.reply(text)

    @commands.command()
    @commands.has_role('Pyrates')
    async def evals(self, ctx, n: int = 0):
        """
        Shows eval pairs

        Args:
            n: Optional argument to show Day n evals
        """

        with sqlite3.connect(f'db/{ctx.guild.id}.sqlite') as con:
            cur = con.cursor()
            if n == 0:
                cur.execute(
                    'SELECT a.* FROM evals a INNER JOIN ('
                    'SELECT MAX(day) maxDay FROM evals) b '
                    'WHERE a.day = b.maxDay'
                )
            else:
                cur.execute(
                    'SELECT * FROM evals WHERE day = ?',
                    (n,)
                )
            recs = cur.fetchall()

        text = (
            '```\n'
            '-----------\n'
            f'DAY {n} EVALS\n'
            '-----------\n'
        )

        for rec in recs:
            _, _, code, coder_id, tester_id = rec
            code_str = str(code).zfill(4)
            coder = discord.utils.get(ctx.guild.members, id=coder_id)
            tester = discord.utils.get(ctx.guild.members, id=tester_id)
            text += (
                f'{code_str}: {tester.display_name} -> {coder.display_name} \n'
            )

        text += '```'
        await ctx.reply(text)

    @setup.error
    async def setup_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument):
            await ctx.reply('You entered an invalid date!')
        elif isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$setup <date>```')

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

    @leaderboard.error
    async def leaderboard_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument):
            await ctx.reply('```$leaderboard [n=5]```')


def setup(bot):
    bot.add_cog(Dev(bot))
