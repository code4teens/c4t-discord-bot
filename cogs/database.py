import sqlite3

from discord.ext import commands


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('Pyrates')
    async def sql(self, ctx, command):
        """
        Runs SQL command

        Args:
            command: SQL command wrapped in double quotes
        """
        with sqlite3.connect(f'db/{ctx.guild.id}.sqlite') as con:
            cur = con.cursor()
            cur.execute(command)
            recs = cur.fetchall()
            con.commit()

        if len(recs) > 0:
            text = ['```']

            for rec in recs:
                text.append(', '.join([*map(str, rec)]))

            text.append('```')
            await ctx.reply('\n'.join(text))

    @sql.error
    async def sql_error(self, ctx, exc):
        if isinstance(exc, commands.CommandInvokeError) \
                or isinstance(exc, commands.ExpectedClosingQuoteError) \
                or isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$sql "<command>"```')


def setup(bot):
    bot.add_cog(Database(bot))
