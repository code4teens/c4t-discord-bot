from bs4 import BeautifulSoup
from discord.ext import commands
import requests


class Day7(commands.Cog, name='Day 7'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def scrape(self, ctx):
        """
        Scrapes user information from predefined website
        """
        url = 'https://webscraper.io/test-sites/tables'
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'html.parser')
        name1 = soup.tbody.tr.td.find_next('td')
        firstname = name1.text
        name2 = name1.find_next('td')
        lastname = name2.text
        name3 = name2.find_next('td')
        username = name3.text
        await ctx.reply(
            f'First Name = {firstname}\n'
            f'Last Name = {lastname}\n'
            f'Username = {username}'
        )

    @commands.command()
    async def currency(self, ctx):
        """
        Scrapes USD/MYR exchange rate from predefined website
        """
        url = 'https://mtradeasia.com/main/daily-exchange-rates/'
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'html.parser')

        # get currency name
        parent = soup.find('td', attrs={'style': 'line-height: 1;'})
        child = parent.find('small', attrs={'class': 'spansmall'})
        currency = child.br.next_sibling
        update_currency = ' '.join(currency.split())

        # get currency rate
        webuy = soup.find('td', attrs={'class': 'text-center'}).text
        rate = ' '.join(webuy.split())
        msg = (
            f'Currency: {update_currency}\n'
            f'Exchange Rate (MYR): {rate}'
        )
        await ctx.reply(msg)

    @commands.command()
    async def movie(self, ctx, title):
        """
        Scrapes movie storyline from title

        Args:
            title: Movie title wrapped in double quotes
        """
        url = f'https://www.imdb.com/find?q={title}&s=tt&ttype=ft&ref_=fn_ft'
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'html.parser')
        result = soup.find('td', attrs={'class': 'result_text'})
        movie_link = result.a.get('href')
        movie_name = result.a.text

        # scrape movie storyline
        url2 = f'https://www.imdb.com{movie_link}'
        content2 = requests.get(url2).content
        soup = BeautifulSoup(content2, 'html.parser')
        parent = soup.find(
            'div', attrs={'class': 'ipc-html-content ipc-html-content--base'}
        )
        element = parent.div.text
        msg = (
            f'Movie Name: {movie_name}\n'
            f'Storyline: {element}'
        )
        await ctx.reply(msg)

    @movie.error
    async def movie_error(self, ctx, exc):
        if isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$movie "<title>"```')


def setup(bot):
    bot.add_cog(Day7(bot))
