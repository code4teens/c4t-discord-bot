from discord.ext import commands
import requests


class Day8(commands.Cog, name='Day 8'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def joke(self, ctx):
        """
        Tells a joke
        """
        url = 'https://official-joke-api.appspot.com/random_joke'
        data = requests.get(url).json()
        await ctx.reply(
            f'{data["setup"]}\n'
            '\n'
            f'*{data["punchline"].strip()}*'
        )

    @commands.command()
    async def ip(self, ctx):
        """
        Returns the bot's IPv4 address
        """
        url = 'https://api.ipify.org/?format=json'
        data = requests.get(url).json()
        await ctx.reply(data['ip'])


def setup(bot):
    bot.add_cog(Day8(bot))
