import random

from discord.ext import commands


class Day4(commands.Cog, name='Day 4'):
    def __init__(self, bot):
        self.bot = bot
        self.shapes = ['rock', 'paper', 'scissor']

    @commands.command()
    async def echo(self, ctx, message):
        """
        Repeats your message
        """
        await ctx.reply(message)

    @commands.command()
    async def say(self, ctx, message):
        """
        Repeats your message and deletes the invocation
        """
        await ctx.channel.send(message)

    # @commands.command()
    # async def rps(self, ctx):
    #     """
    #     Plays a game of 'Rock, paper, scissor'
    #     """
    #     your_shape = random.choice(self.shapes)
    #     bot_shape = random.choice(self.shapes)
    #     your_index = self.shapes.index(your_shape)
    #     bot_index = self.shapes.index(bot_shape)
    #     diff = your_index - bot_index

    #     if diff == 1:
    #         pass


def setup(bot):
    bot.add_cog(Day4(bot))
