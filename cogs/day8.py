from discord.ext import commands
import requests


class Day8(commands.Cog, name='Day 8'):
    def __init__(self, bot):
        self.bot = bot

    def get_ip(self):
        url = 'https://api.ipify.org/?format=json'
        data = requests.get(url).json()
        return data['ip']

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
        ip = self.get_ip()
        await ctx.reply(ip)

    @commands.command()
    async def iplocation(self, ctx):
        """
        Returns the bot's IPv4 address geolocation
        """
        ip = self.get_ip()
        url = f'https://ipinfo.io/{ip}/geo'
        data = requests.get(url).json()
        await ctx.reply(f'{data["city"]}, {data["region"]}, {data["country"]}')

    @commands.command()
    async def iplocation_2(self, ctx):
        """
        Reacts with a flag corresponding to the bot's IPv4 address geolocation
        """
        ip = self.get_ip()
        url = f'https://ipinfo.io/{ip}/geo'
        url2 = f'https://api.ip2country.info/ip?{ip}'
        data = requests.get(url).json()
        data2 = requests.get(url2).json()
        await ctx.reply(f'{data["city"]}, {data["region"]}, {data["country"]}')
        await ctx.message.add_reaction(data2['countryEmoji'])


def setup(bot):
    bot.add_cog(Day8(bot))
