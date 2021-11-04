import random

from discord.ext import commands
import discord
import requests


class Day5(commands.Cog, name='Day 5'):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = [
            '🧸', '😍', '👏🏻', '🥺', '🥰', '🤦🏻‍♀️', '😆',
            '😏', '🥴', '🤯', '😑', '🥳', '🤑', '👻'
        ]
        self.gifs = [
            '861409ba9b00e46a67f4f7be00cee2f7/tenor.gif?itemid=16992959',
            'a7ae94274d1bc120b1a59382ef5ac66b/tenor.gif?itemid=13418523',
            '24ac13447f9409d41c1aecb923aedf81/tenor.gif?itemid=5026057',
            'f6f02f22f3da8a85d8f600a947144b6d/tenor.gif?itemid=17202817',
            '0796f5445e9730634315351c86d00e99/tenor.gif?itemid=15323902',
            'ed628307910258f8d23796b7029faa19/tenor.gif?itemid=12251780',
            '1c7bc370dc6ac84cc79660eba1f4f2c7/tenor.gif?itemid=15443300',
            '119dd3797490c22e49cf42e5357fb719/tenor.gif?itemid=4869672',
            '5a85818cb17039f20e3c31ba87005b72/tenor.gif?itemid=17640265',
            'd3dac1b007907d196e3235d7fe251efe/tenor.gif?itemid=16999811',
            '58de9f3c43b92e5f4cacc57714fd9fa5/tenor.gif?itemid=16216173'
        ]

    @commands.command()
    async def emoji(self, ctx):
        """
        Returns a random emoji
        """
        await ctx.reply(random.choice(self.emojis))

    @commands.command()
    async def emoji_embed(self, ctx):
        """
        Returns a random emoji in an embed message
        """
        embed = discord.Embed(
            title="Emoji Function ON",
            description="Sending emoji: ",
            color=0x4b0082
        )
        emoji = random.choice(self.emojis)
        embed.add_field(
            name=f'{emoji}',
            value="--- Successful ---",
            inline=False
        )

        await ctx.reply(embed=embed)

    @commands.command()
    async def gif(self, ctx):
        """
        Returns a random GIF
        """
        embed = discord.Embed(
            title="GIFs Function ON",
            description="Sending GIF: ",
            color=0xee82ee
        )
        gif = random.choice(self.gifs)
        url = f'https://media1.tenor.com/images/{gif}'
        embed.set_image(url=url)

        await ctx.reply(embed=embed)

    @commands.command()
    async def intro(self, ctx):
        """
        Sends introduction message with photo from local directory
        """
        text = f'Hello coders, I am {ctx.author.mention}! Nice to meet you! 😆'
        file = discord.File('assets/logo.png')

        await ctx.reply(text, file=file)

    @commands.command()
    async def img(self, ctx):
        """
        Downloads image from predefined link and sends the image
        """
        url = 'https://i.imgur.com/SKuJOWE.jpeg'
        filename = 'assets/photo.jpg'
        content = requests.get(url).content

        with open(filename, 'wb') as f:
            f.write(content)

        await ctx.reply(file=discord.File(filename))

    @commands.command()
    async def react(self, ctx):
        """
        Reacts to message based on mood
        """
        mood = ctx.message.content[7:]

        if mood == "happy":
            await ctx.message.add_reaction("😄")
        elif mood == "sad":
            await ctx.message.add_reaction("😞")
        elif mood == "love":
            await ctx.message.add_reaction("🥰")
        elif mood == "wow":
            await ctx.message.add_reaction("🤩")
        elif mood == "lol":
            await ctx.message.add_reaction("🤣")
        elif mood == "teddy":
            await ctx.message.add_reaction("🧸")
        else:
            embed = discord.Embed(
                title='**Command Error**',
                description='Try: `$react [Available Options]`',
                color=0xff0000
            )
            embed.add_field(
                name='Available Options:',
                value=(
                    '1. happy\n'
                    '2. sad\n'
                    '3. love\n'
                    '4. wow\n'
                    '5. lol\n'
                    '6. teddy\n'
                ),
                inline=False
            )

            await ctx.message.add_reaction('✅')
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Day5(bot))
