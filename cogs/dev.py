from discord.ext import commands
from discord.utils import get
import discord

from utils import API_URL, s
import requests
import utils


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class MissingAttachment(commands.errors.CommandError):
        """
        Exception raised when required attachment is missing.

        This inherits from :exc:`CommandError`.
        """
        pass

    @commands.command()
    @commands.has_role('Pyrates')
    async def devecho(self, ctx, channel: discord.TextChannel, message):
        """
        Sends message to a channel

        Args:
            channel: Destination channel
            message: Message body wrapped in double quotes
        """
        await channel.send(message)

    @commands.command()
    @commands.has_role('Pyrates')
    async def devattach(self, ctx, channel: discord.TextChannel, message):
        """
        Sends message with attachment to a channel

        Args:
            channel: Destination channel
            message: Message body wrapped in double quotes
            attachment: Any file supported by Discord
        """
        if len(ctx.message.attachments) > 0:
            file = await ctx.message.attachments[0].to_file()

            await channel.send(message, file=file)
        else:
            raise self.MissingAttachment

    @commands.command()
    @commands.has_role('Pyrates')
    async def givexp(self, ctx, user: discord.Member, xp: int = 10):
        """
        Awards XP to a user

        Args:
            user: User to award XP
            xp(int): Optional argument XP amount
        """
        # get user data
        url = f'{API_URL}/users/{user.id}'
        get_r = s.get(url, timeout=10)

        if get_r.status_code != requests.codes.ok:
            get_r.raise_for_status()

        # update user table
        data = get_r.json()
        put_data = {'xp': data['xp'] + xp}
        put_r = s.put(url, json=put_data, timeout=10)

        if put_r.status_code != requests.codes.ok:
            put_r.raise_for_status()

    @commands.command()
    @commands.has_role('Pyrates')
    async def enrol(self, ctx, user: discord.Member, cohort_id: int = 0):
        """
        Enrols user to a cohort

        Args:
            user: User to enrol
            cohort_id(int): Cohort ID, defaults to current active cohort
        """
        # create user
        user_url = f'{API_URL}/users'
        post_user_data = {
            'id': user.id,
            'name': user.name,
            'discriminator': user.discriminator,
            'display_name': user.display_name
        }
        user_r = s.post(user_url, json=post_user_data, timeout=10)

        if user_r.status_code != requests.codes.created \
                and user_r.status_code != requests.codes.conflict:
            user_r.raise_for_status()

        # create enrolment
        cohort_id = cohort_id if cohort_id != 0 else utils.active_cohort['id']
        enrolment_url = f'{API_URL}/enrolments'
        post_enrolment_data = {
            'user_id': user.id,
            'cohort_id': cohort_id
        }
        enrolment_r = s.post(
            enrolment_url, json=post_enrolment_data, timeout=10
        )

        if enrolment_r.status_code != requests.codes.created \
                and enrolment_r.status_code != requests.codes.conflict:
            enrolment_r.raise_for_status()

        # assign '@Students' role
        role_students = get(ctx.guild.roles, name='Students')

        await user.add_roles(role_students)

        # discord.py Botcamp
        if cohort_id in utils.dpy:
            # create user channel
            role_dev_bot = get(ctx.guild.roles, name='Pyrate Bot')
            role_bocals = get(ctx.guild.roles, name='BOCALs')
            role_observers = get(ctx.guild.roles, name='Observers')
            role_digital_penang = get(ctx.guild.roles, name='Digital Penang')
            overwrites = {
                role_dev_bot: discord.PermissionOverwrite(
                    read_messages=True
                ),
                role_bocals: discord.PermissionOverwrite(
                    read_messages=True
                ),
                role_observers: discord.PermissionOverwrite(
                    read_messages=True
                ),
                # digital penang
                role_digital_penang: discord.PermissionOverwrite(
                    read_messages=True
                ),
                user: discord.PermissionOverwrite(read_messages=True),
                ctx.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False
                )
            }
            topic = 'Test your bot here!'
            ctg_eval = get(
                ctx.guild.categories, name='1-to-1 peer discussions'
            )
            chn_eval = await ctg_eval.create_text_channel(
                user.name,
                overwrites=overwrites,
                topic=topic
            )
            channel_url = f'{API_URL}/channels'
            post_channel_data = {
                'id': chn_eval.id,
                'name': chn_eval.name,
                'user_id': user.id,
                'cohort_id': cohort_id
            }
            channel_r = s.post(channel_url, json=post_channel_data, timeout=10)

            if channel_r.status_code == requests.codes.conflict:
                await chn_eval.delete()
            elif channel_r.status_code != requests.codes.created:
                channel_r.raise_for_status()

            # assign cohort role
            if cohort_id == utils.C4T_DPY_ALPHA:
                role_name = 'C4T discord.py Botcamp (Alpha)'
            elif cohort_id == utils.C4T_DPY_BETA:
                role_name = 'C4T discord.py Botcamp (Beta)'
            elif cohort_id == utils.C4T_DPY_DEC2021:
                role_name = 'C4T discord.py Botcamp (Dec 2021)'
            elif cohort_id == utils.C4W_DPY_FEB2022:
                role_name = 'C4W discord.py Botcamp (Feb 2022)'
            elif cohort_id == utils.C4T_DPY_MAR2022:
                role_name = 'C4T discord.py Botcamp (Mar 2022)'
            elif cohort_id == utils.C4T_DPY_TEST:
                role_name = 'C4T discord.py Botcamp (Test)'

            role_cohort = get(ctx.guild.roles, name=role_name)

            await user.add_roles(role_cohort)

        # send command completion message
        if enrolment_r.status_code == requests.codes.created:
            enrolment_data = enrolment_r.json()
            message = (
                f'{user.mention} enrolled to '
                f'{enrolment_data["cohort"]["name"]}.'
            )
        else:
            cohort_url = f'{API_URL}/cohorts/{cohort_id}'
            cohort_r = s.get(cohort_url, timeout=10)

            if cohort_r.status_code != requests.codes.ok:
                cohort_r.raise_for_status()

            cohort_data = cohort_r.json()
            message = (
                f'{user.mention} already enrolled to {cohort_data["name"]}.'
            )

        await ctx.reply(message)

    @devecho.error
    async def devecho_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument) \
                or isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$devecho <channel> "<message>"```')

    @devattach.error
    async def devattach_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument) \
                or isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$devattach <channel> "<message>"```')
        elif isinstance(exc, self.MissingAttachment):
            await ctx.reply('You forgot to include the attachment.')

    @givexp.error
    async def givexp_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument) \
                or isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$givexp <student> <xp>```')

    @enrol.error
    async def enrol_error(self, ctx, exc):
        if isinstance(exc, commands.BadArgument) \
                or isinstance(exc, commands.MissingRequiredArgument):
            await ctx.reply('```$enrol <student> <cohort_id>```')


def setup(bot):
    bot.add_cog(Dev(bot))
