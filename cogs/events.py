from datetime import datetime
import random
import sqlite3

from discord.ext import commands
import discord
import pytz

import utils as utl


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        now = datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
        print(f'{utl.green}{now}: {self.bot.user.name} is online!{utl.reset}')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with sqlite3.connect(f'db/main.sqlite') as con:
            cur = con.cursor()
            cur.execute(
                'CREATE TABLE IF NOT EXISTS main ('
                'key TEXT PRIMARY KEY, '
                'value TEXT)'
            )
            con.commit()

        with sqlite3.connect(f'db/{guild.id}.sqlite') as con:
            cur = con.cursor()
            cur.execute(
                'CREATE TABLE IF NOT EXISTS main ('
                'key TEXT PRIMARY KEY, '
                'value TEXT)'
            )
            cur.execute(
                'CREATE TABLE IF NOT EXISTS students ('
                'id INTEGER PRIMARY KEY, '
                'name TEXT, '
                'nickname TEXT, '
                'chn_id INTEGER, '
                'bot_id INTEGER, '
                'bot_msg_id TEXT, '
                'evaluator_id INTEGER, '
                'lvl INTEGER, '
                'xp INTEGER)'
            )
            cur.execute(
                'CREATE TABLE IF NOT EXISTS evals ('
                'day INTEGER, '
                'date TEXT, '
                'eval_code INTEGER PRIMARY KEY, '
                'coder_id INTEGER, '
                'tester_id INTEGER)'
            )
            con.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            with sqlite3.connect(f'db/{member.guild.id}.sqlite') as con:
                cur = con.cursor()
                cur.execute(
                    'SELECT id, chn_id, bot_msg_id FROM students '
                    'WHERE bot_id = ?',
                    (member.id,)
                )
                owner_id, chn_eval_id, msg_id = cur.fetchone()

            # send welcome message to '#chit-chat'
            chn_chit_chat = discord.utils.get(
                member.guild.text_channels,
                name='chit-chat'
            )
            owner = discord.utils.get(member.guild.members, id=owner_id)
            await chn_chit_chat.send(
                f'Welcome {owner.mention}\'s bot, {member.mention}!'
            )

            # assign bot '@Student Bots' role
            role_student_bots = discord.utils.get(
                member.guild.roles,
                name='Student Bots'
            )
            await member.add_roles(role_student_bots)

            # grant bot permission to view owner's channel
            chn_eval = discord.utils.get(
                member.guild.text_channels,
                id=chn_eval_id
            )
            await chn_eval.set_permissions(member, view_channel=True)

            # mark bot-invite message in '#server-log' as successful
            chn_server_log = discord.utils.get(
                member.guild.text_channels,
                name='server-log'
            )
            msg = await chn_server_log.fetch_message(msg_id)
            await msg.add_reaction('🟢')
        else:
            with sqlite3.connect(f'db/{member.guild.id}.sqlite') as con:
                cur = con.cursor()
                cur.execute('SELECT value FROM main WHERE key = "coc_msg_id"')
                msg_id, = cur.fetchone()

            # send welcome DM
            chn_coc = discord.utils.get(
                member.guild.text_channels,
                name='code-of-conduct'
            )
            msg = chn_coc.get_partial_message(msg_id)
            text = (
                f'Welcome to {member.guild}, {member.name}!\n'
                '\n'
                'If you are a student, please read the Code of Conduct:\n'
                f'{msg.jump_url}.\n'
                '\n'
                'If you are not a student, please wait for the Pyrates to '
                'grant you your Role.'
            )

            if member.dm_channel is not None:
                await member.dm_channel.send(text)

                # try:
                #     await member.dm_channel.send(text)
                # except Exception as _:  # expect AttributeError
                #     dm = await member.create_dm()
                #     await dm.send(text)

        # send log to '#server-log'
        chn_server_log = discord.utils.get(
            member.guild.text_channels,
            name='server-log'
        )
        now = datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
        await chn_server_log.send(
            '```diff\n'
            f'# {now}\n'
            '\n'
            f'+ {member}: {member.id} joined the server.```'
        )

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not after.bot:
            with sqlite3.connect(f'db/{after.guild.id}.sqlite') as con:
                cur = con.cursor()
                cur.execute(
                    'UPDATE students SET nickname = ? WHERE id = ? ',
                    (after.display_name, after.id)
                )
                con.commit()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            # update database
            with sqlite3.connect(f'db/{member.guild.id}.sqlite') as con:
                cur = con.cursor()
                cur.execute(
                    'UPDATE students SET '
                    'bot_id = NULL, '
                    'bot_msg_id = NULL '
                    'WHERE bot_id = ? ',
                    (member.id,)
                )
                con.commit()
        else:
            role_students = discord.utils.get(
                member.guild.roles,
                name='Students'
            )

            if role_students not in member.roles:
                return

            # update database
            with sqlite3.connect(f'db/{member.guild.id}.sqlite') as con:
                cur = con.cursor()
                cur.execute(
                    'SELECT chn_id FROM students WHERE id = ?',
                    (member.id,)
                )
                chn_id, = cur.fetchone()
                cur.execute('DELETE FROM students WHERE id = ?', (member.id,))
                con.commit()

            # rename inactive user channel
            chn = discord.utils.get(member.guild.text_channels, id=chn_id)
            await chn.edit(name=f'mia-{chn.name}', position=0)

        # send log to '#server-log'
        chn_server_log = discord.utils.get(
            member.guild.text_channels,
            name='server-log'
        )
        now = datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
        await chn_server_log.send(
            '```diff\n'
            f'# {now}\n'
            '\n'
            f'- {member}: {member.id} left the server.```'
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.guild is None:
            return

        # if not webhook, grant xp
        if hasattr(message.author, 'roles'):
            givexp = self.bot.get_command('givexp')
            ctx = await self.bot.get_context(message)
            await givexp(ctx, message.author)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.user.id != payload.user_id:
            if payload.guild_id is not None:
                guild = self.bot.get_guild(payload.guild_id)

                with sqlite3.connect(f'db/{guild.id}.sqlite') as con:
                    cur = con.cursor()
                    cur.execute(
                        'SELECT value FROM main WHERE key = "coc_msg_id"'
                    )
                    msg_id, = [*map(int, cur.fetchone())]

                member = discord.utils.get(guild.members, id=payload.user_id)

                if payload.message_id == msg_id \
                        and payload.event_type == 'REACTION_ADD' \
                        and str(payload.emoji) == '🆗' \
                        and member.id not in utl.admins \
                        and len(member.roles) == 1:

                    # assign '@Students' role
                    role_students = discord.utils.get(
                        guild.roles,
                        name='Students'
                    )
                    await member.add_roles(role_students)

                    # send welcome message to '#chit-chat'
                    chn_chit_chat = discord.utils.get(
                        guild.text_channels,
                        name='chit-chat'
                    )
                    chn_alerts = discord.utils.get(
                        guild.text_channels,
                        name='alerts'
                    )
                    chn_padlet = discord.utils.get(
                        guild.text_channels,
                        name='padlet'
                    )
                    greets = [
                        'Greetings', 'Hey', 'Hi', 'Howdy', 'Welcome', 'Yo'
                    ]
                    greet = random.choice(greets)

                    await chn_chit_chat.send(
                        f'{greet} {member.mention}! Kindly check out '
                        f'{chn_alerts.mention} & {chn_padlet.mention}.'
                    )

                    # create user channel
                    ctg_bot = discord.utils.get(guild.categories, name='bot')
                    role_dev_bot = discord.utils.get(
                        guild.roles,
                        name='Pyrate Bot'
                    )
                    role_bocals = discord.utils.get(guild.roles, name='BOCALs')
                    role_observers = discord.utils.get(
                        guild.roles,
                        name='Observers'
                    )
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(
                            read_messages=False
                        ),
                        role_dev_bot: discord.PermissionOverwrite(
                            read_messages=True
                        ),
                        role_bocals: discord.PermissionOverwrite(
                            read_messages=True
                        ),
                        role_observers: discord.PermissionOverwrite(
                            read_messages=True
                        ),
                        member: discord.PermissionOverwrite(read_messages=True)
                    }
                    topic = 'Test your bot here!'
                    chn_eval = await ctg_bot.create_text_channel(
                        member.name,
                        overwrites=overwrites,
                        topic=topic
                    )

                    # update database
                    with sqlite3.connect(f'db/{guild.id}.sqlite') as con:
                        cur = con.cursor()
                        cur.execute(
                            'INSERT INTO students '
                            '(id, name, nickname, chn_id, lvl, xp) '
                            'VALUES '
                            '(?, ?, ?, ?, ?, ?)',
                            (
                                member.id,
                                f'{member.name}#{member.discriminator}',
                                member.display_name,
                                chn_eval.id,
                                0,
                                0
                            )
                        )
                        con.commit()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await ctx.message.add_reaction('🟢')

        if ctx.command.name == 'say':
            try:
                await ctx.message.delete()
            except Exception as _:  # expect discord.Forbidden
                pass


def setup(bot):
    bot.add_cog(Events(bot))
