from discord.ext import commands
import requests


class Hidden(commands.Cog, name='Hidden'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def joke(self, ctx):
        """
        Tells a joke
        """
        url = 'https://icanhazdadjoke.com'
        headers = {'Accept': 'application/json'}
        r = requests.get(url, headers=headers)

        if r.status_code != requests.codes.ok:
            r.raise_for_status()

        data = r.json()

        await ctx.reply(data['joke'])

    @commands.command(hidden=True)
    async def ichooseyou(self, ctx, pokemon):
        """
        Summons a Pokémon

        Args:
            pokemon: Pokémon name or index number
        """
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
        r = requests.get(url)

        if r.status_code != requests.codes.ok:
            r.raise_for_status()

        data = r.json()

        await ctx.reply(data['sprites']['front_default'])

    @ichooseyou.error
    async def ichooseyou_error(self, ctx, exc):
        if isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$ichooseyou <pokemon>```')


def setup(bot):
    bot.add_cog(Hidden(bot))
