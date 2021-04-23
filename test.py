import discord

bot = discord.Client()
guild = bot.get_guild(829896340363542529)
print(guild.name)