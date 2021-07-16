from discord.ext import commands


class Day3(commands.Cog, name='Day 3'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """
        Replies with a 'Hello !'
        """
        await ctx.reply('Hello !')

    @commands.command()
    async def greet(self, ctx):
        """
        Replies with a 'Hello <name>'
        """
        await ctx.reply(f'Hello {ctx.author.name}')

    @commands.command()
    async def greetings(self, ctx):
        """
        Replies with a 'Hello <nickname>'
        """
        await ctx.reply(f'Hello {ctx.author.display_name}')


def setup(bot):
    bot.add_cog(Day3(bot))
