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
        r = requests.get(url)

        if r.status_code != requests.codes.ok:
            r.raise_for_status()

        content = r.content
        soup = BeautifulSoup(content, 'html.parser')

        # get user information
        name1 = soup.tbody.tr.td.find_next('td')
        name2 = name1.find_next('td')
        name3 = name2.find_next('td')
        message = (
            f'First Name = {name1.text}\n'
            f'Last Name = {name2.text}\n'
            f'Username = {name3.text}'
        )

        await ctx.reply(message)

    @commands.command()
    async def movie(self, ctx, title):
        """
        Scrapes movie storyline from title

        Args:
            title: Movie title wrapped in double quotes
        """
        search_url = \
            f'https://www.imdb.com/find?q={title}&s=tt&ttype=ft&ref_=fn_ft'
        search_r = requests.get(search_url)

        if search_r.status_code != requests.codes.ok:
            search_r.raise_for_status()

        search_content = search_r.content
        soup = BeautifulSoup(search_content, 'html.parser')

        # scrape search results
        result = soup.find('td', attrs={'class': 'result_text'})
        movie_link = result.a.get('href')
        movie_title = result.a.text

        # scrape movie storyline
        movie_url = f'https://www.imdb.com{movie_link}'
        movie_r = requests.get(movie_url)

        if movie_r.status_code != requests.codes.ok:
            movie_r.raise_for_status()

        movie_content = movie_r.content
        soup = BeautifulSoup(movie_content, 'html.parser')
        parent = soup.find(
            'div', attrs={'class': 'ipc-html-content ipc-html-content--base'}
        )
        storyline = parent.div.text
        message = (
            f'Movie Title: {movie_title}\n'
            '\n'
            f'Storyline: {storyline}'
        )

        await ctx.reply(message)

    @movie.error
    async def movie_error(self, ctx, exc):
        if isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$movie "<title>"```')


def setup(bot):
    bot.add_cog(Day7(bot))
