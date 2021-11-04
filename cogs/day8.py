from discord.ext import commands
import requests


class Day8(commands.Cog, name='Day 8'):
    def __init__(self, bot):
        self.bot = bot

    def get_ip(self):
        url = 'https://api.ipify.org/?format=json'
        r = requests.get(url)

        if r.status_code != requests.codes.ok:
            r.raise_for_status()

        data = r.json()

        return data['ip']

    @commands.command()
    async def ip(self, ctx):
        """
        Returns bot's IPv4 address
        """
        ip = self.get_ip()

        await ctx.reply(ip)

    @commands.command()
    async def iploc(self, ctx):
        """
        Returns bot's location
        """
        ip = self.get_ip()
        url = f'https://ipinfo.io/{ip}/geo'
        r = requests.get(url)

        if r.status_code != requests.codes.ok:
            r.raise_for_status()

        data = r.json()
        message = f'{data["city"]}, {data["region"]}, {data["country"]}'

        await ctx.reply(message)


def setup(bot):
    bot.add_cog(Day8(bot))
