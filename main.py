from discord.ext import commands
import discord

from utils import TOKEN

intents = discord.Intents(
    guilds=True,
    members=True,
    messages=True,
    reactions=True
)
bot = commands.Bot(command_prefix='$', intents=intents)
bot.load_extension('cogs.schedule')
bot.load_extension('cogs.events')
bot.load_extension('cogs.dev')
bot.load_extension('cogs.student')
bot.load_extension('cogs.day3')
bot.load_extension('cogs.day4')
bot.load_extension('cogs.day5')
bot.load_extension('cogs.day7')
bot.load_extension('cogs.day8')
bot.load_extension('cogs.hidden')
bot.run(TOKEN)
