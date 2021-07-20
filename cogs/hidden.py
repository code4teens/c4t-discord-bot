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

    @commands.command(hidden=True)
    async def ichooseyou(self, ctx, pokemon):
        """
        Summons a Pokémon

        Args:
            pokemon: Pokémon name or index number
        """
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
        data = requests.get(url).json()
        await ctx.reply(data['sprites']['front_default'])

    @ichooseyou.error
    async def ichooseyou_error(self, ctx, exc):
        if isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$ichooseyou <pokemon>```')


def setup(bot):
    bot.add_cog(Day8(bot))
