from os import getenv
from random import choice

import discord
from discord.ext import commands

from services.podservice import PodService
from utils import checks


def generate_message(team_name):
    title_options = [
        f"How's life {team_name}?",
        "Hello, living organism! How do you do this fine [weather:city] day?",
        "Howdy do!?!",
    ]
    message_options = [
        f"Good? I hope so! Please, go to the link down there and tell me so we can keep tabs on how you're doing. Thanks!",
        f"Hope you're programming is going swell! I have orders to have you fill out the form down there so my fellow staff can keep up to date. Thanks!",
        f"I'm feeling pretty [john:emotion]! Please, tell me how you are feeling about your project down there. Bye for now!",
    ]
    return choice(title_options) + " " + choice(message_options)


class CheckinCommands(commands.Cog, name="Checkin"):
    """Contains pod checkin commands"""

    def __init__(self, bot):
        self.bot = bot
        self.category = int(getenv("CATEGORY", 783229579732320257))

    @commands.command(name='checkin')
    @checks.requires_staff_role()
    async def checkin(self, ctx, pod_name):
        """Checks in on a specific pod"""
        guild: discord.Guild = self.bot.guild
        pod = PodService.get_pod_by_name(pod_name)
        channel: discord.DMChannel = guild.get_channel(int(pod.tc_id))
        message = await channel.send("Hello! This is your friendly Showcase bot! Please react "
                                     "to this message with one of the emojis below with "
                                     "how you are feeling about your project so far!")
        await message.add_reaction("😀")
        await message.add_reaction("😐")
        await message.add_reaction("☹")

    @commands.command(name='checkin_all')
    @checks.requires_staff_role()
    def checkin_all(self, ctx: commands.Context):
        """checks in on all teams"""
        guild: discord.Guild = self.bot.guild
        for pod in PodService.get_all_pods():
            channel: discord.DMChannel = guild.get_channel(int(pod.tc_id))
            message = await channel.send("Hello! This is your friendly Showcase bot! Please react "
                                         "to this message with one of the emojis below with "
                                         "how you are feeling about your project so far!")
            await message.add_reaction("😀")
            await message.add_reaction("😐")
            await message.add_reaction("☹")


def setup(bot):
    bot.add_cog(CheckinCommands(bot))
