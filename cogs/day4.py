import random

from discord.ext import commands


class Day4(commands.Cog, name='Day 4'):
    def __init__(self, bot):
        self.bot = bot
        self.shapes = ['rock', 'paper', 'scissor']

    async def rps(self, ctx, shape):
        bot_shape = random.choice(self.shapes)
        index = self.shapes.index(shape)
        bot_index = self.shapes.index(bot_shape)
        diff = index - bot_index

        if diff == 1 or diff == -2:
            await ctx.reply(
                f'{shape.capitalize()} beats {bot_shape}. You win!'
            )
        elif diff == 2 or diff == -1:
            await ctx.reply(
                f'{bot_shape.capitalize()} beats {shape}. I win!'
            )
        elif diff == 0:
            await ctx.reply(f'It\'s a tie!')

    @commands.command()
    async def echo(self, ctx, message):
        """
        Repeats your message

        Args:
            message: Message body wrapped in double quotes
        """
        await ctx.reply(message)

    @commands.command()
    async def say(self, ctx, message):
        """
        Repeats your message but deletes the invocation

        Args:
            message: Message body wrapped in double quotes
        """
        await ctx.channel.send(message)

    @commands.command()
    async def rock(self, ctx):
        """
        Chooses 'Rock' in a game of Rock, paper, scissor
        """
        await self.rps(ctx, 'rock')

    @commands.command()
    async def paper(self, ctx):
        """
        Chooses 'Paper' in a game of Rock, paper, scissor
        """
        await self.rps(ctx, 'paper')

    @commands.command()
    async def scissor(self, ctx):
        """
        Chooses 'Scissor' in a game of Rock, paper, scissor
        """
        await self.rps(ctx, 'scissor')

    @echo.error
    async def echo_error(self, ctx, exc):
        if isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$echo "<message>"```')

    @say.error
    async def say_error(self, ctx, exc):
        if isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$say "<message>"```')


def setup(bot):
    bot.add_cog(Day4(bot))
