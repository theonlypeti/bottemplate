import asyncio
import random
from datetime import datetime
from typing import Literal

import emoji
import nextcord as discord
from nextcord.ext import commands
from utils import embedutil


class AdvancedCog(commands.Cog):  # cog for more commands and components
    def __init__(self, client):
        self.logger = client.logger.getChild(f"{self.__module__}")
        self.client = client
        # https://github.com/nextcord/nextcord/tree/master/examples/application_commands

    # https://docs.nextcord.dev/en/stable/api.html#event-reference

    # @commands.Cog.listener("on_member_join")
    # async def welcomer(self, member):
    #   ...
    #
    # this is what you would use it for, but for testing, it is more convenient doing a voice update,
    # than having to leave and join servers (also keeping track of which channel to send the welcome to)

    @commands.Cog.listener("on_voice_state_update")  # on joining a voice channel
    async def welcomer(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """sends a welcome message to the joined voice's text channel"""
        if after.channel:
            await after.channel.send(embed=self.return_welcome_embed(member))

    @discord.slash_command(description="Test the welcome message right here right now!")  # type / in chat
    async def welcome(self, interaction: discord.Interaction):
        await interaction.send(embed=self.return_welcome_embed(interaction.user))

    # https://docs.nextcord.dev/en/stable/api.html#member
    # https://docs.nextcord.dev/en/stable/api.html#embed
    def return_welcome_embed(self, member: discord.Member) -> discord.Embed:
        embed = discord.Embed(
            title=f"Hello {member.display_name}",
            description=f"Welcome to the {member.guild.name} server!"
        )
        embed.add_field(name="Current members", value=len(member.guild.humans))
        embed.add_field(name="Current bots", value=len(member.guild.bots))

        if member.guild.icon:
            embed.set_thumbnail(url=member.guild.icon.url)

        embed.set_image(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Welcomedd.jpg/800px-Welcomedd.jpg")

        embed.set_author(icon_url=member.display_avatar, name=member.display_name)
        embed.set_footer(text="This is an automated message.", icon_url=member.guild.me.display_avatar.url)
        embed.timestamp = datetime.now()

        return embed

    @discord.slash_command(name="dmme", description="pls dm me bby")
    async def DMme(self, interaction):
        await interaction.user.send("Hi baby")
        await embedutil.success(interaction, "Done!")  # helper function to quickly respond with a fancy embed.
        # We have to respond to the interaction, sending a message to a user is not a response.

    @discord.slash_command(description="Send a button with a link")
    async def webpage(self, interaction: discord.Interaction):
        # await interaction.response.defer()

        viewObj = discord.ui.View()
        # https://docs.nextcord.dev/en/latest/api.html#view

        buttonObj = discord.ui.Button(
            label="Webpage:",
            emoji=emoji.emojize(":globe_with_meridians:"),
            url="https://www.example.com",
            style=discord.ButtonStyle.url
        )

        viewObj.add_item(buttonObj)

        with interaction.channel.typing():
            await asyncio.sleep(2)
            await interaction.send("For more info click the button:", view=viewObj)

        # https://github.com/nextcord/nextcord/tree/master/examples/views

    @discord.slash_command(description="Heads or tails")
    async def flip(self, interaction: discord.Interaction, choice: Literal["Heads", "Tails"]):
        # typehinting is how you define the expected parameters of a command.
        # https://docs.nextcord.dev/en/latest/api.html#slash-options
        # Either that or
        # https://docs.nextcord.dev/en/latest/api.html#slash-options
        # choice = discord.SlashOption(name=..., description=..., choices=[...], required=...)

        flipped = random.choice(["Heads", "Tails"])
        await interaction.send(f"{flipped} :" + ")" if flipped == choice else "(")


def setup(client):
    client.add_cog(AdvancedCog(client))
