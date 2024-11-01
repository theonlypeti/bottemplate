import random
import nextcord as discord
from nextcord.ext import commands


class BasicCommands(commands.Cog):  # cog for basic commands
    def __init__(self, client):
        self.logger = client.logger.getChild(f"{self.__module__}")
        self.client = client

    @discord.slash_command()  # type / in chat (command name will be the function name, unless set otherwise)
    async def hello(self, interaction: discord.Interaction):
        await interaction.send(
            random.choice(
                ("Shut up",
                 "Hello ^^",
                 "HI!",
                 f"'Sup {interaction.user.name}",
                 f"Welcome to {interaction.channel.name}"
                 )
            )
        )
        # https://docs.nextcord.dev/en/stable/api.html#interaction

    @discord.user_command(name="Steal profile pic")  # right click on user
    async def stealpfp(self, interaction: discord.Interaction, user: discord.User):
        await interaction.send(user.avatar.url)
        # https://docs.nextcord.dev/en/stable/api.html#id5

    # https://docs.nextcord.dev/en/stable/api.html#message
    @discord.message_command(name="You are a clown")  # right click on message
    async def randomcase(self, interaction: discord.Interaction, message: discord.Message):
        assert message.content
        await interaction.send(
            "".join(random.choice([letter.casefold(), letter.upper()]) for letter in message.content) + " <:pepeclown:803763139006693416>")

    @discord.slash_command(name="run", description="For running python code")
    async def run(self, ctx: discord.Interaction, command: str):  # back in the day it was context, not interaction and it is shorter to write out in chat lol so i just stuck with it
        await ctx.response.defer()  # for longer calculations this will wait for up to 15 mins
        if "@" in command:
            await ctx.send("oi oi oi we pinging or what?")
            return
        if any((word in command for word in ("open(", "os.", "eval(", "exec("))):
            await ctx.send("oi oi oi we hackin or what?")
            return
        try:
            a = eval(command)
            await ctx.send(a)
        except Exception as e:
            await ctx.send(f"{e}")
        # try /run ctx.user.avatar.url for example hehe


def setup(client):
    client.add_cog(BasicCommands(client))
