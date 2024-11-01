import nextcord as discord
from nextcord.ext import commands
from utils.paginator import Paginator
from utils.Inventory import Inventory
from utils.permcheck import can_i
from utils.webhook_manager import WebhookManager
import string
from data.consts import TESTSERVER_ID as TEST


class Testing(commands.Cog):
    def __init__(self, client):
        global logger
        logger = client.logger.getChild(f"{self.__module__}")
        self.client = client

        # Replace TESTSERVER_ID with your server id in data/consts.py
        # commands in this file will only show up in your server that you specify here
        if TEST[0] == 957469186798518282:  # default check, ignore this if you changed it already
            logger.warning("in data/consts.py replace the test server id to your server's id for the testing commands to show up in your server.")

    class Testvw(discord.ui.View):
        def __init__(self, user: discord.Member):
            self.msg = None
            self.user = user
            super().__init__(timeout=30)

        @discord.ui.button(label="test")
        async def test(self, button, interaction):
            logger.info("button pressed")
            button.style = discord.ButtonStyle.green
            await self.msg.edit(view=self)

        async def on_timeout(self) -> None:
            logger.info("view timeouted, noone pressed it in time")
            self.children[0].disabled = True
            await self.msg.edit(view=self)

        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            """if this button is not pressed by the command caller, it won't work."""
            return interaction.user == self.user

    class TextInputModal(discord.ui.Modal):
        def __init__(self):
            super().__init__(title="Testing")
            self.inputtext = discord.ui.TextInput(label="Say something", required=False)
            self.add_item(self.inputtext)

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.defer()
            await interaction.send(f"{interaction.user} says {self.inputtext.value}")

    @discord.slash_command(name="testingvw", description="testing", guild_ids=TEST)
    async def testing(self, interaction: discord.Interaction):
        viewObj = self.Testvw(interaction.user)
        viewObj.msg = await interaction.send(content="Hello", view=viewObj, tts=True)

    @discord.slash_command(name="modaltesting", description="testing", guild_ids=TEST)
    async def modaltesting(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.TextInputModal())

    @discord.slash_command(name="pagitest", description="testing", guild_ids=TEST)
    async def pagitest(self, interaction: discord.Interaction):
        embeds = [
            discord.Embed(
                title=f"Page {i}",
                description=f"Page {i} of 5",
                color=discord.Color.random()
            )
            for i in range(1, 6)
        ]
        pagi = Paginator(func=lambda pagin: embeds[pagin.page], select=None, inv=embeds, itemsOnPage=1)
        await pagi.render(interaction, ephemeral=True)

    @discord.slash_command(name="invtest", guild_ids=TEST, description="Inventory test")
    async def invtest(self, interaction: discord.Interaction):
        a = list(string.ascii_uppercase)
        inv: Inventory = Inventory(a)
        await inv.render(interaction, ephemeral=True)
        #inv.inv to take the list of items

    @discord.slash_command(name="webhooktest", description="Send webhook", guild_ids=TEST)
    async def whtest(self, interaction: discord.Interaction):
        async with WebhookManager(interaction) as wh:  # type: discord.Webhook
            await wh.send("Hello", username="Test", avatar_url=interaction.user.avatar.url)

    @discord.slash_command(name="permissioncheck", description="Permission check", guild_ids=TEST)
    async def whtest(self, interaction: discord.Interaction):
        if can_i(interaction).send_messages:
            perms = "You can send messages"
            if can_i(interaction).manage_messages:
                perms += ", manage messages"
            if can_i(interaction).manage_emojis:
                perms += ", manage emojis"
            if can_i(interaction).manage_channels:
                perms += ", manage channels"
            ...
            await interaction.send(perms)


def setup(client):
    client.add_cog(Testing(client))

